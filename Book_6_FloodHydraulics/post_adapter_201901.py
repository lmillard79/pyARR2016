import datetime as dt
import getopt, sys, os
import csv
#import pandas as pd


# input and output file names

# module to round time stamps
def roundTime(DT=None, roundTo=1):
   if DT == None : DT = dt.datetime.now()
   seconds = (DT - DT.min).seconds
   # // is a floor division, not a comment on following line:
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return DT + dt.timedelta(0,rounding-seconds,-DT.microsecond)

# populate the xml file
def xml(location, parameter, value, time):
    sd = str(dt.datetime.date(time[0]))
    ##print sd
    st = str(dt.datetime.time(time[0]))
    ##print st
    ed = str(dt.datetime.date(time[-1]))
    et = str(dt.datetime.time(time[-1]))

    with open(TUFLOW_OUT_XML,'a+b') as xf:
        xf.write('    <series>\n')
        xf.write('        <header>\n')
        xf.write('            <type>instantaneous</type>\n')
        loc_text = str('            <locationId>%s</locationId>\n') % (parameter)
        xf.write(loc_text)
        loc_text = str('            <parameterId>%s</parameterId>\n') % (location)
        xf.write(loc_text)
        xf.write('            <timeStep unit="second" multiplier="900"/>\n')
        sd_text = str('            <startDate date="%s" time="%s"/>\n') % (sd, st)
        xf.write(sd_text)
        ed_text = str('            <endDate date="%s" time="%s"/>\n') % (ed, et)
        xf.write(ed_text)
        xf.write('            <missVal>-999.0</missVal>\n')
        xf.write('            <stationName>Hydro Gauge 1</stationName>\n')
        xf.write('            <units>m3/s</units>\n')
        xf.write('        </header>\n')
        for i in range(len(value)):
            event_date = str('        <event date="%s"') % (str(dt.datetime.date(time[i])))
            event_time = str(' time="%s"') % (str(dt.datetime.time(time[i])))
            event_valu = str(' value="%s"') % value[i]
            event_flag = str(' flag="0"/>\n')
            event = str(event_date+event_time+event_valu+event_flag)
            xf.write(event)
        xf.write('    </series>\n')

# populate and close out xml file
def xmlend(location, parameter, value, time):
    sd = str(dt.datetime.date(time[0]))
    ##print sd
    st = str(dt.datetime.time(time[0]))
    ##print st
    ed = str(dt.datetime.date(time[-1]))
    et = str(dt.datetime.time(time[-1]))

    with open(TUFLOW_OUT_XML,'a+b') as xf:
        xf.write('    <series>\n')
        xf.write('        <header>\n')
        xf.write('            <type>instantaneous</type>\n')
        loc_text = str('            <locationId>%s</locationId>\n') % (parameter)
        xf.write(loc_text)
        loc_text = str('            <parameterId>%s</parameterId>\n') % (location)
        xf.write(loc_text)
        xf.write('            <timeStep unit="second" multiplier="900"/>\n')
        sd_text = str('            <startDate date="%s" time="%s"/>\n') % (sd, st)
        xf.write(sd_text)
        ed_text = str('            <endDate date="%s" time="%s"/>\n') % (ed, et)
        xf.write(ed_text)
        xf.write('            <missVal>-999.0</missVal>\n')
        xf.write('            <stationName>Hydro Gauge 1</stationName>\n')
        xf.write('            <units>m3/s</units>\n')
        xf.write('        </header>\n')
        for i in range(len(value)):
            event_date = str('        <event date="%s"') % (str(dt.datetime.date(time[i])))
            event_time = str(' time="%s"') % (str(dt.datetime.time(time[i])))
            event_valu = str(' value="%s"') % value[i]
            event_flag = str(' flag="0"/>\n')
            event = str(event_date+event_time+event_valu+event_flag)
            xf.write(event)
        xf.write('    </series>\n')        
        xf.write('</TimeSeries>')
        
