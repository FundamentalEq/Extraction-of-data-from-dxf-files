# Python library to interact with dxf files
import ezdxf
#Python library for geometry and mathematical computations
import sympy
import sympy.geometry

# for writing into a shape file
from osgeo import ogr

#for checking and deleting the file
import os

from LineGeometry import *
from GlobalValues import *
from GenCenterLine import *

def create_line(ls) :
    a,b = ls.points
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(float(a.x), float(a.y))
    line.AddPoint(float(b.x), float(b.y))
    return line
def main() :
    dwg = ezdxf.readfile("1RoomWSS.dxf")
    modelspace = dwg.modelspace()
    # Extarction of lines-segments from the dxf file and storing them as
    # sympy.geometry.Segment for further computation
    ElineSegments = []
    for l in modelspace.query('LINE') :
        x1,y1,z1 = l.dxf.start
        x2,y2,z2 = l.dxf.end
        ElineSegments.append(Segment(Point(x1,y1),Point(x2,y2)))

    print ElineSegments

    print "Going to create the impossible"
    driver = ogr.GetDriverByName('ESRI Shapefile')
    shapefile_name = 'plzz.shp'
    if os.path.exists(shapefile_name):
        os.remove(shapefile_name)
    out_data_source = driver.CreateDataSource(shapefile_name)

    # Create Layer

    out_layer = out_data_source.CreateLayer('center_line', geom_type=ogr.wkbLineString)

    # Set Geometry

    out_layer_defn = out_layer.GetLayerDefn()
    for i in range(len(ElineSegments)) :
        new_geom = create_line(ElineSegments[i])
        feature = ogr.Feature(out_layer_defn)
        feature.SetGeometry(new_geom)
        out_layer.CreateFeature(feature)
        feature.Destroy()

    out_data_source.Destroy()
main()
