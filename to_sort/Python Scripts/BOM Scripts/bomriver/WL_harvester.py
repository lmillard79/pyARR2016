
import urllib                                   
import xml.etree.ElementTree as ET
import re
import datetime
import time
import sys

stations_file = sys.argv[1]
stn_file = open(stations_file,'r')
stn = stn_file.readlines()
stn_list = []
stn_data = {}
a
for idx,s in enumerate(stn):
    text = s.split(",")
    mystn = text[1].rstrip('\n')
    ts1 = datetime.datetime.today()
    timestamp = ts1.strftime('%Y%m%d%H%M')
    output = open(timestamp+'_'+mystn+'.csv','w')

    sock = urllib.urlopen("http://www.bom.gov.au/fwo/"+text[0]+"/"+text[0]+"." + mystn + ".tbl.shtml") 
    htmlSource = sock.readlines()                            
    sock.close()  
    print 'Now scraping data for: %s ... %s of %s' %(mystn,idx+1,len(stn)+1)
    
    for x in htmlSource:
        if '<p class="stationdetails">' in x:
            y = re.split('<b>|</b>',x)
            stn_name = y[4][0:-2]
            stn_no = y[2].strip()
            if stn_no[0] == '0':
                stn_no = stn_no[1:]
            output.write('Location Names, %s\n'%(stn_name))
            output.write('Location Ids, H_%s\n'%(stn_no))
            output.write('Time, H.obs\n')
        if '<td align=left>' in x:
            day = x[15:17]
            month = x[18:20]
            year = x[21:25]
            hour = x[26:28]
            minute = x[29:31]
            date_string = '%s-%s-%s %s:%s:00' %(year,month,day,hour,minute)
            output.write('%s,' %date_string)
        if '<td align=right>' in x:
            data = re.split('<td align=right>|</td>',x)
            data_point = data[1]
            output.write('%s\n' %data_point)
            
