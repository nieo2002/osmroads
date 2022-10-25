#coding:utf-8
from osmroads import osm_road_distances

distances = osm_road_distances(level1='Gotland',country='Sweden')
print(distances)
