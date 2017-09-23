''' This Module is for file import / RAW Data import
'''
import time
import pandas as pd
ST = time.time()
### Einlesen der Messdaten (Spalte 0, 1, 2: X-Koord., WK-Kontur, Sch.Kontur
DFREAD = pd.read_excel(open('Profil12.xls', 'rb'), sheetname='Tabelle1')
DF = DFREAD.as_matrix()
PT = round((time.time() - ST), 4)
print('DFREAD erzeugt in '+str(PT)+'  sec')
