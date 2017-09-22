''' This Module calculates the Constants neccessary for later on calculations.
    Modules calculated with Hertz'ian theory for a cylindrical Roller
'''
from math import pi
import math
### Definition verwendeter Konstanten
EMOD = (2.08e+05)                                   ### EModul Lagerstahl
QKZ = 0.3                                           ### Querkontraktionszahl
WKRAD = 11/2                                        ### Waelzkoerperdurchmesser
WKLEN = 10.6                                        ### Waelzkoerperlaenge
RHO = (1/(WKRAD))                                   ### Konstante nach HERTZ
L = 10.6
### FGES = int(input('Gesamtlagerkraft? (In [kN]) '))   ### Lagergesamtlast
FGES = 80   ### Lagergesamtlast
### ANZWK = int(input('Anzahl der Waelzkoerper? '))     ### Anzahl der Waelzkoerper im Lager
ANZWK = 15  ### Anzahl der Waelzkoerper im Lager
FWK = round(((FGES*1000)/ANZWK), 2)                 ### Last auf einzelnen WK
print('Kraft pro Waelzkoerper in : '+str(FWK)+' N')

### Berechne Kontaktbreite
B = round(math.sqrt((8*(1-QKZ**2)*FWK*WKRAD)/(pi*EMOD*WKLEN)), 4)
print('Die Kontaktbreite betraegt: '+str(B)+' mm')

### Berechne po (Maximalpressung)
P0 = round((2*FWK)/(pi*B*WKLEN), 2)
print('Die maximal Pressung im Kontakt betraegt: '+str(P0)+' N/mm^2')
''' This Module calculates the Constants neccessary for later on calculations.
    Modules calculated with Hertz'ian theory for a cylindrical Roller
'''
