import pandas as pd
import pylab
import numpy as np
import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
from matplotlib import style
style.use('ggplot')
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
df = pd.read_excel(open('Profil12.xls', 'rb'), sheetname='Tabelle1')
print (df.head)
Fges = input('Gesamtlagerkraft?')
AnzWK = input('Anzahl der Waelzkoerper?')



##x = [1, 2, 3, 4, 5]
##y = [1, 2, 3, 4, 5]
plt.plot(df, df, 'r--', df, df**2, 'bs', df, df**3, 'g^')
show()

