
## Step 1
Pre-requirements:
下载GDAL-2.4.1.tar.gz(或以上版本)源代码，本地编译GDAL库。
GDAL下载地址： http://download.osgeo.org/gdal/2.4.1/gdal-2.4.1.tar.gz

使用PIP安装依赖python包
`pip install requirements.pip` 安装依赖

## Step 2
准备城市路网边界。
可以使用[阿里云提供的边界编辑器](http://datav.aliyun.com/portal/school/atlas/area_generator)，生成并下载对应城市的GeoJSON格式的城市边界文件。
注意：需要每个城市生成一个对应的GeoJSON文件。测试可参照test_cities目录下的城市。


## Step 3
使用poly_generator.py将下载的GeoJSON文件转换为csv格式，结果保存在polygon.csv里。

## Step 4
使用osm_roads.py，默认读取polygon.csv里的城市边界数据，生成每个城市的道路距离和道路数，结果存放在当前目录的result.csv里。结果的第二列表示道路总数，第三列表示总里程数（KM）
