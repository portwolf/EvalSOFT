''' Module for the AST Theory Calculations
'''
### Alle benoetigten Bibl. laden
### import math
### import pylab
import time
import pandas as pd
from pylab import show, legend, ylabel
import numpy as np
#import datetime
import matplotlib.pyplot as plt
from pylab import *
### from matplotlib import style
### from sklearn import datasets, linear_model
### import importlib
### Eigene "Module"
from constants import *
from dataImport import DF
ST = time.time()
### DELTA_RP berechnen. Einfederung einer Scheibe auf einer Rolle (Startwert für spätere Iteration?)
### (0.0259)
### "Gesamtannaeherung" nach van der Sandt (0.0136)
DEL_K = (3.97*(FWK**(9/10))) / ((1*10**5)*(WKLEN**(8/10)))
DELTA_RP2 = np.zeros((np.shape(DF)))
for c in range(len(DF)):
    for b in range(np.ndim(DF)):
        if  DF[c, 1] <= DELTA_RP:
            DELTA_RP2[c, b] = DF[c, b]
        else: DELTA_RP2[c, b] = 0
PT = round((time.time() - ST), 4)
print('DELTA_RP2 erzeugt in '+str(PT)+' sec')

Q_I = np.zeros(len(DF))

### Berechnung der Tatsächlichen Kontaktlänge
ST
### Einfederung nach van der Sandt (kleiner als nach Teutsch.. warum?)
DEL_K2 = np.zeros((np.shape(DF)))
### Berechnung des Profilabschnitts der tatsächlich in Kontakt mit mit Scheibe
### ist. Berechnung anhand von DEL_K (s.o.)
b = 0
c = 0
for c in range(len(DF)):
    for b in range(np.ndim(DF)):
        if  DF[c, 1] <= DEL_K:
            DEL_K2[c, b] = DF[c, b]

        else:
            DEL_K2[c, b] = 0
PT = round((time.time() - ST), 4)
print('DEL_K2 erzeugt in '+str(PT)+' sec')

###ST
### Berechnen der allgemeinen Kontur eines WK's anhand Messpunkte (Spalte 1 in Profilschrieb)
i = 0
WK_PROFIL = np.zeros(999)
for i in range(len(DF[:, 0])):
    WK_PROFIL[i] = 3.85*10**(-3)*np.log10(1/(1-(2*abs(DF[i, 0])/WKLEN)**2))
PT = round((time.time() - ST), 4)
print('WK_PROFIL erzeugt in '+str(PT)+' sec')


### Lin. Gl. Sys loesen und einzelne Scheibenkraefte berechnen
### Iteration von DELTA_RP (absenken der Einfederung Delta bis Integral der
### Kräfte der Scheiben der WK Einzelkraft entspricht

### DELTA_RP3 = linspace(max(DELTA_RP2), 0, num=1000)

### ### Ab hier neuer Code
### ''' Gewichtungsmatrix (reale Kontaktflaeche erzeugen und mit realen Abständen
### fuellen'''
### GEW_MTX = np.zeros((len(DEL_K2), np.ndim(DEL_K2)))
### for i in range(len(DEL_K2)):
###     for j in range(np.ndim(DEL_K2)):
###         if DEL_K2[i, j] != NaN:
###             GEW_MTX[i, j] = abs(j-i)*WKLEN
###         else:
###             GEW_MTX[i, j] = 0
### GEW_MTX2 = np.zeros((len(DEL_K2), len(DEL_K2)))


### Gewichtungsfunktionmatrix füllen (Abstände berechnen, reale)
ST
### Initialisiere Gewichtungsfunktion Matrix
GFKT = np.zeros((len(DF), len(DF)))
for i in range(len(DF)):

    for j in range(len(DF)):
        GFKT[i, j] = abs((DF[i, 0] - DF[j, 0]))

PT = round((time.time() - ST), 4)
print('GFKT erzeugt in '+str(PT)+' sec')

### Faktor K2 -> quelle: FVA bericht / diss / teutsch?
K2 = 1 / 0.92
### Anzahl der Scheiben in die der WK aufgeteilt wird
N = 100

