###############################################################################################################
#This script is designed to do zonal statistic analysis of all .tif in a folder.
#new attribute will be created in the selected vector layer 
#additional statistics avalialbel, using | to add. E.g. 
#QgsZonalStatistics(vectorlayer, rasterlayer, prefix, band number, QgsZonalStatistics.Mean | QgsZonalStatistics.Max |QgsZonalStatistics.Min)
#Need to run from QGIS --> Plugins --> Python


# Copy paste the Pandas folder from the Anaconda site-packages and paste into your QGIS site-packages folder. I also included the pandas egg-info file.
#  From : C:\Python27\Lib\site-packages\pandas
# To : C:\Program Files\QGIS 2.18\apps\Python27\lib\site-packages


from qgis.analysis import QgsZonalStatistics
import glob, os, re


'''
layer = iface.addVectorLayer(r"W:/Hydraulics/2_NorthCoast/EwenMaddock_FIA_2018/GIS/EwenMaddockDownstream_IncCurrimunidiCk_WGS84.shp", "EwenMaddockDownstream_IncCurrimunidiCk_WGS84", "ogr")
if not layer:
    print "Layer failed to load!"
#vectorlayer = qgis.utils.iface.mapCanvas().currentLayer()
'''
#rasterfolder = r'W:\Hydrology\_2016 ARR Review and application to Dams\02 IFD Grids\BOM_IFD_GRID'
rasterfolder = r'W:\Hydrology\_2016 ARR Review and application to Dams\02 IFD Grids\IFD_GRID_FineRes'
outputfolder = r'W:\Hydraulics\2_NorthCoast\EwenMaddock_FIA_2018\DownstreamRainfall'

## Load the catchment layers (Lat/Long WGS84) and write their names here:
layerNames = ['EwenMaddockDownstream_IncCurrimunidiCk_WGS84']

for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
    if lyr.name() in layerNames:
        vectorlayer = lyr
        for root, subdirs, files in os.walk(rasterfolder):
            for file in files: 
                #if file.endswith("w001001.adf"):
                if file.endswith("tif"):
                    #r =root.split('\\')
                    lyr_name = file[:-4]
                    tm = int(lyr_name[0:5])
                    ey = lyr_name[-2:]
                    if tm < 60:
                        # Ignore short duration events
                        pass
                    elif ey == 'ey':
                        # Ignore high frequency events
                        pass
                    else:
                        if "001a" in lyr_name:
                            lyr_event_name = lyr_name.replace("001a", "0100y")
                        elif "002a" in lyr_name:
                            lyr_event_name = lyr_name.replace("002a", "050y")
                        elif "005a" in lyr_name:
                            lyr_event_name = lyr_name.replace("005a", "020y")
                        elif "010a" in lyr_name:
                            lyr_event_name = lyr_name.replace("010a", "010y")
                        elif "020a" in lyr_name:
                            lyr_event_name = lyr_name.replace("020a", "005y")
                        elif "050a" in lyr_name:
                            lyr_event_name = lyr_name.replace("050a", "002y")
                        elif "01EY" in lyr_name:
                            lyr_event_name = lyr_name.replace("01EY", "001y")
                        else:
                            lyr_event_name = lyr_name     
                        
                        file_path = os.path.join(root,file)
                        print (lyr_event_name)
                        zoneStat= QgsZonalStatistics(vectorlayer, file_path, lyr_event_name, 1, QgsZonalStatistics.Mean)
                        zoneStat.calculateStatistics(None)
                        
        #Process each Layer listed above into a table
        nom = lyr.name()   
        IFDs = []
        fields = lyr.pendingFields()
        for feature in lyr.getFeatures():            
            field_names = [field.name() for field in fields]
            ifd = dict(zip(field_names, feature.attributes()))
            IFDs.append(ifd)
            
        keys = IFDs[0].keys()
                
        with open (outputfolder+'/'+nom+'.csv','w') as fout:    
            for k in keys:                          
                T = str(IFDs[0][k])
                row = k+','+T+'\n' 
                fout.write(row)
        
        # Creates a BOM table for direct input to Excel Worksheet
        '''
import pandas as pd
import csv

fin = 'EwenMaddockDownstream_IncCurrimunidiCk_WGS84.csv' 
df = pd.read_csv(fin,names=['Event','Depth'])
df['Depth'] = df['Depth'].round(2)
df[['Durn','ARI']] = df['Event'].str.split('m',expand = True)
df['ARI'] = df['ARI'].str.replace('y','')
df[['Durn','ARI']] = df[['Durn','ARI']].apply(pd.to_numeric)
df['Durn'] = df['Durn']/60
tbl = df.pivot(index='Durn',columns='ARI',values='Depth')
tbl.to_csv(fin[:-4]+'_output02.csv')
        '''
        print ('Complete!')