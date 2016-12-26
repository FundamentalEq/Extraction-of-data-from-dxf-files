# for writing into a shape file
from osgeo import ogr

#for checking and deleting the file
import os

from sympy.geometry import *

def create_line(ls) :
    a,b = ls.points
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(float(a.x), float(a.y))
    line.AddPoint(float(b.x), float(b.y))
    return line

def MakeShapeFile(ArrayOfLineSegmets,name) :
    print "Going to create the impossible"
    driver = ogr.GetDriverByName('ESRI Shapefile')
    shapefile_name = name
    if os.path.exists(shapefile_name):
        os.remove(shapefile_name)
    out_data_source = driver.CreateDataSource(shapefile_name)

    # Create Layer

    out_layer = out_data_source.CreateLayer('center_line', geom_type=ogr.wkbLineString)

    # Set Geometry

    out_layer_defn = out_layer.GetLayerDefn()
    for i in range(len(ArrayOfLineSegmets)) :
        new_geom = create_line(ArrayOfLineSegmets[i])
        feature = ogr.Feature(out_layer_defn)
        feature.SetGeometry(new_geom)
        out_layer.CreateFeature(feature)
        feature.Destroy()

    out_data_source.Destroy()
def PrintLines(Array) :
    for i in range(len(Array)) :
        a,b = Array[i].points
        print i , float(a.x) ,float(a.y) ,float(b.x) ,float(b.y)
