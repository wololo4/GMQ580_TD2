import sys,os
import math
sys.path.append(r'C:\OSGeo4W64\apps\Python37\Lib\site-packages')
os.environ['PATH'] = r'C:\OSGeo4W64\bin'
os.environ['GDAL_DATA'] = r'C:\OSGeo4W64\share\gdal'
os.environ['PROJ_LIB'] = r'C:\OSGeo4W64\share\proj'

from osgeo import ogr, osr
shpfile = r'C:\Users\Pierre-Antoine\Documents\École\Session 8 Géomatique\GMQ580\ADRESSE.shp'
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

def adresse_proche(valuex,valuey):

    layer.ResetReading()

    feature = layer.GetNextFeature()
    layer.SetSpatialFilterRect(valuex - 1000, valuey - 1000, valuex + 1000, valuey + 1000)
    distancemin = 8000
    valeurmin = 0
    m = []
    n = ''
    while feature:
        geometry = feature.GetGeometryRef()
        valeur = geometry.GetX(), geometry.GetY()
        distance = ((valeur[0] - valuex)**2 + (valeur[1] - valuey)**2)**0.5
        if distancemin > distance:
            geography = feature.GetGeometryRef()
            geography.Transform(transform)
            distancemin = distance
            valeurmin = valeur
            nociv = feature.GetField('TEXTE')
            rue = feature.GetField('SPECIFIQUE')
            geo = str(geography)
            n = distancemin, nociv, rue, geo
            m.append(n)
            n = ''
        feature = layer.GetNextFeature()

    return sorted(m)[0]

valuex = float(input('entree votre valeur en lon :'))
valuey = float(input('entree votre valeur en lat :'))

#valuex = 287000
#valuey = 5040000

point = ogr.Geometry(ogr.wkbPoint)
point.AddPoint(valuex, valuey)

adresse = adresse_proche(point.GetX(),point.GetY())

print (adresse)