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

X0=np.linspace(1e-10, 2e-4, num=1000)
Y0 = 2*X0*np.log10((np.e**(-1/(2*(1-0.3))))/X0)
n=1000
LOG_K11=(sum(np.log10(X0))*sum((np.log10(Y0))**2)-sum(np.log10(Y0))*sum(log10(X0)*np.log10(Y0)))
LOG_K12=n*np.sum((log10(Y0))**2-(sum(log10(Y0)))**2)

LOG_K1=LOG_K11/LOG_K12
K1=10**LOG_K1

LOG_K21=(n*(sum(np.log10(X0))*sum((np.log10(Y0))))-sum(np.log10(Y0))*sum(log10(X0)))
K2=LOG_K21/LOG_K12

