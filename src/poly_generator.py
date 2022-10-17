#coding:utf-8
import geopandas as gpd
import json
import codecs
import csv
import os
from shapely.geometry import Polygon
import numpy as np
import sys

data_list = []

def make_mesh(box,w,h):
    [xmin,ymin,xmax,ymax]=box
    list_x=np.arange(xmin,xmax,w)
    list_y=np.arange(ymin,ymax,h)
    polygon_list=[]
    for i in range(len(list_x)):
        for j in range(len(list_y)):
            xleft=list_x[i]
            ydown=list_y[j]
            if i==len(list_x)-1:
                xright=xmax
            else:
                xright=list_x[i+1]
            if j==len(list_y)-1:
                yup=ymax
            else:
                yup=list_y[j+1]
            rectangle=Polygon([(xleft, ydown), (xright, ydown), (xright, yup), (xleft, yup)])
            polygon_list.append(rectangle)

    return gpd.GeoSeries(polygon_list)

def listDir(rootDir,x_split_size,y_split_size,points_split):

    roots = os.listdir(rootDir)
    for city in roots:
        pathname = os.path.join(rootDir, city)
        
        if (os.path.isfile(pathname)):
            if pathname.endswith('.json') or pathname.endswith('.shp'):
                #print(pathname)

                gdf = gpd.read_file(pathname)

                polygon = gdf.geometry.to_json()
                polygon_dict = json.loads(polygon)
                for i in range(len(polygon_dict["features"])):
                    for points in polygon_dict["features"][i]["geometry"]["coordinates"]:
                        new_points = []
                        polygon_points = points
                        if len(points) == 1 :
                            polygon_points = points[0]
                        for pt in polygon_points:
                            #x = round(pt[0],4)
                            x=pt[0] 
                            y=pt[1] 
                            #y = round(pt[1],3)
                            new_points.append((x,y))
                    
                        json_points = json.dumps(new_points)    
                        #print("len: ",len(new_points))

                        #X1 = round(gdf.iloc[0].geometry.bounds[0],4)  # 最左
                        #Y1 = round(gdf.iloc[0].geometry.bounds[1],4)  # 最下
                        #X2 = round(gdf.iloc[0].geometry.bounds[2],4)  # 最右
                        #Y2 = round(gdf.iloc[0].geometry.bounds[3],4)  # 最上
                        X1=gdf.iloc[0].geometry.bounds[0] 
                        Y1=gdf.iloc[0].geometry.bounds[1] 
                        X2=gdf.iloc[0].geometry.bounds[2] 
                        Y2=gdf.iloc[0].geometry.bounds[3] 

                        x1= X2 - X1
                        y1 = Y2 - Y1
                        split_cnt_x = 1
                        split_cnt_y = 1
                        flag = False

                        if len(new_points) > points_split: 
                            flag = True
                            while 1:
                                if x1 > x_split_size:
                                    split_cnt_x += 1
                                    x1 = round((X2 - X1)/split_cnt_x)
                                    continue
                                break
                            while 1:
                                if y1 > y_split_size:
                                    split_cnt_y += 1
                                    y1 = round((Y2 - Y1)/split_cnt_y)
                                    continue
                                break
                        else:
                            #write csv
                            data_list.append((X1,Y1,X2,Y2,json_points,city[:city.index('.')]))
                            continue

                        w= (gdf.iloc[0].geometry.bounds[2] - gdf.iloc[0].geometry.bounds[0])/split_cnt_x
                        h= (gdf.iloc[0].geometry.bounds[3] - gdf.iloc[0].geometry.bounds[1])/split_cnt_y
                        rect=make_mesh([gdf.iloc[0].geometry.bounds[0],gdf.iloc[0].geometry.bounds[1],gdf.iloc[0].geometry.bounds[2],gdf.iloc[0].geometry.bounds[3]],w,h)
                        rectangles=gpd.GeoDataFrame(geometry=rect)
                        rectangles['RectangleID']=range(len(rectangles))

                        res=gpd.sjoin(left_df=rectangles,
                                    right_df=gdf,
                                    how='right',
                                    op='intersects')

                        if len(new_points) > points_split:
                            g=res.groupby('RectangleID')
                            g=dict(list(g))

                            ax=gdf.plot()
                            color=['yellow','green','blue','black','purple','red']
                            for k,v in g.items():

                                    row=k//split_cnt_x
                                    col=k%split_cnt_y
                                    
                                    boundary = gpd.GeoSeries(rectangles['geometry'][k])
                                    boundary.boundary.plot(ax=ax,color=color[(row%6+col)%6])
                                    boundary_json = boundary.to_json()
                                    boundary_dict = json.loads(boundary_json)
                                    bbox = boundary_dict["features"][0]['bbox']

                                    ix1=bbox[0] 
                                    iy1=bbox[1]
                                    ix2=bbox[2] 
                                    iy2=bbox[3]
                                    data_list.append((ix1,iy1,ix2,iy2,json_points,city))
                                    print("deal with inner bbox...")
        else:
            listDir(pathname)

def data_write_csv(file_name, datas):
    file_csv = codecs.open(file_name,'w+','utf-8')
    writer = csv.writer(file_csv, delimiter=';', quotechar=';', quoting=csv.QUOTE_MINIMAL)
    
    for i in range(datas.__len__()):
        data = datas.pop()
        writer.writerow(data) 

#if len(sys.argv) != 5:
#    print("Usage: poly_generator.py city_polygon_dir x_split_size y_split_size points_split", file=sys.stderr)
#    print("shp_file_dir: where you put shp files", file=sys.stderr)
#    print("x_split_size: x split, as : 1.0 ", file=sys.stderr)
#    print("y_split_size: y split, as : 0.5", file=sys.stderr)
#    print("points_split: maximum points in one polygon, as : 3000", file=sys.stderr)    
#    exit(-1)

#city_polygon_dir = sys.argv[1]
#x_split_size = float(sys.argv[2])
#y_split_size = float(sys.argv[3])
#points_split = int(sys.argv[4])
city_polygon_dir = './cities/'
x_split_size = 10
y_split_size = 10
points_split = 200000
listDir(city_polygon_dir,x_split_size,y_split_size,points_split)
data_write_csv('./polygon.csv',data_list)
