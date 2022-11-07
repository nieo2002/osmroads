#coding:utf-8
from ghsl import ghsl_population_query

populations = ghsl_population_query(level2='济南市',level1='山东省',country='China')
print(populations)