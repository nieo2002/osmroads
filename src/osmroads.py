#coding:utf-8
from cs.CentralSystem import fetch_data_from_ns

def osm_road_lengths_v2(cityname,limit=1000):
    
    sql_cmd = 'select name.name, boundary.polygon, boundary.x1,boundary.y1,boundary.x2,boundary.y2 from osm_city_names name, osm_city_boundary boundary where name.osm_id = boundary.osmid and name.name=\'' +  cityname + '\' ' 
    sql_cmd += ' limit ' + str(limit)
 
    roads = []
    try:
        pologyons = fetch_data_from_ns(sql_cmd)
        lengths = 0.0

        for data in pologyons['value']:
            city = data[0]
            lon1 = data[2]
            lat1 = data[3]
            lon2 = data[4]
            lat2 = data[5]
            npstr= data[1] 

            #calculate city roads distances
            sql_cmd =  'select count(1) as roads,sum(distance) as distance ' + \
            'from ( ' + \
                'select lsid,sum(distance) as distance '  + \
                'from( ' + \
                    'SELECT lsid,geo_distance(x1,y1,x2,y2) as distance  ' + \
                        'FROM ( ' + \
                        '  select lsid,osmid_start_x x1,osmid_start_y y1, osmid_end_x x2,osmid_end_y y2, pnpoly(osmid_start_x,osmid_start_y,\'' + npstr + '\') as pnpolys,pnpoly(osmid_end_x,osmid_end_y,\'' + npstr + '\') as pnpolye ' + \
                        '  from osm_split_edge_roadnet_selected_t  ' + \
                        '  where osmid_start_x  < ' + str(lon2) + ' and osmid_start_x >  ' + str(lon1) + '  and osmid_start_y < ' + str(lat2) + '  and osmid_start_y > ' + str(lat1)  +  \
                        ' ) ' + \
                    'where  pnpolys = true and pnpolye = true' + \
                ') ' + \
                'group by lsid ' + \
            ')'
            
            road = fetch_data_from_ns(sql_cmd)

            result = {'city':cityname,'value':road}
            roads.append(result)
            
    except Exception as error:
        print(error)
    
    return roads

def osm_road_lengths(country,level1,level2=None,level3=None,limit=1000):
    
    sql_cmd = ''    

    if country is None or level1 is None:
        print('parameter country and level1 can not be None.')
        return []
    else:
        level1 = level1.replace('\'',' ')
        sql_cmd = ' select osmid from osm_city_id where level = 1 and  regexp_replace(name,"\'"," ")=\'' + level1  + '\' and parent in ( select osmid from osm_city_id where level =0 and parent = \'' + ' \' and name=\'' + country + '\')'
        if level2 is not None:
            level2 = level2.replace('\'',' ')
            sql_cmd = ' select osmid from osm_city_id where level = 2 and  regexp_replace(name,"\'"," ")= \'' + level2  + '\' and parent in (' + sql_cmd + ' )'
            if level3 is not None:
                level3 = level3.replace('\'',' ')
                sql_cmd = ' select osmid from osm_city_id where level = 3 and  regexp_replace(name,"\'"," ")= \'' + level3  + '\' and parent in (' + sql_cmd + ' )'
            else:
                sql_cmd = 'select osmid from osm_city_id where level = 3 and parent in ( ' + sql_cmd + ' )'
        else:
            sql_cmd = 'select osmid from osm_city_id where level =2 and parent in ( ' + sql_cmd + ' )'

    sql_cmd += ' limit ' + str(limit)
    sql_cmd = 'select distinct localname,polygon,x1,y1,x2,y2,level from osm_city_boundary where osmid in ( ' + sql_cmd + ') '
    roads = []
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
            sql_cmd =  'select count(1) as roads,sum(distance) as distance ' + \
            'from ( ' + \
                'select lsid,sum(distance) as distance '  + \
                'from( ' + \
                    'SELECT lsid,geo_distance(x1,y1,x2,y2) as distance  ' + \
                        'FROM ( ' + \
                        '  select lsid,osmid_start_x x1,osmid_start_y y1, osmid_end_x x2,osmid_end_y y2, pnpoly(osmid_start_x,osmid_start_y,\'' + npstr + '\') as pnpolys,pnpoly(osmid_end_x,osmid_end_y,\'' + npstr + '\') as pnpolye ' + \
                        '  from osm_split_edge_roadnet_selected_t  ' + \
                        '  where osmid_start_x  < ' + str(lon2) + ' and osmid_start_x >  ' + str(lon1) + '  and osmid_start_y < ' + str(lat2) + '  and osmid_start_y > ' + str(lat1)  +  \
                        ' ) ' + \
                    'where  pnpolys = true and pnpolye = true' + \
                ') ' + \
                'group by lsid ' + \
            ')'
            
            road = fetch_data_from_ns(sql_cmd)
            
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
                
            result = {'country':country,'province':level1,'city':level2s,'district':level3s,'value':road}
            roads.append(result)
            
    except Exception as error:
        print(error)
    
    return roads

def gadm_road_distances(level3=None,level2=None,level1=None,country=None,limit=100):
    
    sql_cmd = 'select level2,level1,x1,y1,x2,y2,polygon,country,level3 from city_boundary_standard where '
    if level3 is None and level2 is None and level1 is None and country is None:
        return []

    if level3 is not None:
        sql_cmd += ' upper(level3) = \'' + level3.upper() + '\' and'

    if level2 is not None:
        sql_cmd += ' upper(level2) = \'' + level2.upper() + '\' and'

    if level1 is not None:
        sql_cmd += ' upper(level1) = \'' + level1.upper() + '\' and'

    if country is not None:
        sql_cmd += ' upper(country) = \'' + country.upper() + '\''
    
    if sql_cmd.endswith('and'):
        sql_cmd = sql_cmd[0:-3]

    sql_cmd += ' limit ' + str(limit)

    roads = []
    try:
        pologyons = fetch_data_from_ns(sql_cmd)
        for data in pologyons['value']:
            city = data[0]
            province = data[1]
            lon1 = data[2]
            lat1 = data[3]
            lon2 = data[4]
            lat2 = data[5]
            npstr= data[6] 
            country = data[7]
            county = data[8]

            #calculate city roads distances
            sql_cmd =  'select count(1) as roads,sum(distance) as distance ' + \
            'from ( ' + \
                'select lsid,sum(distance) as distance '  + \
                'from( ' + \
                    'SELECT lsid,geo_distance(x1,y1,x2,y2) as distance  ' + \
                        'FROM ( ' + \
                        '  select lsid,osmid_start_x x1,osmid_start_y y1, osmid_end_x x2,osmid_end_y y2, pnpoly(osmid_start_x,osmid_start_y,\'' + npstr + '\') as pnpolys,pnpoly(osmid_end_x,osmid_end_y,\'' + npstr + '\') as pnpolye ' + \
                        '  from osm_split_edge_roadnet_selected_t  ' + \
                        '  where osmid_start_x  < ' + str(lon2) + ' and osmid_start_x >  ' + str(lon1) + '  and osmid_start_y < ' + str(lat2) + '  and osmid_start_y > ' + str(lat1)  +  \
                        ' ) ' + \
                    'where  pnpolys = true and pnpolye = true' + \
                ') ' + \
                'group by lsid ' + \
            ')'
            
            road = fetch_data_from_ns(sql_cmd)
            result = {'country':country,'province':province,'city':city,'county':county,'value':road}
            roads.append(result)
            
    except Exception as error:
        print(error)
    
    return roads
