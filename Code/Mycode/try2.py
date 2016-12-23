import osgeo.ogr, osgeo.osr

def create_line(points):
    """

    :param points: array of points
    :return: geometry of line
    """
    line = ogr.Geometry(ogr.wkbLineString)

    for pt in points:
        line.AddPoint(float(pt[0]), float(pt[1]))
    return line

driver = ogr.GetDriverByName('ESRI Shapefile')

    shapefile_name = 'i_will_make_u.shp'
    if os.path.exists(shapefile_name):
        os.remove(shapefile_name)

    out_data_source = driver.CreateDataSource(shapefile_name)

    # Create Layer

    out_layer = out_data_source.CreateLayer('center_line', geom_type=ogr.wkbLineString)

    # Set Geometry

    out_layer_defn = out_layer.GetLayerDefn()


                new_geom = create_line(cline_info[1])
                        feature = ogr.Feature(out_layer_defn)
                        feature.SetGeometry(new_geom)
                        out_layer.CreateFeature(feature)
                        feature.Destroy()


    out_data_source.Destroy()
