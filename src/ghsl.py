#coding:utf-8
from cs.CentralSystem import fetch_data_from_ns

def ghsl_population_query(country,level1,level2=None,level3=None,limit=1000):
    
    sql_cmd = ''    

    if country is None or level1 is None:
        print('parameter country and level1 can not be None.')
        return []
    else:
        sql_cmd = ' select osmid from osm_city_id where level = 1 and  upper(name)=\'' + level1.upper()  + '\' and parent in ( select osmid from osm_city_id where level =0 and parent = \'' + ' \' and upper(name)=\'' + country.upper() + '\')'
        if level2 is not None:
            sql_cmd = ' select osmid from osm_city_id where level = 2 and  upper(name)= \'' + level2.upper()  + '\' and parent in (' + sql_cmd + ' )'
            if level3 is not None:
                sql_cmd = ' select osmid from osm_city_id where level = 3 and  upper(name)= \'' + level3.upper()  + '\' and parent in (' + sql_cmd + ' )'
            else:
                sql_cmd = 'select osmid from osm_city_id where level = 3 and parent in ( ' + sql_cmd + ' )'
        else:
            sql_cmd = 'select osmid from osm_city_id where level =2 and parent in ( ' + sql_cmd + ' )'

    #sql_cmd += ' limit ' + str(limit)
    sql_cmd = 'select distinct localname,polygon,x1,y1,x2,y2,level from osm_city_boundary where osmid in ( ' + sql_cmd + ') '
    populations = []
    try:
        pologyons = fetch_data_from_ns(sql_cmd)
        for data in pologyons['value']:
            city = data[0]
            lon1 = data[2]
            lat1 = data[3]
            lon2 = data[4]
            lat2 = data[5]
            npstr= data[1] 
            level = data[6]

            #calculate city roads distances
            sql_cmd =  ' SELECT sum(population) as population ' + \
                        ' FROM ( ' + \
                        '  select population,pnpoly(x,y,\'' + npstr + '\') as pnpoly ' + \
                        '  from ghsl_population  ' + \
                        '  where x  < ' + str(lon2) + ' and x >  ' + str(lon1) + '  and y < ' + str(lat2) + '  and y > ' + str(lat1)  +  \
                        ' ) ' + \
                        ' where  pnpoly = true '
            
            population = fetch_data_from_ns(sql_cmd)
            
            level2s=''
            level3s=''
            if level2 is None:
                level2s = city
            else:
                level2s = level2
                if level3 is None:
                    level3s = city
                else:
                    level3s = level3
                
            result = {'country':country,'province':level1,'city':level2s,'district':level3s,'value':population}
            populations.append(result)
            
    except Exception as error:
        print(error)
    
    return populations
