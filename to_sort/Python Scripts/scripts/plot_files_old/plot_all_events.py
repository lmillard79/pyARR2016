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
            elif len(c_txt) < 2:
                file = file_path + '\\' + events[0:-1] + '\\' + c_txt[0].rstrip('\n') + '\\' + c_txt[0].rstrip('\n') + '.csv'
                pqhpath = file_path + '\\' + events[0:-1] + '\\' + c_txt[0].rstrip('\n') + '\\' + c_txt[0].rstrip('\n') + '.pqh'
            print 'Now processing event %s, catchment %s' %(events[0:-1], c_txt[0].rstrip('\n'))
            os.system("Title Now running %s for Catchment: %s"%(events[0:-1],c_txt[0].rstrip('\n')))
            flag = sep_start.separate(file)
            if flag == 1:
                plotter.plot_urbs(pqhpath,events[0:-1],c_txt[0].rstrip('\n'),'water_level.csv')
            plotter.plot_urbs(pqhpath,events[0:-1],c_txt[0].rstrip('\n'),'flow_rates.csv')


e.close