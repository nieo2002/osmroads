#coding:utf-8
from cs.CentralSystem import fetch_data_from_ns

def osmroads(cityname,limit=1000):
    
    cityname = cityname.replace('\'',' ')
    sql_cmd = 'select distinct name.city, boundary.polygon, boundary.x1,boundary.y1,boundary.x2,boundary.y2,name.lon,name.lat from osm_city_names_aligned name, osm_city_boundary boundary where name.osmid = boundary.osmid and regexp_replace(name.city,"\'"," ")=\'' +  cityname + '\' ' 
    sql_cmd += ' limit ' + str(limit)
 
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
            city_lon = data[6]
            city_lat = data[7]

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

            result = {'city':cityname,'lon':city_lon,'lat':city_lat,'value':road}
            roads.append(result)
            
    except Exception as error:
        print(error)
    
    return roads
    
    return roads
