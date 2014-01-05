import csv
from barcode.views import *
b = open('media/barcode.csv','w')
a = csv.writer(b)
data = []
for barcode in Barcode.objects.all():
    data.append([barcode.barcode,'<---Barcode::SHID---->',barcode.shaastra_id])
a.writerows(data)
b.close()
