### Alle benoetigten Bibl. laden
import math
import pandas as pd
### import pylab
from pylab import figure, show, legend, ylabel
import numpy as np
#import datetime
#import pandas_datareader.data as web
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
from pylab import *
from matplotlib import style
from sklearn import datasets, linear_model
### Erzeuge Graphvorlage
##style.use('ggplot')
##FIGURE = plt.figure()
##AX = FIGURE.add_subplot(111, projection='3d')

### Definition verwendeter Konstanten
EMOD = (2.08e+05)                                   ### EModul Lagerstahl
QKZ = 0.3                                           ### Querkontraktionszahl
WKRAD = 11/2                                        ### Waelzkoerperdurchmesser
WKLEN = 10.6                                        ### Waelzkoerperlaenge
RHO = (1/(WKRAD))                                   ### Konstante nach HERTZ
###l = 10.6/1000
l = 10.6
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
GFKT = np.zeros((999, 999))

### Einlesen der Messdaten
DFREAD = pd.read_excel(open('Profil12.xls', 'rb'), sheetname='Tabelle1')
DF = DFREAD.as_matrix()

### Gewichtungsfunktionmatrix füllen (Abstände berechnen, reale)
for i in range(len(DF)):

    for j in range(len(DF)):
        GFKT[i, j] = abs((DF[i, 0] - DF[j, 0]))
###        print(GFKT[i, j])
###    print(i)

### Gewichtungsfunktionmatrix füllen (Abstände berechnen, reale)
GFKT2 = np.zeros((999, 999))
for i in range(len(DF)):

    for j in range(len(DF)):
        GFKT2[i, j] = abs(j-i)*l
###        print(GFKT[i, j])
###    print(i)

###### Faktoren K1/K2 bestimmen
###X0 = np.linspace(1e-10, 2e-4, num=1000)
#### pylint: disable=no-name-in-module
###Y0 = 2*X0*np.log10((np.e**(-1/(2*(1-0.3))))/X0)
#### pylint: enable=no-name-in-module
###N = 1000
###LOG_K11 = (sum(np.log10(X0))*sum((np.log10(Y0))**2)-sum(np.log10(Y0))*sum(log10(X0)*np.log10(Y0)))
###LOG_K12 = N*np.sum((log10(Y0))**2-(sum(log10(Y0)))**2)
###
###LOG_K1 = LOG_K11/LOG_K12
###K1 = 10**LOG_K1
###
###LOG_K21 = (N*(sum(np.log10(X0))*sum((np.log10(Y0))))-sum(np.log10(Y0))*sum(log10(X0)))
###K2 = LOG_K21/LOG_K12
K2 = 1 / 0.92
N = 1000
### Gewichtungsfunktionmatrix für j=k und j!=k erzeugen
GFKT3 = np.zeros((999, 999))
for i in range(len(GFKT)):
    for j in range(len(GFKT)):
        if j != i:
#        if GFKT2[i, j] > 0:
            GFKT3[i, j] = (1/GFKT2[i, j])**K2
#        elif GFKT2[i, j] == 0:
#        elif j == i:
        else:
            GFKT3[i, j] = (4/l)**K2

### S_I berechnen (S_0 irrelevant, Axiallager). Aus Alternative Slicing Technique.. (Teutsch)
C_I = 3.17*(WKRAD)**0.08*((1-QKZ**2)/EMOD)
S_I = C_I**K2 / (l/N)
GFKT4 = np.zeros((999, 999))
GFKT4 = (N/sum(GFKT3))*S_I*GFKT3

### DELTA_RP berechnen. Einfederung einer Rolle auf einer Scheibe (Startwert für spätere Iteration?)
DELTA_RP = 2.66*(7**0.09) * (FWK*(1-0.3**2)/(2.08*10**5*10.6)**0.91)
DELTA_RP2 = [DELTA_RP] * 999
Q_I = np.zeros(999)
### Lin. Gl. Sys loesen und einzelne Scheibenkraefte berechnen
### Iteration von DELTA_RP (absenken der Einfederung Delta bis Integral der Kräfte der Scheiben der WK Einzelkraft entspricht

DELTA_RP3 = linspace(max(DELTA_RP2), 0, num=1000)
### for j in DELTA_RP3:
###     DELTA_RP2 = [j] * 999
###     print(np.trapz(Q_I)/FWK)
###     if np.trapz(Q_I)/FWK >= 3:
###         j+=10
###         print(j)
###     Q_I = np.linalg.solve(GFKT4, DELTA_RP2)
###     if np.trapz(Q_I)/FWK <= 1.01 and np.trapz(Q_I)/FWK >= 0.99:
###         break

### While loop variante?
### for j in range(len(DELTA_RP3)):
###     DELTA_RP2 = [DELTA_RP3[j]] * 999
###     Q_I = np.linalg.solve(GFKT4, DELTA_RP2)
###     if np.trapz(Q_I)/FWK > 2:
###         j+=50
j=0
while j < len(DELTA_RP3):
    DELTA_RP2=[DELTA_RP3[j]] * 999
    Q_I = np.linalg.solve(GFKT4, DELTA_RP2)
    if np.trapz(Q_I)/FWK > 2:
        j+=100
    if np.trapz(Q_I)/FWK > 1.5:
        j+=5
    if np.trapz(Q_I)/FWK > 1.05:
        j+=1
    j+=1
    if np.trapz(Q_I)/FWK <= 1.01 and np.trapz(Q_I)/FWK >= 0.99:
        break
    print(np.trapz(Q_I)/FWK)
### Berechnen der realen Flaechenpressung einer einzelnen Scheibe
SCH_PRESSUNG = Q_I/(2*B*(l/N))
### Graphen
### f= plt.figure()
f, axes = plt.subplots(3, 1)
axes[0].plot(DF[:,0], DF[:, 1])
axes[0].set_ylabel('Verschleissprofil')
axes[0].grid()
axes[1].plot(DF[:, 0], Q_I)
axes[1].set_ylabel('Kraefte einer Scheibe')
axes[1].grid()

axes[2].plot(DF[:,0], SCH_PRESSUNG)
axes[2].set_ylabel('Pressung einer Scheibe')
axes[2].grid()
### ax1 = FIGURE.add_subplot(111)
### line1 = ax1.plot(Q_I, 'xr-', DF[:, 1], 'r--')
### ylabel("Kraft auf eine Scheibe")
### ax2 = FIGURE.add_subplot(111, share=ax1)
### line2 = ax2.plot(SCH_PRESSUNG, 'g--')
### ax2.yaxis.tick_right()
### ax2.yaxis.set_label_position("right")
### ylabel("Flaechenpressung einer Scheibe")
### legend((line1, line2), ("Kraft / Verschleiss", "Flaechenpressung"))
show()
