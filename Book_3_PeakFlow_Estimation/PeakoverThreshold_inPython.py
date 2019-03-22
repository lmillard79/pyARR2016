import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import sys
!{sys.executable} -m pip install lmoments3
import lmoments3 as lm
from lmoments3 import distr

import numpy as np
import os

%matplotlib inline

## Bring in the Peak over Threshold data 
POT_filt = pd.read_csv('PoT_Filtered_Mooloolah.csv',usecols=[0,2])
POT_filt['Date'] = pd.to_datetime(POT_filt['Date'])
POT_filt = POT_filt.set_index('Date')
records = POT_filt.shape[0]

W = POT_filt['Max'].values.max()
qo = POT_filt['Max'].values.min()

##  Display the data 
fig,(ax0,ax1) = plt.subplots(ncols=2,figsize=(12,5))

POT_filt.plot(marker='o',linewidth=0,ax=ax0)
ax0.set_ylabel('Flow')
ax0.set_title('Filtered Peaks to Threshold 15m$^3$/s\n %s peaks in 47 years of record'%records)
sns.distplot(POT_filt['Max'].values,ax=ax1,axlabel='Flow')
ax1.set_title('Distribution of Filtered Peaks')

## Some basic descriptors
years_of_record = (POT_filt.index[-1]-POT_filt.index[0]).days/365.
peaks_over_threshold = POT_filt['Max'].count()

# the v character
averagePOT = peaks_over_threshold/years_of_record

### Find the L Moments using Gen Pareto distribution (GPA)
data = POT_filt['Max'].values
paras = distr.gpa.lmom_fit(data)

print (paras)
print ('Peaks over threshold per year:'+str(round(averagePOT,3)))
print ('Flow data range:'+str(qo)+' - '+str(W))

arng = np.arange(qo,W,5)

EY = (1. - genpareto.cdf(arng,c=-1*paras['c'],scale=paras['scale'],loc=paras['loc']))/averagePOT

# Original values
quantiles = POT_filt['Max'].values

# Plotting position Eqn 3.2.79 finds AEP so second step converts back to EY
POT_filt['rank'] = POT_filt['Max'].rank(ascending=False)
POT_filt['T'] = (years_of_record + 0.2) / (POT_filt['rank']-0.4)
POT_filt['S'] = -1.*np.log(1-1./POT_filt['T'])
POT_filt['t'] = POT_filt['S']*100

#W = quantiles.max()

## Eqn 3.2.86 Log transformation plotting position   - Had to add =1.0 to get it to bisect the plotted data
EYs = np.exp(np.log(averagePOT)+(paras['loc']/paras['scale'])-(quantiles/paras['scale'])+1.0)
AEPs = (np.exp(EYs)-1.)/(np.exp(EYs))*100
np.round(AEPs,5)

fig,ax=plt.subplots(figsize=(14,8))

POT_filt.plot.scatter(x='t',y='Max',ax=ax,c='k',title='Mooloolah Gauge Partial Series - General Pareto distribution\nPeaks over Threshold')
ax.plot(AEPs,quantiles)

ax.axhline(85,c='r',alpha=0.5)
ax.axvline(35,c='r',alpha=0.5)

ax.semilogx()
ax.grid(True,zorder=0)
ax.grid(which='minor',axis='x',zorder=0)
ax.set_xlim(100,1)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x,pos:'%.0f%%'%x))
ax.set_xlabel('AEP')