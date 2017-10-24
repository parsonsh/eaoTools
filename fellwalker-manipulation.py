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
import astropy
from astropy import units as u
from astropy.table import vstack, Table


# ----------------------------------------------------------------------------------- #
# First I need to produce the 5th order polynomial fit needed for aperture correction #
#    see also: https://stackoverflow.com/questions/18767523/fitting-data-with-numpy   #
# ----------------------------------------------------------------------------------- #

# input data:

datatable = "/Users/hparsons/Documents/git/eaoTools/sc2-appeture-correction.txt"

# output plot:

figname = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850-aperture-correction.png"


# reading in the data table

tablein = astropy.io.ascii.read(datatable, names=('d', '450', '850'))

# plotting and fitting to the data:

plt.figure(figsize=(10,8))

plt.xlabel('aperture size (arcsec)', fontsize=15)
plt.ylabel('850um apertre correction factor', fontsize=15)
plt.scatter(tablein['d'], tablein['850'], marker = 'o')

x = np.asarray(tablein['d'], dtype=float)
y = np.asarray(tablein['850'], dtype=float)

print (x)
print (y)

import numpy.polynomial.polynomial as poly

x_new = np.linspace(x[0], x[-1], num=len(x)*10)
coefs = poly.polyfit(x, y, 5)
ffit = poly.polyval(x_new, coefs)


plt.title('5th order polynomial fit \n to 850um aperture correction \n {}'.format(coefs), fontsize=12)
plt.plot(x_new, ffit)

#print (coefs)

plt.savefig(figname) # saves the current figure
plt.close()

# ----------------------------------------------------------------------------------- #
#                               Setting up my 850 data                                #
# ----------------------------------------------------------------------------------- #

# input data:

inspecting = ('FELLWALKER')

# inspecting = 'ATLASGAL'

# inspecting = 'ATLASGALCONV'

if inspecting == 'FELLWALKER':
	# if looking at the fellwalker data look in:
	datafile = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850um_corr_map_cal-beam_findclump_extractclumps_matched_and_contamination.csv"
	datain = astropy.io.ascii.read(datafile, names=('PIDENT_1','Peak1_1','Peak2_1','Cen1_1','Cen2_1','Size1_1','Size2_1','Sum_1','Peak_1','Area_1','PIDENT_2','Peak1_2','Peak2_2','Cen1_2','Cen2_2','Size1_2','Size2_2','Sum_2','Peak_2','Volume_2','sum_var','PIDENTCon','contam'))
	# if looking at fellwalker data read out: BOTH a latex .tex file and a csv file
	dataoutfilename = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850um_fellwalker_out.tex"
	dataoutcsv = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850um_fellwalker_out.csv"
	print ('inspecting {}'.format(inspecting))
	print ('data in = {}'.format(datafile))
	print ('csv out = {}'.format(dataoutcsv))

if inspecting == 'ATLASGAL':
	datafileA = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850um_corr_map_cal-beam_findclump_extractclumps_matched_ATLASGAL.ascii"
	datain = astropy.io.ascii.read(datafileA, names=('atlas_name','gal_long_peak','gal_lat_peak','gal_long_centre','gal_lat_centre','major','minor','pa','effective_radius','peak_flux','peak_flux_error','int_flux','int_flux_error','flags','SNR','PIDENT_1','Peak1_1','Peak2_1','Cen1_1','Cen2_1','Size1_1','Size2_1','Sum_1','Peak_1','Area_1','PIDENT_2','Peak1_2','Peak2_2','Cen1_2','Cen2_2','Size1_2','Size2_2','Sum_2','Peak_2','Volume_2','Seperation'))
	# if looking at the ATLASGAL data read out: a csv file
	dataoutcsv = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850um_fellwalker_out_ATLASGAL.csv"
	print ('inspecting {}'.format(inspecting))
	print ('data in = {}'.format(datafileA))
	print ('csv out = {}'.format(dataoutcsv))	

if inspecting == 'ATLASGALCONV':
	# if looking at the ATLASGAL data look in:
	datafileAC = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850um_corr_map_cal-beam-convolved-to-ATLASGAL_findclump_extractclumps_matched_ATLASGAL.ascii"
	datain = astropy.io.ascii.read(datafileAC, names=('atlas_name','gal_long_peak','gal_lat_peak','gal_long_centre','gal_lat_centre','major','minor','pa','effective_radius','peak_flux','peak_flux_error','int_flux','int_flux_error','flags','SNR','PIDENT_1','Peak1_1','Peak2_1','Cen1_1','Cen2_1','Size1_1','Size2_1','Sum_1','Peak_1','Area_1','Seperation'))
	# if looking at the ATLASGAL data read out: a csv file
	dataoutcsv = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850um_fellwalker_out_convolved-to-ATLASGAL.csv"
	print ('inspecting {}'.format(inspecting))
	print ('data in = {}'.format(datafileAC))
	print ('csv out = {}'.format(dataoutcsv))



# new table values needed:


if inspecting == 'FELLWALKER':
	datain['Peak_error'] = datain['Peak_1'] / datain['Peak_2']	# peak error - only fellwalker data has data and error info
	datain['contamination'] = datain['contam']*100.0


names = []													# source name
for a, b in zip(datain['Peak1_1'], datain['Peak2_1']):
    if b <= 0:
        names.append( "G{0:07.3f}{1:07.3f}".format(a,b))
    else:   
        names.append("G{0:07.3f}+{1:06.3f}".format(a,b))
datain['Name'] = names


datain['Reff'] = np.sqrt(datain['Area_1'] / math.pi) 		# effective source radius
datain['Deff'] = datain['Reff']*2.0							# effective source aperture



