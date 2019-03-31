
import urllib                                   
import re
import datetime
import time



sock = urllib.urlopen("ftp://ftp.bom.gov.au/anon/gen/fwo/IDQ60336.html") 
htmlSource = sock.readlines()                            
sock.close()  

station_data = {}
mylist = []
date_list = []

for x in htmlSource:
    if 'Issued at' in x:
        y = x.split()
        time = y[2].split('.')
        hour = time[0]
        minute = time[1][0:2]
        ampm = time[1][2:]
        day = y[5]
        month = y[6]
        year = y[7]
        date_string = '%s/%s/%s %s:%s%s' %(day,month,year,hour,minute,ampm)
        #print date_string
        issue_date = datetime.datetime.strptime(date_string,'%d/%B/%Y %I:%M%p')
        print issue_date
        last_hour = issue_date - datetime.timedelta(0,0,0,0,minutes=int(minute))
        for i in range(7,-1,-1):
            date_list.append(last_hour - datetime.timedelta(hours=i))
            
    if '<tr>  <td>Alderley&nbsp;AL&nbsp;*</td>' in x:
        z = re.split('<td>|</td>',x)
        z1 = z[1].replace('&nbsp;'," ")
        z2 = z1.strip('*')
        station = z2.rstrip()
        station = station.replace(' ','_')
        #print '_%s_' %station
        station_data[station]=""
        belinda="broken"
    if '     <td align="right">' in x[0:24]:
        a0 = x.replace('&nbsp;',"-999")
        a = a0.split()
        mylist.append(a[2])        
    if '     </tr>' in x[0:11] and belinda="broken":
        station_data[station]=mylist
        mylist = []
        belinda = "working"

ts1 = datetime.datetime.today()
timestamp = ts1.strftime('%Y%m%d%H%M')
print timestamp
out = open(timestamp+'_rainfall.csv','w')
out.write('Location Names')
for y in station_data:
    out.write(',%s' %(y))

out.write('\n')
out.write('Location Ids')
for y in station_data:
    out.write(',%s' %(y))

out.write('\n')

out.write('Time')
for y in station_data:
    out.write(',P.obs')

out.write('\n')

for x in range(8):
    # yyyy-mm-dd HH:MM:SS format
    out.write('%s' %date_list[x].strftime('%Y-%m-%d %H:%M:%S'))
    for q in station_data:
        out.write(',%s'%station_data[q][x])
    out.write('\n')

out.close()

 