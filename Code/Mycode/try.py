from osgeo import ogr
driver = ogr.GetDriverByName('ESRI Shapefile')
datasource = driver.CreateDataSource('testlines.shp')
layer = datasource.CreateLayer('layerName',geom_type=ogr.wkbLineString)

myLine = ogr.Geometry(type=ogr.wkbLineString)
myLine.AddPoint_2D(0,0)
myLine.AddPoint_2D(10,0)
feature.SetGeometryDirectly(myLine)
layer.CreateFeature(feature)
