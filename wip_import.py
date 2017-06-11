### Alle benoetigten Bibl. laden
import math
import pandas as pd
import pylab
import numpy as np
import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
from matplotlib import style
from sklearn import datasets, linear_model
### Erzeuge Graphvorlage
style.use('ggplot')
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

### Definition verwendeter Konstanten
EMOD = (2.08e+05)                                   ### EModul Lagerstahl
QKZ = 0.3                                           ### Querkontraktionszahl
WKRAD = 11/2                                        ### Waelzkoerperdurchmesser
WKLEN = 10.6                                        ### Waelzkoerperlaenge
RHO = (1/(WKRAD))                                   ### Konstante nach HERTZ
l = 10.6/1000
FGES = int(input('Gesamtlagerkraft? (In [kN]) '))   ### Lagergesamtlast
ANZWK = int(input('Anzahl der Waelzkoerper? '))     ### Anzahl der Waelzkoerper im Lager
FWK = round(((FGES*1000)/ANZWK), 2)                 ### Last auf einzelnen WK
print('Kraft pro Waelzkoerper in : '+str(FWK)+' N')

### Berechne Kontaktbreite
#b = round(math.sqrt((8*(1-QKZ**2)*FWK*2*WKRAD)/(pi*EMOD*WKLEN)), 4)
B = round(math.sqrt((8*(1-QKZ**2)*FWK*WKRAD)/(pi*EMOD*WKLEN)), 4)
print('Die Kontaktbreite betraegt: '+str(B)+' mm')

### Berechne po (Maximalpressung)
P0 = round((2*FWK)/(pi*B*WKLEN), 2)
print('Die maximal Pressung im Kontakt betraegt: '+str(P0)+' N/mm^2')

### Initialisiere Gewichtungsfunktion Matrix
GFkt = np.zeros((1000, 1000))

### Schleife um GFkt zu fuellen
####i = 1#####

### Einlesen der Messdaten
DFREAD = pd.read_excel(open('Profil12.xls', 'rb'), sheetname='Tabelle1')
DF = DFREAD.as_matrix()

###print (DF)
for i in range(len(DF)):

    for j in range(len(DF)):
        GFkt[i, j] = abs((DF[i, 0] - DF[j, 0]))
###        print(GFkt[i,j])
###    print(i)

### Graphdefinitionen
plt.plot(DF, DF, 'r--', DF, DF**2, 'bs', DF, DF**3, 'g^')
## show()
