#!/local/python/bin/python
'''
This script will go in and grab information from 
a pi report form collate all the information and 
produce stats/plots for board reports/those interested
'''


# -------------------------------------------------- #
# setting up ability to grab input from command line #
# -------------------------------------------------- #

import argparse

parser = argparse.ArgumentParser(description="This program's aim is to collate  \
				the information produced in the pireport form",
				usage="pirep-collate.py")                           
parser.add_argument("-y",
		dest="year",
		default=None,
		help="the year requested (i.e. 2017)")
parser.add_argument("-s",
		dest="semester",
		default=None,
		help="the semester requested (A or B)")
args = parser.parse_args()
if (args.year == None) or (args.semester == None):
	parser.print_help()
else:
	print ("\n year and semester provided: {0} {1}\n".format(args.year,args.semester))    


# ------------------------------------------- #
# converting UT into unixtime for file naming #
# ------------------------------------------- #


if (args.semester == "A"):
	startyear = int(args.year)
	startmonth = 2
	endyear = startyear
	endmonth = 7
elif (args.semester == "B"):
	startyear = int(args.year)
	startmonth = 8
	endyear = startyear+1
	endmonth = 1
else:
	print ("semester not specified")

import time
from datetime import date

startdate = date(startyear, startmonth, 1)
enddate = date(endyear, endmonth, 31)

unixstarttime = time.mktime(startdate.timetuple())

unixendtime = time.mktime(enddate.timetuple())

print (startyear, startmonth, 1 ,int(unixstarttime))

print (endyear, endmonth, 31 ,int(unixendtime))

# ------------------------------------------- #
#      grabbing relavent report files         #
# ------------------------------------------- #


filelocation = '/web/data/reports/JCMT/'


