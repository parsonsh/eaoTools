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

ratings = {'not applicable': None, 'very dissatisfied': 0, 'dissatisfied': 1, 'satisfied': 2, 'very satisfied': 3, 'very useful':3, 'in prep':3}



# going to use tables to add data row by row to a new table:

from astropy.table import Table, Column
import numpy as np

t = Table()
t = Table(names=('Completion', 'HoursRemaining', 'rateproposalease', 'ratepropdocs', 'ratesc2itc', 'ratehetitc', 'ratepross', 'rateotinstall', 'rateotease','rateotdocs','rateotsupport','rateompdownload','ratecadcdownload','ratestarinstall','ratestarlink','ratehetdocs','ratesc2docs','rateoracdr','ratescienceproduct','ratedataquality','ratecompletion','ratepublicationprob','ratefop','rateomp','rateweb'), dtype=('float',float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float))
# t = Table(names=('projid','Completion', 'HoursRemaining', 'rateproposalease', 'ratepropdocs', 'ratesc2itc', 'ratehetitc', 'ratepross', 'rateotinstall', 'rateotease','rateotdocs','rateotsupport','rateompdownload','ratecadcdownload','ratestarinstall','ratestarlink','ratehetdocs','ratesc2docs','rateoracdr','ratescienceproduct','ratedataquality','ratecompletion','ratepublicationprob','ratefop','rateomp','rateweb'), dtype=('str','float',float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float))


# maybe need to define a function to turn a line into a rating.

for x in myfiles:
	with open(x) as input_data:
		print (x)
		# setting all variables to None before going into loop
		projid=percom=hourscom=rateproposalease=ratepropdocs=ratesc2itc=ratehetitc=ratepross=rateotinstall=rateotease=rateotdocs=rateotsupport=rateompdownload=ratecadcdownload=ratestarinstall=ratestarlink=ratehetdocs=ratesc2docs=rateoracdr=ratescienceproduct=ratedataquality=ratecompletion=ratepublicationprob=ratefop=rateomp=rateweb=None
		for line in input_data:
			if "TEST" in line: #IGNORE ANY TEST FILES THAT EXIST 
# 				print ("need to skip TEST FOUND!!!!!")
				break
			if "Reference number" in line:
				projid = repr((line.split(":"))[1].strip())
# 				print (projid)
# 				print (type(projid))
			if "Percentage Completed:" in line:
				percom = float((line[-7:-2]).strip())
			if "Completion of project in terms of hours:" in line:
				hourscom = float((line.split(":"))[1].strip())
 				
			## PROPOSAL SYSTEM RATINGS

			if "Please rate proposal system ease of" in line:
				rateproposalease = ratings[(line.split(":"))[1].strip()] 
			if "rate documentation.:" in line: ####
				ratepropdocs = ratings[(line.split(":"))[1].strip()]
			if "SCUBA-2 ITC" in line: ####
				ratesc2itc = ratings[(line.split(":"))[1].strip()]
			if "heterodyne ITC" in line: ####
				ratehetitc = ratings[(line.split(":"))[1].strip()]
			if "observatory staff support" in line: ####
				ratepross = ratings[(line.split(":"))[1].strip()]
				
			## JCMT OT - MSB PREPARATION
			
			if "OT installation" in line: 
				rateotinstall =  ratings[(line.split(":"))[1].strip()] 
			if "OT ease of use.:" in line:
				rateotease =  ratings[(line.split(":"))[1].strip()] 
			if "OT documentation.:" in line: 
				rateotdocs =  ratings[(line.split(":"))[1].strip()] 
			if "OT support.:" in line:  
				rateotsupport =  ratings[(line.split(":"))[1].strip()] 
				
			## DATA ACQUISITION/DATA REDUCTION
			
			if "OMP interface to download your data.:" in line: 
				rateompdownload = ratings[(line.split(":"))[1].strip()] 
			if "CADC interface for searching the JCMT Science Archive and downloading data.:" in line:
				ratecadcdownload = ratings[(line.split(":"))[1].strip()] 
			if "Starlink software installation.:" in line:
				ratestarinstall = ratings[(line.split(":"))[1].strip()] 
			if "Starlink software packages for analysis, reduction, and visualisation.:" in line:
				ratestarlink = ratings[(line.split(":"))[1].strip()] 
			if "heterodyne data reduction documentation.:" in line: 
				ratehetdocs = ratings[(line.split(":"))[1].strip()] 
			if "SCUBA-2 data reduction documentation.:" in line: 
				ratesc2docs = ratings[(line.split(":"))[1].strip()] 
			if "data reduction pipelines (ORAC-DR).:" in line: 
				rateoracdr = ratings[(line.split(":"))[1].strip()] 
			if "science-products of the data reduction pipelines.:" in line:  
				ratescienceproduct = ratings[(line.split(":"))[1].strip()] 
			
			## SCIENCE
				
			if "quality of data obtained.:" in line:
	 			ratedataquality = ratings[(line.split(":"))[1].strip()] 
	 		if "usefulness of data collected/level of completeness" in line:
	 			 ratecompletion = ratings[(line.split(":"))[1].strip()] 
	 		if "likelihood of data leading to publication" in line: 
	 		 	ratepublicationprob = ratings[(line.split(":"))[1].strip()] 
	 			
	 		## GENERAL
	 		
			if "level of communication with your Friend of Project.:" in line:
# 				print (line)
				ratefop = ratings[(line.split(":"))[1].strip()] 
			if "ease and usefulness of OMP project home page.:" in line:
# 				print(line)
	 			rateomp = ratings[(line.split(":"))[1].strip()] 
	 		if "satisfied were you with the web site.:" in line:
	 			rateweb = ratings[(line.split(":"))[1].strip()] 		

		# saving the ratings from each file into my new table:
	 	t.add_row((percom,hourscom,rateproposalease,ratepropdocs,ratesc2itc,ratehetitc,ratepross,rateotinstall,rateotease,rateotdocs,rateotsupport,rateompdownload,ratecadcdownload,ratestarinstall,ratestarlink,ratehetdocs,ratesc2docs,rateoracdr,ratescienceproduct,ratedataquality,ratecompletion,ratepublicationprob,ratefop,rateomp,rateweb))
# 	 	t.add_row((projid,percom,hourscom,rateproposalease,ratepropdocs,ratesc2itc,ratehetitc,ratepross,rateotinstall,rateotease,rateotdocs,rateotsupport,rateompdownload,ratecadcdownload,ratestarinstall,ratestarlink,ratehetdocs,ratesc2docs,rateoracdr,ratescienceproduct,ratedataquality,ratecompletion,ratepublicationprob,ratefop,rateomp,rateweb))

	 		 	
print(t)




# -------------------------------------------- #
#      plotting info from report files         #
# -------------------------------------------- #

# in essence I want one plot to show median value (as a bar) and SD (as an error bar) for each rating.


