#Créer un buffer qui enregistre le couche qu'Elle superpose
import sys, os
import math
sys.path.append(r'C:\OSGeo4W64\apps\Python37\Lib\site-packages')
os.environ['PATH'] = r'C:\OSGeo4W64\bin'
os.environ['GDAL_DATA'] = r'C:\OSGeo4W64\share\gdal'
os.environ['PROJ_LIB'] = r'C:\OSGeo4W64\share\proj'

from osgeo import ogr, osr
shpfile = r'C:\Remi\Geo-info\td6\GMQ580_TD2\data\ADRESSE.shp'
driver = ogr.GetDriverByName('ESRI Shapefile')
datasource = driver.Open(shpfile)
layer = datasource.GetLayer(0)

feature = layer.GetNextFeature()

spatialReferenceSRC = osr.SpatialReference()
spatialReferenceSRC.ImportFromEPSG(32188)

spatialReferenceDEST = osr.SpatialReference()
spatialReferenceDEST.ImportFromEPSG(4326)

transform = osr.CoordinateTransformation(spatialReferenceSRC, spatialReferenceDEST)

invtransform = osr.CoordinateTransformation(spatialReferenceDEST, spatialReferenceSRC)


def createBuffer(inputfn, outputBufferfn, bufferDist):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    datasource = driver.Open(shpfile)
    layer = datasource.GetLayer(0)
    #inputds = ogr.Open(inputfn)
    #inputlyr = inputds.GetLayer()

    #shpdriver = ogr.GetDriverByName('ESRI Shapefile')
    if os.path.exists(outputBufferfn):
        driver.DeleteDataSource(outputBufferfn)
    outputBufferds = driver.CreateDataSource(outputBufferfn)
    bufferlyr = outputBufferds.CreateLayer(outputBufferfn, geom_type=ogr.wkbPolygon)
    featureDefn = bufferlyr.GetLayerDefn()

    for feature in layer:
         ingeom = feature.GetGeometryRef()
         geomBuffer = ingeom.Buffer(bufferDist)

         outFeature = ogr.Feature(featureDefn)
         outFeature.SetGeometry(geomBuffer)
         bufferlyr.CreateFeature(outFeature)
    outFeature = None

def main(inputfn, outputBufferfn, bufferDist):
    createBuffer(inputfn, outputBufferfn, bufferDist)

if __name__ == "__main__":
    inputfn = 'ADRESSE.shp'
    outputBufferfn = 'testBuffer.shp'
    bufferDist = 1000

    main(inputfn, outputBufferfn, bufferDist)