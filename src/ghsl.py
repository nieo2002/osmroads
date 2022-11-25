#coding:utf-8
from cs.CentralSystem import fetch_data_from_ns


def ghslpopulation(cityname,limit=1000):
    
    cityname = cityname.replace('\'',' ')
    sql_cmd = 'select distinct name.city, boundary.polygon, boundary.x1,boundary.y1,boundary.x2,boundary.y2,name.lon,name.lat from osm_city_names_aligned name, osm_city_boundary boundary where name.osmid = boundary.osmid and regexp_replace(name.city,"\'"," ")=\'' +  cityname + '\' ' 
    sql_cmd += ' limit ' + str(limit)
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
            city_lon = data[6]
            city_lat = data[7]

            #calculate city roads distances
            sql_cmd =  ' SELECT sum(population) as population ' + \
                        ' FROM ( ' + \
                        '  select population,pnpoly(x,y,\'' + npstr + '\') as pnpoly ' + \
                        '  from ghsl_population  ' + \
                        '  where x  < ' + str(lon2) + ' and x >  ' + str(lon1) + '  and y < ' + str(lat2) + '  and y > ' + str(lat1)  +  \
                        ' ) ' + \
                        ' where  pnpoly = true '
            
            population = fetch_data_from_ns(sql_cmd)
            result = {'city':cityname,'lon':city_lon,'lat':city_lat,'value':population}
            populations.append(result)
            
    except Exception as error:
        print(error)
    
    return populations
