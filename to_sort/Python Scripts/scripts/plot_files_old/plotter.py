def plot_urbs(pqhpath,event,catchment,csv_results):
    import numpy as np
    import sys
    import csv
    from datetime import timedelta 
    from datetime import date
    from datetime import time
    from datetime import datetime
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import pqh_extractor

      
    count = 0
    time_series = []
    time_series_raw = []
    ts_str = []
    ts_fmt = []
    series1 = []
    series2 = []
    open_csv = open(csv_results,'rb')
    open_rain = open('rainfall.csv','rb')
    e_open_rain = open('eff_rainfall.csv','rb')
    csv_file = csv.DictReader(open_csv, delimiter=',', quotechar='"')
    rain_file = csv.DictReader(open_rain, delimiter=',', quotechar='"')
    e_rain_file = csv.DictReader(e_open_rain, delimiter=',', quotechar='"')
    header_list = csv_file.fieldnames
    rain_header_list = rain_file.fieldnames
    e_rain_header_list = e_rain_file.fieldnames
    field_count = len(header_list)
    
    
    if open_csv.name == 'water_level.csv':
        results_type = 'Water Level'
        type_flag = 'H'
        unit = ' (m)'
    elif open_csv.name == 'flow_rates.csv':
        results_type = 'Flow'
        type_flag = 'Q'
        unit =  (' (m$^3$/s)')
    
    print 'Now generating plot for %s locations' %(results_type)
    
    #counter for fields in water level or discharge file
    xx = 1
    
    #format data
    time_series = []
    time_series_raw = []
    for row in csv_file:
        time_series_raw.append(float(row[header_list[0]]))
    for values in time_series_raw:
        vdays = int(values)
        vhours = int((values - int(values))*24)
        time_series.append(datetime(1899,12,30) + timedelta(days=vdays,hours=vhours))
        
    # start plotting for each location
    while xx <= max(field_count-1,1):
        test1 = str(header_list[xx-1])
        test2 = str(header_list[xx])
        testR = test2[0:-4].replace(" ","")
        try:
            test3 = str(header_list[xx+1])
        except:
            test3 = 'end_of_file'
        location = test2[0:-4].strip()
        open_csv.seek(0)
        open_csv.next()
        open_rain.seek(0)
        open_rain.next()
        e_open_rain.seek(0)
        e_open_rain.next()
        series1 = []
        series2 = []
        rain = [0.0]
        e_rain =[0.0]
        
        rain_t = 'False'
        e_rain_t = 'False'
        l_rain = 'False'
        #test rain data
        count = 0
        for header in rain_header_list:
            count = count + 1
            if testR in header:
                yy = count -1
                rain_t = 'True'
  
        count_e = 0
        for header in e_rain_header_list:
            count_e = count_e +1
            if testR in header:
                e_rain_t = 'True'
        
              
        # get PQH parameters
        
        stats = pqh_extractor.get_PQH_stats(pqhpath,event,catchment,location)
        # format series
        for row in csv_file:
            series1.append(float(row[header_list[xx]]))
            try:
                series2.append(float(row[header_list[xx+1]]))
            except:
                series2 = [0]
        for (i,item) in enumerate(series2):
            if item==-99:
               series2[i] = 0
        
        #Calculating rainfall losses    
        if rain_t == 'True' and e_rain_t == 'True':
            for row in rain_file:
                rain.append(float(row[rain_header_list[yy]]))
            for row in e_rain_file:
                e_rain.append(float(row[e_rain_header_list[yy]]))
            l_rain = np.subtract(rain,e_rain)
            r1 = rain
            r2 = l_rain
            l_rain_t = 'True'
        elif rain_t == 'True' and e_rain_t != 'True':
            for row in rain_file:
                rain.append(float(row[yy]))
            l_rain = rain
            r1 = rain
            r2 = l_rain
            l_rain_t = 'True'
        elif rain_t != 'True' and e_rain_t != 'True':
            l_rain_t = 'False'
        
        #Plotting    
        if test2[0:-4] == test3[0:-4] and test1[0:-4] != test2[0:-4]:
            print 'Now generating plot at %s' %(location)
            x = []
            x = time_series
            y1 = series1
            y2 = series2
            width = 0.04
            plt.close('all')
            
            
            if l_rain_t != 'False':
                
                fig, ax = plt.subplots(1) 
                B1 = ax.bar(x,r1, width, color = "cyan", label='Gross Rainfall',edgecolor = 'none')
                B2 = ax.bar(x,r2, width, color = "grey", label='Losses',edgecolor = 'none')
                plt.xlim([min(x),max(x)])
                if max(r1) == 0:
                    plt.ylim([0,0.1])
                elif max(r1)>0:
                    plt.ylim([0,max(r1)*1.5])
                ax.yaxis.set_ticks_position('right')            
                plt.yticks(fontsize = 6)
                ax.yaxis.set_label_position('right')
                ax.set_ylabel ('Rainfall (mm/hr)',fontsize = 10)
                legend1, labels1 = ax.get_legend_handles_labels()
                newax = ax.twinx()
                L1 = newax.plot(x,y1, 'r:', label=header_list[xx])
                L2 = newax.plot(x,y2, 'r-', label=header_list[xx+1])
                newax.yaxis.tick_left()
                ax.yaxis.tick_right()
                plt.yticks(fontsize = 6)
                newax.yaxis.set_label_position("left")
                newax.set_ylabel (results_type +unit, fontsize = 10)
                plt.yticks(fontsize = 6)
                plt.xlim([min(x),max(x)])
                legend2, labels2 = newax.get_legend_handles_labels()
                newax.legend(legend2 + legend1, labels2 + labels1, fontsize = 6)
                newax.yaxis.grid(True, color = 'grey',linewidth = 0.5)
                  
                  
                  
            elif l_rain_t == 'False':
                fig, ax = plt.subplots(1)   
                L1 = ax.plot(x,y1, 'r:', label=header_list[xx])
                L2 = ax.plot(x,y2, 'r-', label=header_list[xx+1])
                ax.set_ylabel (results_type +unit, fontsize = 10)
                plt.yticks(fontsize = 6)
                plt.xlim([min(x),max(x)])
                handles, labels = ax.get_legend_handles_labels()
                ax.legend(handles[::-1], labels[::-1],fontsize = 6)
                ax.yaxis.grid(True, color = 'grey',linewidth = 0.5)

            # Format plot
            if results_type == 'Water Level':
               plt.title('Event: %s at %s\n Parameters: alpha=%0.2f, beta=%0.2f, m=%0.2f, IL=%0.2f , CL=%0.2f' %(event,location,stats[0],stats[1],stats[2],stats[3],stats[4]), fontsize = 10 )
            elif results_type == 'Flow':
               plt.title('Event: %s at %s\n Parameters: alpha=%0.2f, beta=%0.2f, m=%0.2f, IL=%0.2f, CL=%0.2f\n Statistics: NS=%0.2f, VR=%0.2f, PR=%0.2f' %(event,location,stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],stats[6],stats[7]), fontsize = 10)
            fig.autofmt_xdate()
            ax.axes.set_xticklabels(x, rotation=45,fontsize = 6)
            myformat = mdates.DateFormatter('%d/%m/%Y %H:%M')
            ax.xaxis.set_major_formatter(myformat)
            ax.xaxis.set_major_locator(mdates.HourLocator(x[0].hour))
            ax.xaxis.grid(True,color = 'grey', linewidth = 0.5)
            
            # add seqwater logo
            myfig = plt.figure()
            im = imread('SEQWater_HOR_RGB.png')
            height = im.size[1]
            fig.figimage(im, 0, fig.bbox.ymax - height)
            
            
            # Export filenames
            try:
                int(event)
                filename2 = event + '_' + catchment + '_' + test2[0:-3].strip() + '_' + type_flag + '.png'
                filename3 = event + '_' + catchment + '_' + test2[0:-3].strip() + '_' + type_flag + '.jpg'
            except ValueError:
                filename2 = catchment + '_' + test2[0:-3].strip() + '_' + type_flag + '.png'
                filename3 = catchment + '_' + test2[0:-3].strip() + '_' + type_flag + '.jpg'
            plt.savefig(filename2,format='png',dpi=500 )
            plt.savefig(filename2,format='png',dpi=500 )
            print 'Now generating plot at %s... Done!' %(location)
                        
        elif test2[0:-4] != test3[0:-4] and test1[0:-4] != test2[0:-4]:
            print 'Now generating plot at %s' %(location)
            x = []
            x = time_series
            y1 = series1
            r1 = rain
            r2 = l_rain
            width = 0.05
            plt.close('all')
            fig, ax = plt.subplots(1)
            L1 = ax.plot(x,y1, 'r--', label=header_list[xx])
            ax.set_ylabel (results_type +unit, fontsize = 10)
            plt.yticks(fontsize = 6)
            
            if l_rain_t != 'False':
                  fig, ax = plt.subplots(1)
                  B1 = ax.bar(x,r1, width, color = "cyan", label='Gross Rainfall',edgecolor = 'none')
                  B2 = ax.bar(x,r2, width, color = "grey", label='Losses',edgecolor = 'none')
                  plt.xlim([min(x),max(x)])
                  if max(r1) == 0:
                      plt.ylim([0,0.1])
                  elif max(r1)>0:
                      plt.ylim([0,max(r1)*1.5])
                  ax.yaxis.set_ticks_position('right')            
                  plt.yticks(fontsize = 6)
                  ax.yaxis.set_label_position('right')
                  ax.set_ylabel ('Rainfall (mm/hr)',fontsize = 10)
                  legend1, labels1 = ax.get_legend_handles_labels()
                  
                  newax = ax.twinx()
                  L1 = newax.plot(x,y1, 'r:', label=header_list[xx])
                  newax.yaxis.tick_left()
                  ax.yaxis.tick_right()
                  plt.yticks(fontsize = 6)
                  newax.yaxis.set_label_position("left")
                  newax.set_ylabel (results_type +unit, fontsize = 10)
                  plt.yticks(fontsize = 6)
                  plt.xlim([min(x),max(x)])
                  legend2, labels2 = newax.get_legend_handles_labels()
                  newax.legend(legend2 + legend1, labels2 + labels1, fontsize = 6)
                  newax.yaxis.grid(True, color = 'grey', linewidth = 0.5)
                  
                  
            elif l_rain_t == 'False':
                  fig, ax = plt.subplots(1)   
                  L1 = ax.plot(x,y1, 'r:', label=header_list[xx])
                  ax.set_ylabel (results_type +unit, fontsize = 10)
                  plt.yticks(fontsize = 6)
                  plt.xlim([min(x),max(x)])
                  handles, labels = ax.get_legend_handles_labels()
                  ax.legend(handles[::-1], labels[::-1],fontsize = 6)
                  ax.yaxis.grid(True, color = 'grey', linewidth = 0.5)
                
            # Format plot
            if results_type == 'Water Level':
               plt.title('Event: %s at %s\n Parameters: alpha=%0.2f, beta=%0.2f, m=%0.2f, IL=%0.2f , CL=%0.2f' %(event,location,stats[0],stats[1],stats[2],stats[3],stats[4]), fontsize = 10 )
            elif results_type == 'Flow':
               plt.title('Event: %s at %s\n Parameters: alpha=%0.2f, beta=%0.2f, m=%0.2f, IL=%0.2f, CL=%0.2f\n Statistics: NS=%0.2f, VR=%0.2f, PR=%0.2f' %(event,location,stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],stats[6],stats[7]), fontsize = 10)
            fig.autofmt_xdate()
            ax.axes.set_xticklabels(x, rotation=45,fontsize = 6)
            myformat = mdates.DateFormatter('%d/%m/%Y %H:%M')
            ax.xaxis.set_major_formatter(myformat)
            ax.xaxis.set_major_locator(mdates.HourLocator(x[0].hour))
            ax.xaxis.grid(True,color = 'grey', linewidth = 0.5)
            # add seqwater logo
            
            
            # Export filenames
            try:
                int(event)
                filename2 = event + '_' + catchment + '_' + test2[0:-3].strip() + '_' + type_flag + '.png'
                filename3 = event + '_' + catchment + '_' + test2[0:-3].strip() + '_' + type_flag + '.jpg'
            except ValueError:
                filename2 = catchment + '_' + test2[0:-3].strip() + '_' + type_flag + '.png'
                filename3 = catchment + '_' + test2[0:-3].strip() + '_' + type_flag + '.jpg'
            plt.savefig(filename2,format='png',dpi=500 )
            print 'Now generating plot at %s... Done!' %(location)    
        xx = xx + 1
    open_csv.close
    open_rain.close
    e_open_rain.close

