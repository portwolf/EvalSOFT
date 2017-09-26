''' This Module calculates the Constants neccessary for later on calculations.
    Modules calculated with Hertz'ian theory for a cylindrical Roller
'''
from math import pi
import math
import numpy as np
from dataImport import DF
### Definition verwendeter Konstanten
E_R = (2.08e+05)                                    ### EModul Roller
E_W = (2.08e+05)                                    ### EModul Washer
NUE_R = (1/3)                                       ### POISSON Ratio Roller
NUE_W = (1/3)                                       ### POISSON Ratio Roller
WKRAD = 11/2                                        ### Radius Roller
WARAD = 1*10**100                                   ### Radius Washer
T_W = 7.5                                         ### Washer Thickness
WKLEN = 10.6                                        ### Waelzkoerperlaenge
RHO = (1/(WKRAD))                                   ### Konstante nach HERTZ
L = 10.6                                            ### Roller length
N = 1000                                            ### Number of Slices/Roller
### FGES = int(input('Gesamtlagerkraft? (In [kN]) '))   ### Lagergesamtlast
FGES = 80   ### Lagergesamtlast

### ANZWK = int(input('Anzahl der Waelzkoerper? '))     ### Anzahl der Waelzkoerper im Lager
ANZWK = 15  ### Anzahl der Waelzkoerper im Lager

FWK = round(((FGES*1000)/ANZWK), 2)                 ### Last auf einzelnen WK
print('Kraft pro Waelzkoerper in : '+str(FWK)+' N')

### Einfederung nach Teutsch S. 46
DELTA_RP = 2.66*(7**0.09) * (FWK*(1-0.3**2)/(2.08*10**5*10.6)**0.91)



E_RED =	2*E_R*E_W*(1/((1-NUE_R**2)*E_W+(1-NUE_W**2)*E_R))
R_RED =	(1/WARAD + 1/WKRAD)

### Berechne Kontaktbreite
B = np.round(np.sqrt(8*FWK/(np.pi*E_RED*R_RED*L)), 4)
print('Die Kontaktbreite betraegt: '+str(B)+' mm')

### Berechne po (Maximalpressung)
P0 = round((2*FWK)/(pi*B*WKLEN), 2)
print('Die maximal Pressung im Kontakt betraegt: '+str(P0)+' N/mm^2')

#########	HERTZ line contact	######################################
#########	TEUTSCH page 149 and 150	##############################
# pylint: disable=E1103
DEL_1 = (2*FWK/(np.pi*L)) * (((1 - NUE_R**2)/E_R) * (np.log(2*WKRAD/B) - 1./2)
+ ((1. - NUE_W**2)/E_W) * (np.log(2*T_W/B) - NUE_W/2*(1 - NUE_W)))
        #	Gl. 7.7
# pylint: enable=E1103

DEL_1 = DEL_1 - DF[:,1]
DEL_1[DEL_1 < 0] = 0

Y0 = (DEL_1*(1 + 2*WKRAD/WARAD))/T_W                                            #   Gl. 7.12.1
X0 = (FWK*(1 + 2*WKRAD/WARAD))/(np.pi*E_RED*L*T_W)                              #   Gl. 7.12.1


### k1 = sum(np.log10(X0))
### k2 = sum(np.log10(Y0)**2)
### k3 = sum(np.log10(Y0))
### k4 = sum(np.log10(X0)*np.log10(Y0))
###
### LOG_K1 = (k1*k2 - k3*k4)/(N*k2 - k3**2)                              #	Gl. 7.16
### K1 = 10**LOG_K1						    #	Gl. 7.16
### K2 = (N*k4 - k3*k1)/(N*k2 - k3**2)				    #	Gl. 7.17
###
### print(K1, K2)
##############################################################################################################
#########	bearing dimension	###################################

z			=	15.				#	number of rollers		[-]
L			=	10.				#	length of roller		[mm]
d			=	11.				#	diameter of roller		[mm]
r			=	1.e100			#	curvature of washer 	[mm]
E_r			=	2.08e5			#	elastic modulus roller	[N/mm2]
E_w			=	2.08e5			#	elastic modulus washer	[N/mm2]
nue_r		=	1./3			#	POISSON ratio roller	[-]
nue_w		=	1./3			#	POISSON ratio washer	[-]
t_w			=	8.5				#	thickness of washer		[mm]
d_m			=	1.e100			#	mean radial diameter	[mm]

#########	loads	###############################################

Q			=	80.0e3			#	axial load				[N]
n			= 	7.5				#	speed					[rpm]
T			=	80.0			#	temperature				[K]
Q_z			= 	Q/z				#	load per roller 		[N]

#########	simulation parmaters	###############################

n			=	201
l			=	L/n
Q_r			=	np.linspace(0.1, 10e3, n)

###################################################################
''' This Module calculates the Constants necessary for later on calculations.
    Modules calculated with Hertz'ian theory for a cylindrical Roller
'''
