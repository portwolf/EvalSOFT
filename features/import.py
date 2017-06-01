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

### Erzeuge Graphvorlage
style.use('ggplot')
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

### Definition verwendeter Konstanten
Emod = (2.08e+05)                                   ### EModul Lagerstahl
QKZ = 0.3                                           ### Querkontraktionszahl
WKrad = 11                                          ### Waelzkoerperdurchmesser
WKlen = 10.6                                        ### Waelzkoerperlaenge
rho = (1/(WKlen/2))                                 ### Konstante nach HERTZ
l = 10.6/1000
Fges = int(input('Gesamtlagerkraft? (In [kN]) '))   ### Lagergesamtlast
AnzWK = int(input('Anzahl der Waelzkoerper? '))     ### Anzahl der Waelzkoerper im Lager
Fwk = round(((Fges*1000)/AnzWK), 2)                 ### Last auf einzelnen WK
print ('Kraft pro Waelzkoerper in : '+str(Fwk)+' N')

### Berechne Kontaktbreite
b = round(math.sqrt((8*(1-QKZ**2)*Fwk*WKrad)/(pi*Emod*WKlen)), 4)
print('Die Kontaktbreite betraegt :'+str(b)+' mm')

### Berechne po (Maximalpressung)
p0 = round((2*Fwk)/(pi*b*WKlen), 2)
print('Die maximal Pressung im Kontakt betraegt: '+str(p0)+' N/mm^2')

### Initialisiere Gewichtungsfunktion Matrix
GFkt = np.zeros((1000, 1000))

### Schleife um GFkt zu fuellen
####i = 1#####
### Einlesen der Messdaten
df = pd.read_excel(open('Profil12.xls', 'rb'), sheetname='Tabelle1')
###print (df)

### Graphdefinitionen
plt.plot(df, df, 'r--', df, df**2, 'bs', df, df**3, 'g^')
## show()

