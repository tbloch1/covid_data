import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import mplcyberpunk


def intplot(Country1,Country2,Normalise,cases,globalpop):

  ccases1 = cases[cases.countriesAndTerritories == Country1]
  ccases2 = cases[cases.countriesAndTerritories == Country2]

  c1div = globalpop[globalpop.Location == Country1].PopTotal.mean()*1000
  c2div = globalpop[globalpop.Location == Country2].PopTotal.mean()*1000
  density1 = globalpop[globalpop.Location == Country1].PopDensity.mean()
  density2 = globalpop[globalpop.Location == Country2].PopDensity.mean()

  plt.style.use("cyberpunk")
  plt.figure(figsize=(12,8),dpi=300)
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

  
def localeplot(Locale, coords, death, populations, ukcounties):
  plt.style.use("cyberpunk")
  plt.figure(figsize=(12,4.5),dpi=300)
  gs = gridspec.GridSpec(1,3)
  ax1 = plt.subplot(gs[0,0])
  ax2 = plt.subplot(gs[0,1:])

  ukcounties.plot(ax=ax1,color='w')
  ax1.scatter(coords.long.values, coords.lat.values,s=1,c='#08F7FE')

  ax1.scatter(coords[coords['lad17nm'] == Locale].long.values,
              coords[coords['lad17nm'] == Locale].lat.values,
              s=6,c='#FE53BB')
  
  areacode = coords[coords['lad17nm'] == Locale]['lad17cd'].values[0]
  
  death_area = death[(death['Cause of death'] == 'COVID 19') &
                     (death['Area code'] == areacode)]
  death_area_i = death[(death['Cause of death'] == 'COVID 19') &
                       (death['Area code'] != areacode)]

  death_day = [death_area.loc[i]['Number of deaths'].astype('float32').sum() for i in death_area.index.unique()]
  death_day_i = [death_area_i.loc[i]['Number of deaths'].astype('float32').sum() for i in death_area.index.unique()]
  death_day, death_day_i = np.array(death_day), np.array(death_day_i)
  
  popsize = populations[populations.Name == Locale]['All ages'].astype('float64').values[0]
  totsize = np.nanmax(populations['All ages'].astype('float64').values)-popsize
  
  ax2.plot(death_area.index.unique(),death_day*100000/popsize,c='#FE53BB',label='{} (Pop. {})'.format(Locale,popsize))
  ax2.plot(death_area.index.unique(),death_day_i*100000/totsize,c='#08F7FE',label='Rest of UK')
  
  ax2.legend()
  ax1.set_xticklabels([])
  ax1.set_yticklabels([])
  ax2.set_ylabel("Death's per 100k")
  ax2.set_xticks(np.sort(death_area.index.unique())[::5])
  ax2.set_xticklabels([str(i)[:10] for i in np.sort(death_area.index.unique())[::5]],rotation=90)
  plt.plot()
