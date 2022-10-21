#coding:utf-8
import json
import os
import geopandas as gpd

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
            if pathname.endswith('.json') or pathname.endswith('.shp'):

                gdf = gpd.read_file(pathname)
                polygons = gdf.geometry.to_json()
                polygon_dict = json.loads(polygons)

                i=0
                for district in  gdf.iloc:
                    try:
                        city = district[6]
                        province = district[4]
                        country = district[1]

                        #bound box
                        X1=district.geometry.bounds[0] 
                        Y1=district.geometry.bounds[1] 
                        X2=district.geometry.bounds[2] 
                        Y2=district.geometry.bounds[3] 

                        type = polygon_dict["features"][i]["geometry"]['type']
                        for polygon in polygon_dict["features"][i]["geometry"]["coordinates"]:

                            if type =='Polygon':
                                #simple polygon
                                data_list.append((country,province,city,X1,Y1,X2,Y2,str(polygon)))
                            else:
                                #multi polygon
                                for polygon_points in polygon:
                                    data_list.append((country,province,city,X1,Y1,X2,Y2,str(polygon_points)))
                    except Exception as error:
                        print(pathname)
                                
                    i = i + 1

    return data_list
