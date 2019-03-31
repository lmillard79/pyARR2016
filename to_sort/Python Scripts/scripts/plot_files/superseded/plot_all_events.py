import sep_start
import plotter_v2
import pqh_extractor
import os, sys

event_list = sys.argv[1]
catch_list = sys.argv[2]
file_path = ''
c_list = []

e = open(event_list,'r')
c = open(catch_list,'r')

for catchments in c:
    c_list.append(catchments[0:-1])
c.close
print c_list

#print c_list

for idx,events in enumerate(e):
    for names in c_list:
        os.system('cls')
        if idx == 0:
            file_path = events[0:-1]
        elif idx != 0:
            file = file_path + '\\' + events[0:-1] + '\\' + names + '\\' + names + '.csv'
            pqhpath = file_path + '\\' + events[0:-1] + '\\' + names + '\\' + names + '.pqh'
            print 'Now processing event %s, catchment %s' %(events[0:-1], names)
            os.system("Title Now running %s for Catchment: %s"%(events[0:-1],names))
            flag = sep_start.separate(file)
            
            if flag == 1:
                plotter_v2.plot_urbs(pqhpath,events[0:-1],names,'water_level.csv')
           
  
            plotter_v2.plot_urbs(pqhpath,events[0:-1],names,'flow_rates.csv')


e.close