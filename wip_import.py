### Alle benoetigten Bibl. laden
import threading
import math
import pylab
import pandas as pd
from pylab import figure, show, legend, ylabel
import numpy as np
#import datetime
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
from pylab import *
from matplotlib import style
from sklearn import datasets, linear_model

### Definition verwendeter Konstanten
EMOD = (2.08e+05)                                   ### EModul Lagerstahl
QKZ = 0.3                                           ### Querkontraktionszahl
WKRAD = 11/2                                        ### Waelzkoerperdurchmesser
WKLEN = 10.6                                        ### Waelzkoerperlaenge
RHO = (1/(WKRAD))                                   ### Konstante nach HERTZ
l = 10.6
FGES = int(input('Gesamtlagerkraft? (In [kN]) '))   ### Lagergesamtlast
ANZWK = int(input('Anzahl der Waelzkoerper? '))     ### Anzahl der Waelzkoerper im Lager
FWK = round(((FGES*1000)/ANZWK), 2)                 ### Last auf einzelnen WK
print('Kraft pro Waelzkoerper in : '+str(FWK)+' N')

### Berechne Kontaktbreite
B = round(math.sqrt((8*(1-QKZ**2)*FWK*WKRAD)/(pi*EMOD*WKLEN)), 4)
print('Die Kontaktbreite betraegt: '+str(B)+' mm')

### Berechne po (Maximalpressung)
P0 = round((2*FWK)/(pi*B*WKLEN), 2)
print('Die maximal Pressung im Kontakt betraegt: '+str(P0)+' N/mm^2')

### Initialisiere Gewichtungsfunktion Matrix
GFKT = np.zeros((999, 999))

### Einlesen der Messdaten
DFREAD = pd.read_excel(open('Profil12.xls', 'rb'), sheetname='Tabelle1')
DF = DFREAD.as_matrix()

### Gewichtungsfunktionmatrix füllen (Abstände berechnen, reale)
for i in range(len(DF)):

    for j in range(len(DF)):
        GFKT[i, j] = abs((DF[i, 0] - DF[j, 0]))

### Gewichtungsfunktionmatrix füllen (Abstände berechnen, reale)
GFKT2 = np.zeros((999, 999))
for i in range(len(DF)):

    for j in range(len(DF)):
        GFKT2[i, j] = abs(j-i)*l

K2 = 1 / 0.92
### Anzahl der Scheiben in die der WK aufgeteilt wird
N = 90

### Gewichtungsfunktionmatrix für j=k und j!=k erzeugen
GFKT3 = np.zeros((999, 999))
for i in range(len(GFKT)):
    for j in range(len(GFKT)):
        if j != i:
            GFKT3[i, j] = (1/GFKT2[i, j])**K2
        else:
            GFKT3[i, j] = (4/l)**K2

### S_I berechnen (S_0 irrelevant, Axiallager). Aus Alternative Slicing Technique.. (Teutsch)
C_I = 3.17*(WKRAD)**0.08*((1-QKZ**2)/EMOD)
S_I = C_I**K2 / (l/N)
GFKT4 = np.zeros((999, 999))
GFKT4 = (N/sum(GFKT3))*S_I*GFKT3

### DELTA_RP berechnen. Einfederung einer Scheibe auf einer Rolle (Startwert für spätere Iteration?)
DELTA_RP = 2.66*(7**0.09) * (FWK*(1-0.3**2)/(2.08*10**5*10.6)**0.91)
DELTA_RP2 = [DELTA_RP] * 999
Q_I = np.zeros(999)

### Berechnung der Tatsächlichen Kontaktlänge

### Einfederung nach van der Sandt (kleiner als nach Teutsch.. warum?)
DEL_K = (3.97*(FWK**(9/10))) / ((1*10**5)*(l**(8/10)))
DEL_K2 = np.zeros((999, 1))
### Berechnung des Profilabschnitts der tatsächlich in Kontakt mit mit Scheibe
### ist. Berechnung anhand von DEL_K (s.o.)
for c in range(len(DF)):
    if  DF[c, 1] <= DELTA_RP:
        DEL_K2[c] = DF[c, 1]

    else:
        DEL_K2[c] = NaN

### Berechnen der allgemeinen Kontur eines WK's anhand Messpunkte (Spalte 1 in Profilschrieb)
i = 0
WK_PROFIL = np.zeros(999)
for i in range(len(DFREAD)):
    WK_PROFIL[i] = 3.85*10**(-3)*np.log10(1/(1-(2*DF[i, 0]/WKLEN)**2))
    print(WK_PROFIL[i])

### Lin. Gl. Sys loesen und einzelne Scheibenkraefte berechnen
### Iteration von DELTA_RP (absenken der Einfederung Delta bis Integral der
### Kräfte der Scheiben der WK Einzelkraft entspricht

DELTA_RP3 = linspace(max(DELTA_RP2), 0, num=1000)

j = 0
while j < len(DELTA_RP3):
    DELTA_RP2 = [DELTA_RP3[j]] * 999
    Q_I = np.linalg.solve(GFKT4, DELTA_RP2)
    if np.trapz(Q_I)/FWK > 2:
        j += 100
    if np.trapz(Q_I)/FWK > 1.5:
        j += 5
    if np.trapz(Q_I)/FWK > 1.05:
        j += 1
    j += 1
    if np.trapz(Q_I)/FWK <= 1.01 and np.trapz(Q_I)/FWK >= 0.99:
        break
    print(np.trapz(Q_I)/FWK)
### Berechnen der realen Flaechenpressung einer einzelnen Scheibe
SCH_PRESSUNG = Q_I/(2*B*(l/N))
### Graphen
f, axes = plt.subplots(3, 1, sharex=True)
axes[0].plot(DF[:, 0], DF[:, 1],
        DF[:, 0], WK_PROFIL,
        DF[:, 0], DELTA_RP2,
        DF[:,0], DEL_K2)
axes[0].set_ylabel('Verschleissprofil')
axes[0].grid()
axes[1].plot(DF[:, 0], Q_I)
axes[1].set_ylabel('Kraefte einer Scheibe')
axes[1].grid()

axes[2].plot(DF[:, 0], SCH_PRESSUNG)
axes[2].set_ylabel('Pressung einer Scheibe')
axes[2].grid()
f.savefig('foo.png')
show()
