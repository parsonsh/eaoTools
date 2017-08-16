#!/local/python/bin/python
'''
This script will grab all data associated with 
a project and produce output files containin the raw data

'''

# if script does not work try and run the following on the command line:
# this should already be in your path but if not...

# bash
# export  SYBASE=/local/progs/sybase
# export PYTHONPATH=/jac_sw/omp/python/lib:$PYTHONPATH
# tcshrc
# setenv SYBASE=/local/progs/sybase
# setenv PYTHONPATH /jac_sw/omp/python/lib


# -------------------------------------------------- #
# setting up ability to grab input from command line #
# -------------------------------------------------- #

import argparse

parser = argparse.ArgumentParser(description="This program's aim is to produce  \
				the files & commandline input for the pi report \
				form email",
				usage="pi-report-form.py")                           
parser.add_argument("-p",
		dest="projectid",
		default=None,
		help="project id (i.e. M17BP084)")
parser.add_argument("-i",
		dest="instrument",
		default=None,
		help="instrument (i.e. POL-2)")
args = parser.parse_args()
if (args.projectid == None) or (args.instrument == None):
	parser.print_help()
else:
	print ("\n    project provided: {0}".format(args.projectid))    
	print ("\n    instrument requested: {0}\n".format(args.instrument))   


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

# ------------------------------------------------------ #
# using an omp database query to grab data for a project #
# ------------------------------------------------------ #


observations = ompdb.get_observations_from_project(projectcode=args.projectid,instrument=args.instrument)

count=1
for i in observations:
	utdat = observations[i].utdate
	obsnum = observations[i].obsnum
	inst = observations[i].instrument
        print ("{} : ls /jcmtdata/raw/scuba2/s8?/{}/{}/*.sdf >> myfiles.list").format(inst,utdat,format(obsnum,"05d"))
	count += 1

#list(observations.keys())

#list(observations.values())

#observations.values()[0]


#for i in observations:
#	print(i)

#observations['scuba2_00013_20170810T063158']

#observations['scuba2_00013_20170810T063158'].obsnum


#ompdb.get_obsid_common('acsis_00010_20170704T102551')

#cominfo = ompdb.get_obsid_common('acsis_00010_20170704T102551')

#cominfo._fields

#cominfo.recipe

#summaryobs = ompdb.get_summary_obs_info_group(semester='17A', queue='PI')

#summaryobs


