##################################################
#
#  This code takes all of the URBS .csv files and collates it into a sorted list of timeseries
#  for use in GoldSim or Tuflow/Estry models 
#  Other analysis for ARR2016 is possible to calculate medians and plotting - this can be added to post-processing
#  - 12 February 2019 
#
####################################################

import csv
import os
import pandas as pd

# ----------- INITIALISE ---------------
urbsPath = r'W:\Hydrology\dams\ewen_maddock\urbs\2018_Study\99. Report\_FloodDataFiles_Existing/'
csvlst = []

files = os.listdir(urbsPath)
for f in files:        
    if f.endswith('.csv'):
        fin = urbsPath+f
        csvlst.append(fin)

outpath = r'W:\Hydraulics\2_NorthCoast\EwenMaddock_FIA_2018\Routing_Calculator\URBS/'

# --------------------------------------
dfALL_URBS = pd.DataFrame()

for csvin in csvlst[0:35]:
    f = csvin.split('/')[-1][:-4] 
    
    with open(csvin,'r') as f1:
        # Go read the file and grab line numbers and AEP, Duration and Temporal Pattern for later.
        f2 = f1.readlines()  
        for n, line in enumerate(f2):
            if '"River Levels"' in line:
                WL_start = int(n)
            elif "Flow Rates  " in line:
                Q_start = int(n)
            elif "PARAMETER data" in line:
                param_start = int(n)
            
            ##STORM DURATION OF 2.0 HOURS FOR ARI 1E3 ENSEMBLE 0 BFVF=0.03
            elif "STORM DURATION" in line: 
                parts = line.split()
                dur = parts[3].split('.')[0]  
                aep = parts[7]             
                #tp = int(parts[9])  # doesn't work for >10 patterns
                tp = f.split('_')[-1]

        # ---- Now open the file with Pandas and grab all the Flows -----
        # nb usescols isn't necessary as dftmp.columns writes everything out. 
        dftmp = pd.read_csv(csvin, skiprows=Q_start, skipfooter=4, usecols=[0,1,2], index_col=0) 
        dftmp.index.names = ['Time_hrs']
        dftmp.columns = dftmp.columns.str.replace(' ', '')
        dftmp.columns = dftmp.columns.str.replace('(', '')  # can't do it all at once- '(C)' means columns?
        dftmp.columns = dftmp.columns.str.replace('C', '')
        dftmp.columns = dftmp.columns.str.replace(')', '')               
        dftmp.columns = pd.MultiIndex.from_product([[f],[aep],[dur],[tp],dftmp.columns]) 
               
        dfALL_URBS = pd.concat([dfALL_URBS,dftmp],axis=1)
        
        # ---- Now grab all the Levels -----
        # nb usecols=[0,1] selects the columns, i.e. [0,1] is the timestamp [0] and the first column [Ewen Maddock] 
        dftmp = pd.read_csv(csvin, skiprows=WL_start, skipfooter=((param_start+4)-Q_start), usecols=[0,1], index_col=0)         
        dftmp.index.names = ['Time_hrs']
        #first column is renamed from Ewen Maddock to Level for clarity
        dftmp.columns = pd.MultiIndex.from_product([[f],[aep],[dur],[tp],['Level']])         
        
        dfALL_URBS = pd.concat([dfALL_URBS,dftmp],axis=1)

# ---------- TIDY UP for use in Downstream models ---------
dfALL_URBS.interpolate(inplace=True, limit=10) # Create a uniform timeseries index 
dfALL_URBS = dfALL_URBS.sortlevel(4,axis=1)  # Group the output by Inflow, Level and Outflow across all events
dfALL_URBS = dfALL_URBS.fillna(0)  # needed for GoldSim

# ----------- Output ---------------------------------------
dfALL_URBS.max().to_csv(outpath+'MaxValues_URBS.csv')
dfALL_URBS.to_csv(outpath+'AllTimeseries_URBS.csv')