#!/local/python/bin/python
'''
This script will go in and grab information from 
a pi report form collate all the information and 
produce stats/plots for board reports/those interested

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

print (startyear, startmonth, 1, int(unixstarttime))

print (endyear, endmonth, 31, int(unixendtime))

# ------------------------------------------- #
#      grabbing relavent report files         #
# ------------------------------------------- #

pth = '/web/data/reports/JCMT/'

import os	
from glob import glob

filenames = [os.path.basename(x) for x in glob(pth+"pirep_*.txt")]

#print(type(filenames))

myfiles=[]


for x in filenames:
	timestamp = x[6:16] # only correct for pirep	
#	print (x,timestamp)
	if unixstarttime <= int(timestamp) <= unixendtime:
		print ("pirep_{0}.txt".format(timestamp))
		myfiles.append("{0}pirep_{1}.txt".format(pth,timestamp))
print (myfiles)

	
# -------------------------------------------- #
#      grabbing info from report files         #
# -------------------------------------------- #	



def ratingvalue(stringprovided,wheretosearch):
	'''
	the function is used to convert a qualitive rating 
	into a quantative value.
	'''
	ratings = {'not applicable': None, 'very dissatisfied': 0, 'dissatisfied': 1, 'satisfied': 2, 'very satisfied': 3}
	if stringprovided in wheretosearch:
		print (stringprovided)
		print (wheretosearch)
		if ":   very satisfied" in wheretosearch:
			ratevalue = ratings['very satisfied']
		if  ":   satisfied" in wheretosearch:
			ratevalue = ratings['satisfied']
		if  ":   dissatisfied" in wheretosearch:
			ratevalue = ratings['dissatisfied']
		if ":   very dissatisfied" in wheretosearch:
			ratevalue = ratings['very dissatisfied']
		if  ":   not applicable" in wheretosearch:
			ratevalue = ratings['not applicable']
		print (ratevalue)
#		return ratevalue


	

# maybe need to define a function to turn a line into a rating.

for x in myfiles:
	with open(x) as input_data:
		print (x)
		for line in input_data:
			if "Percentage Completed:" in line:
				percom = (line[-7:-2]).strip()
				print ("completion = {0}%".format(percom))

#			if "Please rate proposal system ease of" in line:
#				rateline = line				
#			if "OT ease of use.:" in line:
#			if "OT documentation.:" in line: 
#			if "OT support.:" in line:  
#			if "OMP interface to download your data.:" in line: 
#			if "CADC interface for searching the JCMT Science Archive and downloading data.:" in line:
#			if "Starlink software installation.:" in line:
#			if "Starlink software packages for analysis, reduction, and visualisation.:" in line:
#			if "heterodyne data reduction documentation.:" in line: 
#			if "SCUBA-2 data reduction documentation.:" in line: 
#			if "data reduction pipelines (ORAC-DR).:" in line: 
#			if "science-products of the data reduction pipelines.:" in line:  


 			ratedataquality = ratingvalue("quality of data obtained.:",line)
 	#		print(ratedataquality)


# 			if "quality of data obtained.:" in line:
# 				rateline = line
# 				print (rateline)
# 				if ":   very satisfied" in rateline:
# 					print ('very satisfied')
# 					ratedataquality = ratings['very satisfied']
# 				if  ":   satisfied" in rateline:
# 					ratedataquality = ratings['satisfied']
# 				if  ":   dissatisfied" in rateline:
# 					ratedataquality = ratings['dissatisfied']
# 				if ":   very dissatisfied" in rateline:
# 					ratedataquality = ratings['very dissatisfied']
# 				if  ":   not applicable" in rateline:
# 					ratedataquality = ratings['not applicable']
# 				print (ratedataquality)
				
#			if "satisfied were you with the level of communication with your Friend of Project.:" in line:
			rateomp = ratingvalue("ease and usefulness of OMP project home page.:",line)
			rateweb = ratingvalue("satisfied were you with the web site.:",line)

#Completion of project in terms of hours:   0
# Please rate usefulness of data collected/level of completeness.: 

# Please rate likelihood of data leading to publication.: 	

# -------------------------------------------- #
#      plotting info from report files         #
# -------------------------------------------- #

# in essence I want one plot to show median value (as a bar) and SD (as an error bar) for each rating.


