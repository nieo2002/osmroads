#coding:utf-8
from cs.CentralSystem import fetch_data_from_ns

def osm_road_distances(level3=None,level2=None,level1=None,country=None,limit=100):
    
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
