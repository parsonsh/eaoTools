#!/Users/hparsons/anaconda/bin/python
'''
this code will take a file containing: 
	first_name last_name email@address
and return a file containing:
	first_name last_name <email@address>,
'''

import argparse

parser = argparse.ArgumentParser(description="This program's aim is to produce  \
								usable format of email lists",
								usage="email_convert.py")							
parser.add_argument("-f", "--files",
					dest="files",
					default=None,
					help="the file containing a list of names/emails to process")
args = parser.parse_args()
if (args.files == None):
    parser.print_help()
else:
	print ("\n	file provided: {0}\n".format(args.files)) # this is my input file	


# datain = open(args.files,'r') # r = read - but this is lazy way
#dataout = open('chimps-google-email.list','w') # w = write - but this is lazy way

with open(args.files,'r') as datain: # better (will close the file after)
	dataout=''.join(["reformatted-",args.files])
	print ("	file produced: {}\n".format(dataout)) # this is my input file
	with open(dataout,'w') as dataout:

		for line in datain:
			if (line[0] == '#'):
				pass
			else:
				values = line.strip().split()
				inputs = len(values)
				names = values[0:(inputs-1)]
				allnames = ' '.join(names)
				email = values[(inputs-1)]
				print ("{} <{}>".format(allnames,email))
				dataout.write("{} <{}>,\n".format(allnames,email))
