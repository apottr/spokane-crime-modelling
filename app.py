from pathlib import Path
from osgeo import ogr
from osgeo import osr
from download_dataset import exec_dl
import os

data_dir = Path(__file__).parent.resolve() / "data" #pylint:disable=no-member

def init_layer(fname):
    shapefile = str(data_dir / fname)
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataSource = driver.Open(shapefile, 0)
    layer = dataSource.GetLayer()
    return layer

srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

def process_layer(layer):
    trs = layer.GetSpatialRef()
    trn = osr.CoordinateTransformation(trs,srs)
    for feature in layer:
        geom = feature.GetGeometryRef()
        pt = geom.Centroid()
        pt.Transform(trn)
        print(pt.ExportToWkt())
    layer.ResetReading()

if __name__ == "__main__":
    exec_dl()
    print("finished downloading shapefiles")
    l = init_layer("Crime_2013.shp")
    print("initialized layer")
    process_layer(l)