# ----------------------------------------------------------------------------------- #
#                    Applying aperture correction to my 850 data                      #
# ----------------------------------------------------------------------------------- #


Sum_1_apcorrected = []

# correcting for apperture size

for sum, d in zip(datain['Sum_1'], datain['Deff']):
	if (d > 20) and (d < 125):
		correction850 = poly.polyval(d, coefs)			
		Sum_1_apcorrected.append(sum/correction850/1000.0) # convert from mJy to Jy
	if (d > 125):
		Sum_1_apcorrected.append(sum/1.09/1000.0) # convert from mJy to Jy

# correcting for sum_1 being in units Jy/beam*pixel 

beamwidth  = 14.6 # arcsec
pix_length = 6.0  # arcsec

sigma=np.sqrt((-(beamwidth/2.0)**2.0)/(2.0*np.log(0.5))) 

beam_area=2.0*np.pi*sigma**2.0                                                                                                                                                                                          

#Find the number of pixels in a beam                                                                                                                                                                                    

pixels_in_beam = beam_area/pix_length**2                                                                                                                                                                                

#convert from jy/beam*pixel to jy/pixel*pixel (=jy)

jyperpixel=Sum_1_apcorrected/pixels_in_beam                                                                                                                                                                                 

datain['Sum_1_corrected'] = jyperpixel * u.Jy	# set units to Jy

if inspecting == 'FELLWALKER':
	datain['sum_var_corrected']=datain['sum_var']/pixels_in_beam  



# ----------------------------------------------------------------------------------- #
#            calculating back of the envelope concentration estimate                  #  
#                        with help from Steve Mairs                                   #
# ----------------------------------------------------------------------------------- #


if inspecting == 'FELLWALKER':
	datain['Concentration'] = 1 - (1.13*beamwidth**2.0*datain['Sum_1_corrected']/(np.pi*datain['Reff']**2.0*(datain['Peak_1']/1000)))


# ----------------------------------------------------------------------------------- #
#                making compact source catalogue (CSV and Latex)                      #
# ----------------------------------------------------------------------------------- #

datain.sort('Peak1_1')

# initially with no formatting for the csv file:


if inspecting == 'FELLWALKER':
	print (dataoutcsv)
	tableout = []
	tableout = (datain['PIDENT_1'],datain['Name'], datain['Peak1_1'], datain['Peak2_1'], datain['Cen1_1'], datain['Cen2_1'], datain['Reff'], (datain['Peak_1']/1000), (datain['Peak_error']/1000), datain['Sum_1_corrected'], datain['sum_var_corrected'], datain['Peak_2'], datain['Concentration'],datain['contamination'])
	dataout = Table(tableout, names=['PIDENT','Name','l_max','b_max','l','b','Reff','S_peak ','S_peak_error','S_int','S_int_error','SNR','C','contamination'])
	astropy.io.ascii.write(dataout, dataoutcsv, format='csv', overwrite=True)

	# with formatting for the latex publication file:

	datain['Peak1_1'].format = '%.3f'
	datain['Peak2_1'].format = '%.3f'
	datain['Cen1_1'].format = '%.3f'
	datain['Cen2_1'].format = '%.3f'

	datain['Reff'].format = '%.0f'
	datain['Peak'] = (datain['Peak_1']/1000.0)
	datain['Peak_e'] = (datain['Peak_error']/1000.0)
	datain['Peak'].format = '%.2f'
	datain['Peak_e'].format = '%.2f'
	datain['Sum_1_corrected'].format = '%.2f'
	datain['sum_var_corrected'].format = '%.2f'
	datain['Peak_2'].format = '%.1f'
	datain['Concentration'].format = '%.2f'
	datain['contamination'].format = '%.0f'

	tableout = []
	tableout = (datain['Name'], datain['Peak1_1'], datain['Peak2_1'], datain['Cen1_1'], datain['Cen2_1'], datain['Reff'], datain['Peak'], datain['Peak_e'], datain['Sum_1_corrected'], datain['sum_var_corrected'], datain['Peak_2'], datain['Concentration'],datain['contamination'])
	dataout = Table(tableout, names=['Name','l_max','b_max','l','b','Reff','S_peak ','S_peak_error','S_int','S_int_error','SNR','C','Con'])
	astropy.io.ascii.write(dataout, dataoutfilename, format='latex', overwrite=True)
	astropy.io.ascii.write(dataout, dataoutcsv, format='csv', overwrite=True)
	print (dataout)

if (inspecting == 'ATLASGAL') or (inspecting == 'ATLASGALCONV'):
	print (dataoutcsv)
	tableout = []
	tableout = (datain['atlas_name'],datain['gal_long_peak'],datain['gal_lat_peak'],datain['gal_long_centre'],datain['gal_lat_centre'],datain['major'],datain['minor'],datain['pa'],datain['effective_radius'],datain['peak_flux'],datain['peak_flux_error'],datain['int_flux'],datain['int_flux_error'],datain['flags'],datain['SNR'],datain['Name'], datain['Peak1_1'], datain['Peak2_1'], datain['Cen1_1'], datain['Cen2_1'], datain['Reff'], (datain['Peak_1']/1000), datain['Sum_1_corrected'])
	dataout = Table(tableout, names=['atlas_name','gal_long_peak','gal_lat_peak','gal_long_centre','gal_lat_centre','major','minor','pa','effective_radius','peak_flux','peak_flux_error','int_flux','int_flux_error','flags','SNR','Name','l_max','b_max','l','b','Reff','S_peak ','S_int'])
	astropy.io.ascii.write(dataout, dataoutcsv, format='csv', overwrite=True)
