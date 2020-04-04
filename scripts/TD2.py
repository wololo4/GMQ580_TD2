import sys,os
import math
sys.path.append(r'C:\OSGeo4W64\apps\Python37\Lib\site-packages')
os.environ['PATH'] = r'C:\OSGeo4W64\bin'
os.environ['GDAL_DATA'] = r'C:\OSGeo4W64\share\gdal'
os.environ['PROJ_LIB'] = r'C:\OSGeo4W64\share\proj'

from osgeo import ogr, osr
#definition des couches
adresse_shp = r'C:\Users\Pierre-Antoine\Documents\École\Session 8 Géomatique\GMQ580\ADRESSE.shp'
quartier_shp = r'C:\Users\Pierre-Antoine\Documents\École\Session 8 Géomatique\GMQ580\quartiers.shp'
route_shp = r'C:\Users\Pierre-Antoine\Documents\École\Session 8 Géomatique\GMQ580\geobase_mtl.shp'

driver = ogr.GetDriverByName('ESRI Shapefile')
datasource_add = driver.Open(adresse_shp)
datasource_rou = driver.Open(route_shp)
datasource_qua = driver.Open(quartier_shp)

layer_add = datasource_add.GetLayer(0)
layer_rou = datasource_rou.GetLayer(0)
layer_qua = datasource_qua.GetLayer(0)

feature_add = layer_add.GetNextFeature()
feature_rou = layer_rou.GetNextFeature()
feature_qua = layer_qua.GetNextFeature()

#definition de la projection
spatialReferenceSRC = osr.SpatialReference()
spatialReferenceSRC.ImportFromEPSG(32188)

spatialReferenceDEST = osr.SpatialReference()
spatialReferenceDEST.ImportFromEPSG(4326)

transform = osr.CoordinateTransformation(spatialReferenceSRC, spatialReferenceDEST)

invtransform = osr.CoordinateTransformation(spatialReferenceDEST, spatialReferenceSRC)

#fonction qui retourne l'adresse la plus proche
def adresse_proche(valuex,valuey):

    layer_add.ResetReading()

    feature = layer_add.GetNextFeature()
    #filtre spatial pour diminuer le temps de calcul
    layer_add.SetSpatialFilterRect(valuex - 1000, valuey - 1000, valuex + 1000, valuey + 1000)
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
            distancemin = distance
            valeurmin = valeur
            nociv = feature.GetField('TEXTE')
            rue = feature.GetField('SPECIFIQUE')
            geo = str(geography)
            n = distancemin, nociv, rue, geo
            m.append(n)
            n = ''
        feature = layer_add.GetNextFeature()
    #retourne la distance, le numero civique, le nom de la rue et la geometrie
    return sorted(m)[0]

#fonction qui cree une zone tampon autour de l'incident
def createBuffer(point):

    bufferDist = 1000
    test = str(point)
    pt = ogr.CreateGeometryFromWkt(test)
    poly = pt.Buffer(bufferDist)
    #retourne la geometrie
    return poly

#fonction qui retourne le nombre de foyer affecté
def nombre_adresse():
    layer_add.ResetReading()

    feature = layer_add.GetNextFeature()
    m = []
    intersection = ''
    for feature in layer_add:
        geom_adr = feature.GetGeometryRef()
        tampon2 = ogr.CreateGeometryFromWkt(tampon)
        #intersection entre la zone tampon et la couche d'adresse
        if geom_adr.Intersect(tampon2):
            intersection = geom_adr.Intersection(tampon2)
            m.append(intersection)
            intersection = ''
    #retourne le nombre d'adresse dans la zone tampon
    return (len(m))

#fonction qui trouve les arteres dans la zone tampon
def nom_route():
    layer_rou.ResetReading()
    feature2 = layer_rou.GetNextFeature()
    r = []
    c = ''
    for feature2 in layer_rou:
        geom_rou = feature2.GetGeometryRef()
        tampon2 = ogr.CreateGeometryFromWkt(tampon)
        #intersection entre la couche des routes et de la zone tampon
        if geom_rou.Intersect(tampon2):
            att_nom = feature2.GetField('Nom_Voie')
            att_typevoie = feature2.GetField('Typ_Voie')
            c = att_typevoie, att_nom
            r.append(c)
            c =''
            feature2 = layer_rou.GetNextFeature()
    #retourne le type de route et son nom
    #cette operation est utile pour obtenir des valeurs unique de rue
    return (list(set(r)))

#fonction qui trouve les quartiers affecte et la populaton
def nom_quartier():
    layer_qua.ResetReading()
    feature = layer_qua.GetNextFeature()
    p = []
    q = ''
    y = []
    for feature1 in layer_qua:
        geom_qua = feature1.GetGeometryRef()
        tampon2 = ogr.CreateGeometryFromWkt(tampon)
        if geom_qua.Intersect(tampon2):
            att_pop = feature1.GetField('Population')
            att_quart = feature1.GetField('ARROND')
            p.append(att_quart)
            y.append(att_pop)
    #retourne le(s) nom(s) du quartier et la population totale de ces quartiers
    return (p, sum(y))

#coordonnees du point
valuex = float(input('entree votre valeur en lon :'))
valuey = float(input('entree votre valeur en lat :'))

#valuex = 287000
#valuey = 5040000

point = ogr.Geometry(ogr.wkbPoint)
point.AddPoint(valuex, valuey)

adresse = adresse_proche(point.GetX(),point.GetY())

tampon = str(createBuffer(point))

nombre = nombre_adresse()
nombre2 = nom_route()
nombre3 = nom_quartier()

print (adresse)
print (tampon)
print (nombre)
print (nombre2)
print (nombre3)