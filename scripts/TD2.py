from osgeo import ogr, osr
shpfile = r'../data/geobase_mtl.shp'
driver = ogr.GetDriverByName('ESRI Shapefile')
datasource = driver.Open(shpfile)
layer = datasource.GetLayer(0)


feature = layer.GetNextFeature()

spatialReferenceSRC = osr.SpatialReference()
spatialReferenceSRC.ImportFromEPSG(2950)

spatialReferenceDEST = osr.SpatialReference()
spatialReferenceDEST.ImportFromEPSG(4326)

transform = osr.CoordinateTransformation(spatialReferenceSRC, spatialReferenceDEST)

invtransform = osr.CoordinateTransformation(spatialReferenceDEST, spatialReferenceSRC)


def coord_adresse(Rue, NoCivique):

    # Rue = 'Grenet'
    # NoCivique = '#12501'

    a = []
    b = ''
    feature = layer.GetNextFeature()

    while feature:
         if str(feature.GetField('SPECIFIQUE')).lower() == Rue.lower() and str(feature.GetField('TEXTE'))[1:] == NoCivique:
             geography = feature.GetGeometryRef()
             geography.Transform(transform)
             b = feature.GetField('SPECIFIQUE'), feature.GetField('TEXTE'), feature.GetField('ID_ADRESSE'), geography.ExportToWkt()
             a.append(b)
             b = ''
         feature = layer.GetNextFeature()

    return a

Rue = input('Entree le nom de rue :')
NoCivique = input('Entree le numero civique de la rue :')

#rue = grenet
#nocivique  = #12501

w = coord_adresse(Rue,NoCivique)

#print w

def distance_adresse(valuex,valuey):

    layer.ResetReading()

    feature = layer.GetNextFeature()
    layer.SetSpatialFilterRect(valuex - 1000, valuey - 1000, valuex + 1000, valuey + 1000)
    distancemin = 8000
    valeurmin = 0
    m = []
    n = ''
    while feature:
        valeur = feature.GetField('xcoord'), feature.GetField('ycoord')
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

point = ogr.Geometry(ogr.wkbPoint)
point.AddPoint(valuex, valuey)
point.Transform(invtransform)

#valuex = 287000
#valuey = 5040000

y = distance_adresse(point.GetX(),point.GetY())

print (30 * '-')
print ("   M A I N - M E N U")
print (30 * '-')
print ("1. Les coordonnee de l'adresse")
print ("2. L'adresse la plus proche")
print (30 * '-')


choice = input('Enter your choice [1-2] : ')


choice = int(choice)


if choice == 1:
        print (w)
elif choice == 2:
        print (y)
else:
        print ("Invalid number. Try again...")
