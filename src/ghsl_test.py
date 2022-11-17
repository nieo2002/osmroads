#coding:utf-8
from ghsl import ghsl_population_v2

populations = ghsl_population_v2('Weißpriach')
print(populations)

populations = ghsl_population(country='China',level1='山东省',level2='济南市',limit=1000)
print(populations)
