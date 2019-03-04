Import pandas as pd 
##Read in the files, define the probability widths required in a CSV
probDict = r"W:\Hydraulics\3_Pine\NorthPine\DamBreakAssessment2017\2_Hydrology\Dict_ProbWidth.csv"
S_probWidth = pd.read_csv(probDict,index_col=0,usecols=[0,4]).squeeze()
RPHfile = r'W:\Hydrology\dams\north_pine\urbs\design_rev2017\design_flood\NPD\Analysis\FSL_38.6\DES16_5gates_Outflow_arr_spatialV.xlsm'

## Read in the same spreadsheet as Steve’s not sure if URBS can give a RPH dump without the translation from RPQ
RPH = pd.read_excel(RPHfile, sheetname='RPH',index_col=(0,1),skiprows=4,header=0)
RPH = RPH.iloc[:,:19]

## Set up an empty plot figure
fig,ax = plt.subplots()

for n, g in RPH.groupby('Duration'):
    ## Have to do some initial tidy up 
    nom = str(n)+'h_PeakLevel'    
    Prob = g.stack().reset_index()
    Prob = Prob.rename(columns={'ARI':'AEP (1 in Y)',0:nom,'level_2':'TP'})        
    Prob = Prob.sort_values(nom)
    ## Do a count of the number of temporal patterns per duration
    ProbCount = Prob.groupby('AEP (1 in Y)')[nom].count().to_dict()  
    Prob['count'] = Prob['AEP (1 in Y)'].map(ProbCount)
    ## Map the width to AEP
    Prob['width'] = Prob['AEP (1 in Y)'].map(widthDict)    
    
    ## Do a count of the number of temporal patterns per duration
    
    Prob['Width'] = Prob['width']/Prob['count']
    Prob['Accum'] = Prob['Width'].cumsum()            
    Prob['AEP_tpt'] = 1.0/(1.0 - (Prob['Accum']))

    ## Filter out the very end
    Prob = Prob[Prob['AEP_tpt']>0.0]
    Prob.plot(x='AEP_tpt',y=nom,logx=True,ax=ax,style='.',xlim=(2,1e7))
