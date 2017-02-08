# for writing into a shape file
from osgeo import ogr

#for checking and deleting the file
import os

from LineSegment import *

def create_line(ls) :
    a,b = ls.points
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(float(a.x), float(a.y))
    line.AddPoint(float(b.x), float(b.y))
    return line

def MakeShapeFile(ArrayOfLineSegmets,name) :
    print "Going Genrate Shapefile ",name
    driver = ogr.GetDriverByName('ESRI Shapefile')
    shapefile_name = name
    if os.path.exists(shapefile_name):
        os.remove(shapefile_name)
    out_data_source = driver.CreateDataSource(shapefile_name)

    # Create Layer

    out_layer = out_data_source.CreateLayer('center_line', geom_type=ogr.wkbLineString)

    # for giving id to each line
    out_layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
    # Set Geometry
    out_layer_defn = out_layer.GetLayerDefn()
    for i in range(len(ArrayOfLineSegmets)) :
        new_geom = create_line(ArrayOfLineSegmets[i])
        feature = ogr.Feature(out_layer_defn)

        # for giving id to each line
        feature.SetField('id',i)

        feature.SetGeometry(new_geom)
        out_layer.CreateFeature(feature)
        feature.Destroy()

    out_data_source.Destroy()
def PrintLines(Array) :
    for i in range(len(Array)) :
        # if i == 4 or i == 5 :
            # print i , Array[i] , Array[i].slope
        a,b = Array[i].points
        print i , float(a.x) ,float(a.y) ,float(b.x) ,float(b.y)
