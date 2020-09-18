import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
try:
  import mplcyberpunk
except:
  !pip install mplcyberpunk
  clear_output()
  import mplcyberpunk


def intplot(Country1,Country2,Normalise,cases,globalpop):

  ccases1 = cases[cases.countriesAndTerritories == Country1]
  ccases2 = cases[cases.countriesAndTerritories == Country2]

  c1div = globalpop[globalpop.Location == Country1].PopTotal.mean()*1000
  c2div = globalpop[globalpop.Location == Country2].PopTotal.mean()*1000
  density1 = globalpop[globalpop.Location == Country1].PopDensity.mean()
  density2 = globalpop[globalpop.Location == Country2].PopDensity.mean()

  plt.style.use("cyberpunk")
  plt.figure(figsize=(12,8))
  ax1,ax2 = plt.subplot(221),plt.subplot(223)
  ax3,ax4 = plt.subplot(222), plt.subplot(224)

  if Normalise:
    caseno1 = ccases1.cases.values*100000/c1div
    deathno1 = ccases1.deaths.values*100000/c1div
    caseno2 = ccases2.cases.values*100000/c1div
    deathno2 = ccases2.deaths.values*100000/c1div
    labels = 'Per 100k'
  else:
    caseno1 = ccases1.cases.values
    deathno1 = ccases1.deaths.values
    caseno2 = ccases2.cases.values
    deathno2 = ccases2.deaths.values
    labels = 'Total'

  ax1.plot(ccases1.index,caseno1,label=labels)
  ax2.plot(ccases1.index,deathno1,label=labels)
  ax3.plot(ccases2.index,caseno2,label=labels)
  ax4.plot(ccases2.index,deathno2,label=labels)

  [i.set_ylim(0,max([max(caseno1),max(caseno2)])) for i in [ax1,ax3]]
  [i.set_ylim(0,max([max(deathno1),max(deathno2)])) for i in [ax2,ax4]]

  ax1.set_title('{}: Daily Cases ({}) \nPop. Dens.: {} $km^{}$'.format(Country1,labels,int(density1),-2))
  ax2.set_title('{}: Daily Deaths ({}) \nPop. Dens.: {} $km^{}$'.format(Country1,labels,int(density1),-2))
  ax3.set_title('{}: Daily Cases ({}) \nPop. Dens.: {} $km^{}$'.format(Country2,labels,int(density2),-2))
  ax4.set_title('{}: Daily Deaths ({}) \nPop. Dens.: {} $km^{}$'.format(Country2,labels,int(density2),-2))

  dateticks = [str(i)[:10] for i in ccases1.index[::15]]
  [i.set_xticks(ccases1.index[::15]) for i in [ax1,ax2,ax3,ax4]]
  [i.set_xticklabels(dateticks,rotation=90) for i in [ax1,ax2,ax3,ax4]]


  plt.tight_layout()
  plt.show()
