#coding:utf-8
from osmroads import osm_road_distances

distances = osm_road_distances(level3='余杭区',level2='杭州市',level1='浙江省',country='China')
print(distances)

distances = osm_road_distances(level2='济宁市',level1='山东省',country='China')
print(distances)

distances = osm_road_distances(level1='山东省',country='China')
print(distances)
