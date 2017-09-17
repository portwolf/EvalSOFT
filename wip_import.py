### Alle benoetigten Bibl. laden
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
l = 10.6 / 1000
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

### Einlesen der Messdaten (Spalte 0, 1, 2: X-Koord., WK-Kontur, Sch.Kontur
DFREAD = pd.read_excel(open('Profil12.xls', 'rb'), sheetname='Tabelle1')
DF = DFREAD.as_matrix()


### DELTA_RP berechnen. Einfederung einer Scheibe auf einer Rolle (Startwert für spätere Iteration?)
DELTA_RP = 2.66*(7**0.09) * (FWK*(1-0.3**2)/(2.08*10**5*10.6)**0.91)
DELTA_RP2=np.zeros((shape(DF)))
for c in range (len(DF)):
    for b in range(ndim(DF)):
        if  DF[c, 1] <= DELTA_RP:
            DELTA_RP2[c, b] = DF[c, b]
        else:
            DELTA_RP2[c, b] = 0
Q_I = np.zeros(len(DF))

### Berechnung der Tatsächlichen Kontaktlänge

### Einfederung nach van der Sandt (kleiner als nach Teutsch.. warum?)
DEL_K = (3.97*(FWK**(9/10))) / ((1*10**5)*((l*1000)**(8/10)))
DEL_K2 = np.zeros((shape(DF)))
### Berechnung des Profilabschnitts der tatsächlich in Kontakt mit mit Scheibe
### ist. Berechnung anhand von DEL_K (s.o.)
b = 0
c = 0
for c in range(len(DF)):
    for b in range(ndim(DF)):
        if  DF[c, 1] <= DEL_K:
            DEL_K2[c, b] = DF[c, b]

        else:
            DEL_K2[c, b] = 0

### Berechnen der allgemeinen Kontur eines WK's anhand Messpunkte (Spalte 1 in Profilschrieb)
i = 0
WK_PROFIL = np.zeros(999)
for i in range(len(DFREAD)):
    WK_PROFIL[i] = 3.85*10**(-3)*np.log10(1/(1-(2*DF[i, 0]/WKLEN)**2))

### Lin. Gl. Sys loesen und einzelne Scheibenkraefte berechnen
### Iteration von DELTA_RP (absenken der Einfederung Delta bis Integral der
### Kräfte der Scheiben der WK Einzelkraft entspricht

### DELTA_RP3 = linspace(max(DELTA_RP2), 0, num=1000)

### Ab hier neuer Code
''' Gewichtungsmatrix (reale Kontaktflaeche erzeugen und mit realen Abständen
fuellen'''
GEW_MTX = np.zeros((len(DEL_K2), len(DEL_K2)))
for i in range(len(DEL_K2)):
    for j in range(ndim(DEL_K2)):
        if DEL_K2[i, j] != NaN:
            GEW_MTX[i, j] = abs(j-i)*l
        else:
            GEW_MTX[i, j] = 0
GEW_MTX2 = np.zeros((len(DEL_K2), len(DEL_K2)))

### Initialisiere Gewichtungsfunktion Matrix
GFKT = np.zeros((len(DF), len(DF)))

### Gewichtungsfunktionmatrix füllen (Abstände berechnen, reale)
for i in range(len(DF)):

    for j in range(len(DF)):
        GFKT[i, j] = abs((DF[i, 0] - DF[j, 0]))

### Faktor K2 -> quelle: FVA bericht / diss / teutsch?
K2 = 1 / 0.92
### Anzahl der Scheiben in die der WK aufgeteilt wird
N = 1000

### Gewichtungsfunktionmatrix füllen (Abstände berechnen, reale)
GFKT2 = np.zeros((len(DF), len(DF)))
for i in range(len(DF)):
    if DEL_K2[i,1]!=0:
        for j in range(len(DF)):
            GFKT2[i, j] = abs(j-i)*l
### Gewichtungsfunktionmatrix für j=k und j!=k erzeugen
GFKT3 = np.zeros((len(DF), len(DF)))
for i in range(len(GFKT)):
    for j in range(len(GFKT)):
        if j != i:
            GFKT3[i, j] = (1/GFKT2[i, j])**K2
        else:
            GFKT3[i, j] = (4/l)**K2
### S_I berechnen (S_0 irrelevant, Axiallager). Aus Alternative Slicing Technique.. (Teutsch)
C_I = 3.17*(WKRAD)**0.08*((1-QKZ**2)/EMOD)
S_I = C_I**K2 / (1000*l/N)
GFKT4 = np.zeros((len(DF), len(DF)))
GFKT4 = (N/sum(GFKT3))*S_I*GFKT3

j = 0
while j < len(DELTA_RP2):
###    DELTA_RP2 = [DELTA_RP3[j]] * 999
    Q_I = np.linalg.solve(GFKT4[nonzero[GFKT4]], DELTA_RP2[nonzero(DELTA_RP2)])
    if np.trapz(Q_I)/FWK > 2:
        j += 200
    if np.trapz(Q_I)/FWK > 1.5:
        j += 50
    if np.trapz(Q_I)/FWK > 1.05:
        j += 10
    j += 1
    if np.trapz(Q_I)/FWK <= 1.01 and np.trapz(Q_I)/FWK >= 0.99:
        break
    print(np.trapz(Q_I)/FWK)
    if np.trapz(Q_I)/FWK < 0.9:
        break
### Berechnen der realen Flaechenpressung einer einzelnen Scheibe
SCH_PRESSUNG = Q_I/(2*B*(l/N))

### Graphen
f, AXES = plt.subplots(3, sharex=True)
AXES[0].plot(DF[:, 0], DF[:, 1], label='Gemessenes Profil')
AXES[0].plot(DF[:, 0], WK_PROFIL, label='Berechnetes WK Profil')
AXES[0].plot(DF[:, 0], DELTA_RP2[:, 1], label='Einfederung nach Teutsch')
AXES[0].plot(DF[:, 0], DEL_K2[:, 1], label='Einfederung nach v.d.Sandt')
AXES[0].set_ylabel('Verschleissprofil')
AXES[0].legend(bbox_to_anchor=(0.9, 1), loc=2, borderaxespad=0.)
AXES[0].grid()
AXES[1].plot(DF[:, 0], Q_I)
AXES[1].set_ylabel('Kraefte auf eine Scheibe')
plt.legend(bbox_to_anchor=(0.9, 1), loc=2, borderaxespad=0.)
AXES[1].grid()

AXES[2].plot(DF[:, 0], SCH_PRESSUNG)
AXES[2].set_ylabel('Pressung einer Scheibe')
plt.legend(bbox_to_anchor=(0.9, 1), loc=2, borderaxespad=0.)
AXES[2].grid()

f.savefig('foo.png')
show()
