#!/local/python/bin/python
'''
This script generate the files needed to send an 
ompbulk message to projects (PI and UH) who were
awarded time within a semester.
'''


# -------------------------------------------------- #
# setting up ability to grab input from command line #
# -------------------------------------------------- #

import argparse

parser = argparse.ArgumentParser(description="This program's aim is to produce  \
				the files & commandline input for the pi report \
				form email",
				usage="pi-report-form.py")                           
parser.add_argument("-s",
		dest="semester",
		default=None,
		help="the semester requested (i.e. 17A)")
args = parser.parse_args()
if (args.semester == None):
	parser.print_help()
else:
	print ("\n    semester provided: {0}\n".format(args.semester))    



# -------------------- #
# Specific for Harriet #
# -------------------- #

name = ("Harriet")
ompidname = ("PARSONSH")


# ------------------------------------------------------------------------------------ #
# creating a xxx-comment.txt file to contain the message and contense to sent to users #
# ------------------------------------------------------------------------------------ #

namefile1 = ((args.semester),"comment.txt")
dataout1 = ("-".join(namefile1))
namedataout1 = (dataout1)


with open(dataout1,'w') as dataout1:
	dataout1.write("PI Feedback for past JCMT Semester {}\n \n\
Dear JCMT User\n\n\
Our records indicate you were awarded JCMT science time \
during the past semester. Now that the semester is finished \
we would like to ask for feedback from the PI of each project, \
irrespective of project completion/hours obtained.\n \n\
Your feedback will help inform our future planning for \
improvements to our level of service and support throughout \
your projects lifespan (from MSB creation to data acquisition \
and reduction).  Completion of the form should take no more \
than 5-10 minutes.\n \nThe form can be found at the following \
link: \n \nhttps://www.eao.hawaii.edu/eao-bin/jcmt_pirep.pl \n \n\
We thank you for your time. \n \nBest regards, \n{} \n".format(args.semester,name))


# ------------------------------------------------------------------------- #
# creating a xxx-project.txt file to contain the projects to send emails to #
# ------------------------------------------------------------------------- #


namefile2 = ((args.semester),"projects.txt")
dataout2 = ("-".join(namefile2))
namedataout2 = (dataout2)

# ---------------------------------------------------- #
# setting up the ability to query from the ompdatabase #
# ---------------------------------------------------- #


from omp.db.db import OMPDB
from omp.siteconfig import get_omp_siteconfig

def get_omp_database():
	"""
	Construct a read-only OMP database access object.
	Access comes from the omp site_config file.
	"""

	config = get_omp_siteconfig()
	credentials = 'hdr_database'

	ompdb = OMPDB(
		server=config.get(credentials, 'server'),
		user=config.get(credentials, 'user'),
		password=config.get(credentials, 'password'),
		read_only=True)

	return ompdb


ompdb = get_omp_database() # !!! I need this bit

# ------------------------------------------------------------------------ #
# using an omp database query to grab project ids for file xxx-project.txt #
# ------------------------------------------------------------------------ #


projectids = ompdb.get_projectids(args.semester, telescope='JCMT')

with open(dataout2,'w') as dataout2:
	for x in range(0, len(projectids)):
		instance = (projectids[x])
		if ((instance[4]) == ("P")) or ((instance[4]) == ("H")):
			dataout2.write("{}\n".format(instance))



#support_projects = ompdb.get_support_projects(ompidname, args.semester)




print ("please run the following command to send email to users: \n\nompbulk -comment {} -projects {} -userid {}\n").format(namedataout1,namedataout2,ompidname)

