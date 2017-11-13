#!/local/python/bin/python
'''
This script will go in and grab information from 
an observer report form collate all the information and 
produce stats/plots for board reports/those interested

This is not done on a strict by semester basis but is good enough for 
the purposes of tracking user satisfaction.

Note I do not do this by region it only matters that any issues
are addressed and that we address areas that need it. 

inputs: -y year -s semester
i.e. -y 2017 -s A
'''


# -------------------------------------------------- #
# setting up ability to grab input from command line #
# -------------------------------------------------- #

import argparse

parser = argparse.ArgumentParser(description="This program's aim is to collate  \
				the information produced in the observer report form",
				usage="obsrep-collate.py")                           
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

print (startyear, startmonth, 1, int(unixstarttime))

print (endyear, endmonth, 31, int(unixendtime))

# ------------------------------------------- #
#      grabbing relavent report files         #
# ------------------------------------------- #

pth = '/web/data/reports/JCMT/'

import os	
from glob import glob

filenames = [os.path.basename(x) for x in glob(pth+"obsrep_*.txt")]

myfiles=[]

for x in filenames:
	timestamp = x[7:17] # only correct for obsrep	
# 	print (x,timestamp, timestamp.islower())
	if timestamp.islower() is False: # dismissing the weirdly named files from 2009. 
		if unixstarttime <= int(timestamp) <= unixendtime:
#  			print ("obsrep_{0}.txt".format(timestamp))
			myfiles.append("{0}obsrep_{1}.txt".format(pth,timestamp))
# print (myfiles)

	
# -------------------------------------------- #
#      grabbing info from report files         #
# -------------------------------------------- #	

#first a dictionary of ratings and corresponding values
ratings = {'not applicable': None, 'very dissatisfied': 0, 'dissatisfied': 1, 'satisfied': 2, 'very satisfied': 3, 'very useful':3, 'in prep':3}

# going to use tables to add data row by row to a new table:

from astropy.table import Table, Column
import numpy as np

### current bug - cannot add the project id to the output table - format issue seems to be the problem

t = Table()
t = Table(names=('ratedata','ratequeue','ratetelescope','rateinstrument','ratecomputing','ratedr','rateweb','ratesupport'))

for x in myfiles:
	with open(x) as input_data:
 		print (x)
		# setting all variables to None before going into loop
		ratedata=ratequeue=ratetelescope=rateinstrument=ratecomputing=ratedr=rateweb=ratesupport=None
		for line in input_data:
			if "TEST" in line: #IGNORE ANY TEST FILES THAT EXIST 
# 				print ("need to skip TEST FOUND!!!!!")
				break
			if "Reference number" in line:
				projid = repr((line.split(":"))[1].strip())
# 				print (projid)
# 				print (type(projid))
			if "data obtained for Observer's programme" in line:
				ratedata = ratings[(line.split(":"))[1].strip()]
			if "satisfied were you with the queue system?" in line:
				ratequeue = ratings[(line.split(":"))[1].strip()]
			if "performance of the telescope" in line:
				ratetelescope  = ratings[(line.split(":"))[1].strip()]
			if "performance of the instruments" in line:
				rateinstrument = ratings[(line.split(":"))[1].strip()]
			if "with the computing resources" in line:
				ratecomputing = ratings[(line.split(":"))[1].strip()]
			if "with the data reduction software" in line:
				ratedr = ratings[(line.split(":"))[1].strip()]
			if "with the DR software" in line: # needed for the 2015A forms
				ratedr = ratings[(line.split(":"))[1].strip()]
			if "with the web site" in line:
				rateweb = ratings[(line.split(":"))[1].strip()]
			if "support provided during your run" in line:
				ratesupport = ratings[(line.split(":"))[1].strip()]
		t.add_row((ratedata,ratequeue,ratetelescope,rateinstrument,ratecomputing,ratedr,rateweb,ratesupport))
 	
print(t)



# -------------------------------------------- #
#      plotting info from report files         #
# -------------------------------------------- #

# in essence I want one plot to show median value (as a bar) and min/max (as an error bar) for each rating.


import matplotlib 
matplotlib.use('agg')
from matplotlib import pyplot as plt

names = np.array(['Data Quality','Queue','Telescope','Instruments','Computing','Dara Reduction','Web site','Support'])
meanvalues = np.array([np.nanmean(t['ratedata']),np.nanmean(t['ratequeue']),np.nanmean(t['ratetelescope']),np.nanmean(t['rateinstrument']),np.nanmean(t['ratecomputing']),np.nanmean(t['ratedr']),np.nanmean(t['rateweb']),np.nanmean(t['ratesupport'])])
minvalues = np.array([np.nanmin(t['ratedata']),np.nanmin(t['ratequeue']),np.nanmin(t['ratetelescope']),np.nanmin(t['rateinstrument']),np.nanmin(t['ratecomputing']),np.nanmin(t['ratedr']),np.nanmin(t['rateweb']),np.nanmin(t['ratesupport'])])
maxvalues = np.array([np.nanmax(t['ratedata']),np.nanmax(t['ratequeue']),np.nanmax(t['ratetelescope']),np.nanmax(t['rateinstrument']),np.nanmax(t['ratecomputing']),np.nanmax(t['ratedr']),np.nanmax(t['rateweb']),np.nanmax(t['ratesupport'])])

mindiff = meanvalues - minvalues  
maxdiff = maxvalues - meanvalues

fig = plt.figure()
y_pos = np.arange(len(names)) # make an array from 0 to length or the number of bars needed
x_pos = (0,1,2,3)
x_words = ('very dissatisfied','dissatisfied','satisfied','very satisfied')
plt.barh(y_pos, meanvalues, align='center', color='orange', alpha=0.7, xerr=(mindiff,maxdiff),ecolor='grey')
plt.yticks(y_pos, names)
plt.xticks(x_pos, x_words)
plt.title('Observer Feedback for {0}{1} ({2})'.format(args.year,args.semester,len(t['ratesupport'])))
plt.savefig('/home/hparsons/WWW/operations/reports/obsrep/{0}{1}-obsrep.pdf'.format(args.year,args.semester))











