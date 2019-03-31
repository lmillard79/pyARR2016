import sep_start
import plotter
import pqh_extractor
import os, sys

event_list = sys.argv[1]
catch_list = sys.argv[2]
file_path = ''
c_list = []

e = open(event_list,'r')
c = open(catch_list,'r')
log = open('log.txt','w')
c_file = c.readlines()


for idx,events in enumerate(e):
    if events == '\n':
        break
    for names in c_file:
        if names == '\n':
            continue
        os.system('cls')
        if idx == 0:
            file_path = events.rstrip('\n')
        elif idx != 0:
            c_txt = names.split(',')
            if len(c_txt) == 2:
                file = file_path + '\\' + events[0:-1] + '\\' + c_txt[0] + '\\' + c_txt[1].rstrip('\n') + '.csv'
                pqhpath = file_path + '\\' + events[0:-1] + '\\' + c_txt[0] + '\\' + c_txt[1].rstrip('\n') + '.pqh'
                pqhfile = c_txt[1].rstrip('\n') + '.pqh'
            elif len(c_txt) < 2:
                file = file_path + '\\' + events[0:-1] + '\\' + c_txt[0].rstrip('\n') + '\\' + c_txt[0].rstrip('\n') + '.csv'
                pqhpath = file_path + '\\' + events[0:-1] + '\\' + c_txt[0].rstrip('\n') + '\\' + c_txt[0].rstrip('\n') + '.pqh'
                pqhfile = c_txt[0].rstrip('\n') + '.pqh'
            print 'Now processing event %s, catchment %s' %(events[0:-1], c_txt[0].rstrip('\n'))
            os.system("Title Now running %s for Catchment: %s"%(events[0:-1],c_txt[0].rstrip('\n')))
            
            # add some error reporting and continue if a loop fails
            # writes errors to log.txt
            try:
                flag = sep_start.separate(file)
                log.write('Success: File: %s separation: OK\n'%(file))
            except:
                print 'Failed to separte CSV file: %s' %(file)
                log.write('File: %s separation: FAILED\n'%(file))
                continue
            if flag == 1:
                try:
                    plotter.plot_urbs(pqhpath,events[0:-1],c_txt[0].rstrip('\n'),'water_level.csv')
                    log.write('Success: plot water level for file %s\n'%(pqhfile))
                except:
                    print 'Failed to plot water level PQH file: %s' %(pqhfile)
                    log.write('Failed to plot water level for file %s\n'%(pqhfile))
                    continue
            try:
                plotter.plot_urbs(pqhpath,events[0:-1],c_txt[0].rstrip('\n'),'flow_rates.csv')
                log.write('Success: plot flow for file %s\n'%(pqhfile))
            except:
                print 'Failed to plot flow from PQH file: %s' %(pqhfile)
                log.write('Failed to plot flow for file %s\n'%(pqhfile))
                continue
                

c.close
e.close
log.close