# Main section in script
def main(TUFLOW_OUT_XML,TUFLOW_PO,tufl_trd):
    
    simID = TUFLOW_PO[-34:-10]
    
     # write XML output header
    with open(TUFLOW_OUT_XML,'w') as xf:
        xf.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        xf.write('<TimeSeries xmlns="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd" version="1.2">\n')
        xf.write('    <timeZone>10.0</timeZone>\n')

    # predefine some variables
    ## data=pd.DataFrame()
    data=[]
    time=[]
    date=[]
    time=[]

    # open the TUFLOW _PO.csv file           
    with open(TUFLOW_PO, 'rb') as f:  #csvfile
        reader = csv.reader(f, delimiter=',', quotechar='"')
        header = reader.next()  #next line of csv 
    f.close()
     
    header[0]='Timestep'
    header[1]='Time'
    i=1         
    
    for col in header[2:]:    # each item after Time and Timestep column headers
        i= i+1
        prefix = 'H'
        parameter = 'Water Level'
       
        a = col[len(prefix)+1:]   # strip the Prefix i.e. H 
        indA = a.find(simID)
        indB = a.rfind('[') #find last occurrence of [
        if (indA >= 0) and (indB >= 0): # strip simulation ID from header
            a = a[0:indB-1]  # returns just the location name                
        header [i] = a     
        
    #try:        
        ##data = pd.read_csv(TUFLOW_PO, header=0, names=header)    
    
    with open(TUFLOW_PO) as csvfile:
        line_count = 0
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if line_count == 0:
                header0 = row
                line_count +=1                                    
            elif line_count == 1:
                header1 = row
                line_count +=1    
                #header = [x[0] + x[1] for x in zip(header0, header1)]
                header = zip(header0,header1)
            else:
                line_count +=1
            
    with open(TUFLOW_PO) as csvfile:
        line_count = 0
        reader = csv.DictReader(csvfile, fieldnames=header) 
        for row in reader:
            if line_count < 3: 
                line_count +=1             
           
            elif line_count < 15:                                
                data.append(row)
                line_count +=1        
            else:
                line_count +=1 
                pass
            
        with open('test.txt','w') as outfile:
            fp = csv.DictWriter(outfile, header)
            fp.writeheader()
            fp.writerows(data)
            
            
        raw_input('ttt')    
        
 
        '''
        with open("path/to/file.csv", "r") as f:
            csvraw = list(csv.reader(f))
        col_headers = csvraw[1][1:]
        row_headers = [row[0] for row in csvraw[1:]]
        data = [row[1:] for row in csvraw[1:]]
        
 
    except:
        print 'here'
        message = 'ERROR - Error reading data from: '+TUFLOW_PO
        error = True
        return error, message   
    ''' 
    # extract simulation start/end time
    with open(tufl_trd,('r')) as rf:
        for line in rf:
            #print line
            if 'simulation start time =' in line:
                d=str(line[26:36])
                t=str(line[37:45])
                yy, mm, dd = [int(a) for a in d.split('-')]
                hh, mn, ss = [int(a) for a in t.split(':')]
                timeorig=dt.datetime(yy,mm,dd,hh,mn,ss)
            if 'End Time' in line:
                com, dur = [a.strip() for a in line.split('==')]
                timeend =timeorig+dt.timedelta(hours=float(dur))

    # put time series results in an output XML file

    for i in range(data.shape[1]-1):                # i  Number of columns/locations 
        value = []                                  # reset the value variable list
        for j in range(data.shape[0]-1):            # j is Number of rows / time records           
            if i is 0:              # first column is blank
                next
            elif i is 1:            # time column                
                t = timeorig+dt.timedelta(hours=float(data.iloc[j,i]))  #--- 
                t = roundTime(t,roundTo=1)        
                time.append(t)
            else:
                value.append(data.iloc[j,i])         
                
        if i > 1:                   # for each data column, generate output XML entry
            xml(parameter, data.iloc[:,i].name, value, time)
            
        if i == data.shape[1]-2:      # close out XML file            
            xmlend(parameter, data.iloc[:,i].name, value, time)                            
          
if __name__ == '__main__':
    '''
    Add Arguments into python script

A = The tuflow output XML which will be read into FEWS
B = The TUFLOW PO csv file
C = TUFLOW read file

        '''
    #try:
    #    #opts, args = getopt.getopt(sys.argv[1:], "A:B:C:")
    ROOT_DIR=r'D:\FEWS\FEWS_Standalone\FEWS_2017_01_EstryFastModel\Modules\ESTRY\lowerBrisbane/'

    TUFLOW_OUT_XML = ROOT_DIR+'output.xml'
    TUFLOW_PO = ROOT_DIR+'Output\lowerBris_FAST-0403_FEWS_PO.csv'
    tufl_trd =ROOT_DIR+'\end_time.trd'
    
    '''
    except getopt.GetoptError, err:
    
        # print help information and exit:
        print str(err)
        sys.exit('ERROR: Unknown Argument')
    
    for o, a in opts:
        if o == "-A":
            TUFLOW_OUT_XML = a
        elif o in ("-B"):
            TUFLOW_PO = a
        elif o in ("-C"):
            tufl_trd = a
        else:
            assert False, "unhandled option"

    nArg = len((sys.argv[1:]))
    if nArg > 6:
        print('ERROR:\nPost adapter is expecting Three arguments. Please check.')
        print('The following arguments are expected:\n-A = The tuflow output XML which will be read into FEWS,\n-B = The TUFLOW PO csv file\n-C = TUFLOW read file')
        sys.exit('ERROR: The following arguments are expected:\n-A = The tuflow output XML which will be read into FEWS,\n-B = The TUFLOW PO csv file\n-C = TUFLOW read file')
    elif nArg < 6:
        print('ERROR:\nPost adapter is expecting Three arguments. Please check.')
        print('The following arguments are expected:\n-A = The tuflow output XML which will be read into FEWS,\n-B = The TUFLOW PO csv file\n-C = TUFLOW read file')
        sys.exit('ERROR: The following arguments are expected:\n-A = The tuflow output XML which will be read into FEWS,\n-B = The TUFLOW PO csv file\n-C = TUFLOW read file')
'''

    # Call the function doing all the work
    main(TUFLOW_OUT_XML,TUFLOW_PO,tufl_trd)
