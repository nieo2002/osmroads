#coding:utf-8
import json
import os
import geopandas as gpd
import shapely.wkt as wkt
from shapely.geometry import MultiPolygon

#根据文件名区分不同的polygon
def build_polygon_from_files(dir):

    data_list = []

    roots = os.listdir(dir)
    for district in roots:
        pathname = os.path.join(dir, district)
        
        if (os.path.isfile(pathname)):
            if pathname.endswith('.json') or pathname.endswith('.shp'):

                gdf = gpd.read_file(pathname)
                polygons = gdf.geometry.to_json()
                polygon_dict = json.loads(polygons)

                for i in range(len(polygon_dict["features"])):

                    X1=gdf.iloc[i].geometry.bounds[0] 
                    Y1=gdf.iloc[i].geometry.bounds[1] 
                    X2=gdf.iloc[i].geometry.bounds[2] 
                    Y2=gdf.iloc[i].geometry.bounds[3] 

                    for polygon in polygon_dict["features"][i]["geometry"]["coordinates"]:
                        
                        if polygon_dict["features"][i]["geometry"]['type'] =='Polygon':
                            data_list.append((X1,Y1,X2,Y2,str(polygon),district[:district.index('.')]))
                        else:
                            for polygon_points in polygon:
                                data_list.append((X1,Y1,X2,Y2,str(polygon_points),district[:district.index('.')]))
    return data_list

#根据文件名区分不同的polygon
def build_polygon_from_gadmfile(dir):

    data_list = []

    roots = os.listdir(dir)
    for district in roots:
        pathname = os.path.join(dir, district)
        
        if (os.path.isfile(pathname)):
            if pathname.endswith('.json'):

                gdf = gpd.read_file(pathname)
                polygons = gdf.geometry.to_json()
                polygon_dict = json.loads(polygons)

                i=0
                for district in  gdf.iloc:

                    try:

                        country = district['COUNTRY']
                        level1 = ''
                        level2 = ''
                        level3 = ''
                        try:
                            level1 = district['NAME_1']
                        except Exception as name_1_error:
                            pass                        
                        try:
                            level2 = district['NAME_2']
                        except Exception as name_2_error:
                            pass
                        try:
                            level3 = district['NAME_3']
                        except Exception as name_3_error:
                            pass                        

                        #bound box
                        X1=district.geometry.bounds[0] 
                        Y1=district.geometry.bounds[1] 
                        X2=district.geometry.bounds[2] 
                        Y2=district.geometry.bounds[3] 

                        type = polygon_dict["features"][i]["geometry"]['type']
                        for polygon in polygon_dict["features"][i]["geometry"]["coordinates"]:

                            if type =='Polygon':
                                #simple polygon
                                data_list.append((country,level1,level2,level3,X1,Y1,X2,Y2,str(polygon)))
                            else:
                                #multi polygon
                                for polygon_points in polygon:
                                    data_list.append((country,level1,level2,level3,X1,Y1,X2,Y2,str(polygon_points)))
                    except Exception as error:
                        print(pathname)
                                
                    i = i + 1

    return data_list

def build_polygon_from_osm(dir):

    data_list = []

    roots = os.listdir(dir)
    for district in roots:
        pathname = os.path.join(dir, district)
        
        if (os.path.isfile(pathname)):
            if pathname.endswith('.json') or pathname.endswith('.geojson'):

                gdf = gpd.read_file(pathname)
                polygons = gdf.geometry.to_json()
                polygon_dict = json.loads(polygons)

                for i in range(len(gdf)):

                    try:
                        district = gdf.iloc[i]

                        #skip country boundary
                        if district.parents is None:
                            continue

                        parents = district.parents.split(',')
                        if len(parents) > 3:
                            continue
                        level = len(parents)
                        
                        X1=district.geometry.bounds[0] 
                        Y1=district.geometry.bounds[1] 
                        X2=district.geometry.bounds[2] 
                        Y2=district.geometry.bounds[3] 

                        #get distrinct attribute
                        name= district.name
                        name_en= district.name_en
                        if name_en is None:
                            name_en = ' '
                        name_local = district.local_name
                        if name_local is None:
                            name_local = ' '
                        
                        name_local = name_local.replace(';',',').replace('"','')
                        name = str(name).replace(';',',').replace('"','')
                        name_en = name_en.replace(';',',').replace('"','')

                        #parents = district.parents
                        osmid = district.osm_id
                        area = float(district.geometry.area)

                        for parent in parents:

                            #polygon_dict["features"][i]["geometry"]["coordinates"]
                            for polygon in polygon_dict["features"][i]["geometry"]["coordinates"]:
                                
                                if district.geometry.geom_type =='Polygon':
                                    data_list.append((name,name_en,name_local,osmid,level,parent,area,X1,Y1,X2,Y2,str(polygon)))
                                else:
                                    for polygon_points in polygon:
                                        data_list.append((name,name_en,name_local,osmid,level,parent,area,X1,Y1,X2,Y2,str(polygon_points)))
                    except Exception as error:
                        print(error)

                    i = i + 1

    return data_list