ST
### Gewichtungsfunktionmatrix füllen (Abstände berechnen, reale)
GFKT2 = np.zeros((len(DF), len(DF)))
for i in range(len(DF)):
    for j in range(len(DF)):
        GFKT2[i, j] = abs(j-i)*(WKLEN/N)
PT = round((time.time() - ST), 4)
print('GFKT2 erzeugt in '+str(PT)+' sec')
###ST
### Gewichtungsfunktionmatrix für j=k und j!=k erzeugen
GFKT3 = np.zeros((len(DF), len(DF)))
for i in range(len(GFKT)):
    for j in range(len(GFKT)):
        if j != i:
            GFKT3[i, j] = (1/GFKT2[i, j])**K2
        else:
            GFKT3[i, j] = (4/(WKLEN/1000))**K2
PT = round((time.time() - ST), 4)
print('GFKT3 erzeugt in '+str(PT)+' sec')

### S_I berechnen (S_0 irrelevant, Axiallager). Aus Alternative Slicing Technique.. (Teutsch)
C_I = 3.17*(WKRAD)**0.08*((1-NUE_R**2)/E_R)**(1/K2)
S_I = C_I**K2 / (WKLEN/N)

###ST
GFKT4 = np.zeros((len(DF), len(DF)))
GFKT4 = (N/sum(GFKT3))*S_I*GFKT3

PT = round((time.time() - ST), 4)
print('GFKT4 erzeugt in '+str(PT)+' sec')

### DELTA_RP2 Vektor erzeugen. Berechnete einfederung linear bis 0 absenken
DEL_K3 = DEL_K - DF[:, 1]
DEL_K3[DEL_K3 < 0] = 0
Q_I = np.linalg.solve(GFKT4, (DEL_K3)**K2)
### Reale Kraft Q_I auf eine Scheibe berechnen
while np.trapz(Q_I)/FWK > 1.01:
    if np.trapz(Q_I)/FWK > 1.5:
        DEL_K3 = DEL_K3*0.8
        Q_I = np.linalg.solve(GFKT4, (DEL_K3)**K2)
    if np.trapz(Q_I)/FWK > 1.01:
        DEL_K3 = DEL_K3*0.9
        Q_I = np.linalg.solve(GFKT4, (DEL_K3)**K2)
        if np.trapz(Q_I)/FWK < 0.99:
            DEL_K3 = DEL_K3*1.1
            Q_I = np.linalg.solve(GFKT4, (DEL_K3)**K2)
    print(np.trapz(Q_I)/FWK)
### Berechnen der realen Flaechenpressung einer einzelnen Scheibe
SCH_PRESSUNG = 2*Q_I/(np.pi*B*(WKLEN/N))

### Graphen
f, AXES = plt.subplots(3, sharex=True)
AXES[0].plot(DF[:, 0], DF[:, 1], label='Gemessenes Profil')
AXES[0].plot(DF[:, 0], WK_PROFIL, label='Berechnetes WK Profil')
AXES[0].plot(DF[:, 0], DELTA_RP2[:, 1], label='Einfederung nach Teutsch')
AXES[0].plot(DF[:, 0], DEL_K2[:, 1], label='Einfederung nach v.d.Sandt')
AXES[0].set_ylabel('Verschleissprofil')
AXES[0].legend(bbox_to_anchor=(0.9, 1), loc=2, borderaxespad=0.)
AXES[0].grid()
AXES[1].plot(DF[:, 0], Q_I, label='Kraft auf eine inf. kleine Scheibe.')
AXES[1].set_ylabel('Kraefte auf eine Scheibe')
plt.legend(bbox_to_anchor=(0.9, 1), loc=2, borderaxespad=0.)
AXES[1].grid()

AXES[2].plot(DF[:, 0], SCH_PRESSUNG, label='Pressung einer inf. Scheibe')
AXES[2].set_ylabel('Pressung einer Scheibe')
plt.legend(bbox_to_anchor=(0.9, 1), loc=2, borderaxespad=0.)
AXES[2].grid()

f.savefig('foo.svg', type='svg')
show()
