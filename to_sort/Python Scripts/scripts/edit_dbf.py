import sys
import dbf


dbf_file = sys.argv[1]
station = sys.argv[2]
edit_station = station.lstrip('0')

table = dbf.Table(dbf_file)
table.open()

for idx,record in enumerate(dbf.Process(table)):
    if edit_station == str(record.num):
        record.priority = '2'
        print 'Amended station: %s... Done!' %edit_station

table.close()
