#!/local/python/bin/python
'''
This script will grab my galactic centre data file
and it will take the area from each source
calculate a effective source radius 'r'
and then apply an appeture correction to the 850um 
flux as taken by Dempsey 2013
for catalogue info see:
http://starlink.eao.hawaii.edu/docs/sun255.htx/sun255se3.html#x4-180003
'''

import math
import matplotlib.pyplot as plt
import numpy as np

datatable = "/Users/hparsons/Documents/git/eaoTools/sc2-appeture-correction.txt"
datafile = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850um_corr_map_cal-beam_findclump_extractclumps_matched.csv"


# ----------------------------------------------------------------------------------- #
# First I need to produce the 5th order polynomial fit needed for aperture correction #
#    see also: https://stackoverflow.com/questions/18767523/fitting-data-with-numpy   #
# ----------------------------------------------------------------------------------- #

dict850 = {}							# creating an empty dictionary
dict450 = {}
with open(datatable,'r') as tablein:	# first setting up aperture values
	line = tablein.readline()			# read the data line by line
	while line[0] == '#':				# any line that is a heading
		line = tablein.readline()		# readline and move on
	for line in tablein:				# data is comma separated line is interpreted automatically as a list
#		print (line)
		(d, F450, F850) = line.split()	# grabbing the data I want from the file
		dict850[int(d)] = (F850)		# inputting values into my 850um dictionary
		dict450[int(d)] = (F450)		# inputting values into my 450um dictionary
		print (d,F850)

#       (key, val) = line.split()
#       dict[int(key)] = val

print (dict850)

data = {"x":[], "y":[]}
for coord in dict850.items():
    data["x"].append(coord[0])
    data["y"].append(coord[1])
    
# display scatter plot data
plt.figure(figsize=(10,8))

plt.xlabel('x', fontsize=15)
plt.ylabel('y', fontsize=15)
plt.scatter(data["x"], data["y"], marker = 'o')

x = np.asarray(data["x"], dtype=float)
y = np.asarray(data["y"], dtype=float)

print (x)
print (y)

import numpy.polynomial.polynomial as poly

x_new = np.linspace(x[0], x[-1], num=len(x)*10)
coefs = poly.polyfit(x, y, 5)
ffit = poly.polyval(x_new, coefs)


plt.title('5th order polynomial fit \n to 850um aperture correction \n {}'.format(coefs), fontsize=12)
#plt.title('5th order polynomial fit to 850um apeture correction {}', fontsize=20).fortmat(coefs)
plt.plot(x_new, ffit)

print (coefs)

#(z1, z2, z3, z4, z5, z6) = np.polyfit(x, y, 5)	# Polynomial coefficients ordered from low to high
#print (z1)										# np.polyfit returns: ... + Ax^2 + Bx + C

#plt.plot(data["x"], , marker = 'o')


figname = ("/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850-aperture-correction.png")
print (figname)
plt.savefig(figname) # saves the current figure


#quit()

# ----------------------------------------------------------------------------------- #
#                    Applying aperture correction to my 850 data                      #
# ----------------------------------------------------------------------------------- #



i = 0 
j = 0 
k = 0 

with open(datafile,'r') as datain:
	line = datain.readline()			# read the data line by line
	while line[0] == 'PIDENT_1':		# any line that is a heading
		line = datain.readline()		# readline and move on

	for line in datain:					# data is comma separated line is interpreted automatically as a list
#		print (line)					# line is a tuple, does not let me use .split()
		row = line.split()				# and having hard time with REGEX
		values = row[0].split(",")		# need to "split" twice as has white space and commas

		PIDENT_1 = float(values[0])		# note wcspar = true was used so values are in arcsec
		Peak1_1 = float(values[1])		# galactic latitude l (degrees)
		Peak2_1 = float(values[2])		# galactic longitude b (degrees)
		Cen1_1 = float(values[3])
		Cen2_1 = float(values[4])
		Size1_1 = float(values[5])		# arcsec
		Size2_1 = float(values[6])		# arcsec
		Sum_1 = float(values[7])		# units mJy
		Peak_1 = float(values[8])		# units = mJy/beam
		Area_1 = float(values[9])		# units = arcsec.arcsec
		Sum_2 = float(values[17])		# sum from SNR map
		Peak_2 = float(values[18])		# peak from SNR map
		Sum_error = Sum_1 / Sum_2
		Peak_error = Peak_1 / Peak_2
		
		Sum_1_corrected = 0				# could use improvement - looks a little "unsafe"
		
		if (Peak2_1 < 0):
			Name = "G{0:07.3f}{1:07.3f}".format(Peak1_1, Peak2_1) 
		else:
			Name = "G{0:07.3f}+{1:06.3f}".format(Peak1_1, Peak2_1)

		r = 1.0 * math.sqrt(Area_1 / math.pi) 	# r = effective source radius
		d = r*2.0								# d = effective source aperture
		

		if (d > 20) and (d < 125): # then we need to use our coefficients
			i = i+1

#			print ('here:: 20 <= {:.2f} < 125'.format(d))
#			print (r, d, correction850)
			correction850 = poly.polyval(d, coefs)			
			Sum_1_corrected = Sum_1/correction850

		if (d > 125): # then we apply the 1.09 correction.
			j = j+1
			
#			print ('here:: {:.2f} >= 125'.format(d))
#			print (r, d, 1.09)
			Sum_1_corrected = Sum_1/1.09
			
		if (d < 20 ): # sanity check - but in this data no sources are less than 20"
			k = k+1


# ----------------------------------------------------------------------------------- #
#                     Producing output table from data provided                       #
# ----------------------------------------------------------------------------------- #
		

#		print ('{11:4}: {0:15} {1:.3f} {2:.3f} {3:.3f} {4:.3f} {5:.0f} {6:.0f} {7:.0f} {8:.2f} {9:.2f} {10:.2f} {11:.1f}'\
#			.format(Name, Peak1_1, Peak2_1, Cen1_1, Cen2_1, Size1_1, Size2_1, r, \
#			Peak_1/1000.0, Peak_error/1000.0, Sum_1_corrected/1000.0, Peak_2, PIDENT_1 ))
		print ('{0:.2f} {1:.2f}'.format(Peak_error/1000.0, Sum_error/1000.0))

#print (i,j,k)	
		
		
		
		
		
		
		