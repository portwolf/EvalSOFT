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
GFKT = np.zeros((1000, 1000))

### Schleife um GFKT zu fuellen
####i = 1#####

### Einlesen der Messdaten
DFREAD = pd.read_excel(open('Profil12.xls', 'rb'), sheetname='Tabelle1')
DF = DFREAD.as_matrix()

### Gewichtungsfunktionmatrix füllen (Abstände berechnen, reale)
for i in range(len(DF)):

    for j in range(len(DF)):
        GFKT[i, j] = abs((DF[i, 0] - DF[j, 0]))
###        print(GFKT[i,j])
###    print(i)

### Gewichtungsfunktionmatrix füllen (Abstände berechnen, reale)
GFKT2 = np.zeros((1000, 1000))
for i in range(len(DF)):

    for j in range(len(DF)):
        GFKT2[i, j] = abs(j-i)*l
###        print(GFKT[i,j])
###    print(i)

### Faktoren K1/K2 bestimmen
X0 = np.linspace(1e-10, 2e-4, num=1000)
Y0 = 2*X0*np.log10((np.e**(-1/(2*(1-0.3))))/X0)
N = 1000
LOG_K11 = (sum(np.log10(X0))*sum((np.log10(Y0))**2)-sum(np.log10(Y0))*sum(log10(X0)*np.log10(Y0)))
LOG_K12 = N*np.sum((log10(Y0))**2-(sum(log10(Y0)))**2)

LOG_K1 = LOG_K11/LOG_K12
K1 = 10**LOG_K1

LOG_K21 = (N*(sum(np.log10(X0))*sum((np.log10(Y0))))-sum(np.log10(Y0))*sum(log10(X0)))
K2 = LOG_K21/LOG_K12

### Gewichtungsfunktionmatrix für j=k und j!=k erzeugen
GFKT3 = np.zeros((1000, 1000))
for i in range(len(GFKT)):
    for j in range(len(GFKT)):
        if GFKT3[i, j] > 0:
            GFKT3[i, j] = (1/GFKT2[i, j])**K2
        elif GFKT3[i, j] < 0:
            GFKT3[i, j] = (1/GFKT2[i, j])**K2
        elif GFKT3[i, j] == 0:
            GFKT3[i, j] = (4/l)**K2

### Graphdefinitionen
plt.plot(DF, DF, 'r--', DF, DF**2, 'bs', DF, DF**3, 'g^')
## show()
