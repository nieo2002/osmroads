
## Step 1
Pre-requirements:
下载GDAL-2.4.1.tar.gz(或以上版本)源代码，本地编译GDAL库。
GDAL下载地址： http://download.osgeo.org/gdal/2.4.1/gdal-2.4.1.tar.gz

使用PIP安装依赖python包
`pip install requirements.pip` 安装依赖

## Step 2
使用osm_test.py启动一个测试，可以查看'Hefa'市的路网里程数
osm_road_distances函数使用说明：目前支持的城市、地区和国家名称，遵循GADM标准。
