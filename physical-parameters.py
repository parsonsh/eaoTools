#!/local/python/bin/python
'''
This script will eventually grab my galactic centre data 
and produce mass and column density estimates
'''

import math
import matplotlib.pyplot as plt
import numpy as np
import astropy
from astropy import constants as const
from astropy import units as u
from astropy.modeling.blackbody import blackbody_nu
from astropy.coordinates import Angle
from astropy.table import vstack, Table



# ----------------------------------------------------------------------------------- #
#                the input data - Galactic Centre, JPS and ATLASGAL                   #
# ----------------------------------------------------------------------------------- #


# input: Galactic Centre data that has been matched to the median contamination estimates:
# NOTE THIS DOES NOT HAVE FELLWALKER CORRECTION FOR AREA - SO INTEGRATED FLUX IS IN JY/BEAM*AREA

file = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850um_fellwalker_out-with-contamination-values.ascii"
datain = astropy.io.ascii.read(file, names=['PIDENT','Name','l_max','b_max','l','b','Reff','S_peak','S_peak_error','S_int','S_int_error','SNR','PIDENT_C','contamination'])


# input: Median CO contamination estimate by clump number



# ----------------------------------------------------------------------------------- #
#    calculating back of the envelope calculation for column density and mass         #
# ----------------------------------------------------------------------------------- #


wavelength = 850E-6 * u.m										# considering 850um
frequency = wavelength.to(u.Hz, equivalencies=u.spectral())
temperature = 20 * u.K											# typical clump temperature
Distance = 8000.0 * u.pc										# distance to galactic centre
beta = 2.0														# dust emissivity

# CALCULATE DUST MASS OPACIY VALUE @ 850um: 

kappa = 0.1 * ((frequency/(1E12 *u.Hz))**beta) * (u.cm**2 / u.gram) 

# CALCULATE PLANCK CONSTANT Bv(T) VALUE @ 850um:

flux_nu = (blackbody_nu(wavelength, temperature))

# CALCULATE REPRESENTATIVE MASS:

M = (datain['S_peak']* u.Jy) * ((Distance)**2.0) / (kappa * flux_nu)
datain['Msolar_weird'] = M.decompose().to(u.M_sun*u.rad*u.rad)	# somewhere getting a rad*rad

# CALCULATE REPRESENTATIVE EFFECTIVE RADIUS:
	
radius = Angle(datain['Reff'], u.arcsec)			# specifying effective radius is in arcsec
datain['Radiuspc'] = radius.radian * Distance		# effective radius in pc
Radiusm = datain['Radiuspc'].to(u.m)				# effective radius in m

# CALCULATE REPRESENTATIVE COLUMN DENSITY:

mH = 1.008 * const.u 					# mass of Hydrogen
mu = 2.86								# mean molecular weight

NH2 = ((datain['Msolar_weird'])) / ( mH * mu * math.pi * (Radiusm**2))
datain['NH2cm'] = NH2.decompose().to(u.rad*u.rad/u.cm**2)	# following through with the rad*rad

# CALCULATE CONCENTRATION VALUE: - before

# datain['ratio1'] = 1.13*(13.0**2.0)*datain['S_int']
# datain['ratio2'] = math.pi * (datain['Reff']**2.0) * datain['S_peak']
# 
# datain['Concentration'] = 1-(datain['ratio1']/datain['ratio2'])



# ----------------------------------------------------------------------------------- #
#            calculating back of the envelope concentration estimate                  #  
#                        with help from Steve Mairs                                   #
# ----------------------------------------------------------------------------------- #


# Note the beam width and the pixel scale
beamwidth  = 14.6 # arcsec
pix_length = 6.0  # arcsec


def beam2pix(value,pix_length,beamwidth,PIXTYPE='arcsec',BEAMTYPE='arcsecs',DISTANCE=100):
  import numpy as np                                                                       

  #Convert pix_length and beamwidth to arcseconds if they aren't already                                          
  if PIXTYPE=='degrees':                                                                   
    pix_length=206264.806*pix_length*(np.pi/180.0)                                         
  if PIXTYPE=='radians':                                                                   
    pix_length=206264.806*pix_length                                                       
  if PIXTYPE=='parsecs':                                                                   
    pix_length=(pix_length/DISTANCE)*206264.806                                            
  if BEAMTYPE=='degrees':                                                                  
    beamwidth=206264.806*beamwidth*(np.pi/180.0)                                           
  if BEAMTYPE=='radians':                                                                  
    beamwidth=206264.806*beamwidth                                                         

  # We know that Total_Flux = Peak*2*pi*int(x*exp(-x^2/(2*sigma^2))) -- int is evaluated from 0 -> inf 
  # So, by the substitution z =x/sigma (then m=z^2), 
  #our integral evaluates to 1 and we have:  Total_Flux = Peak*2*Pi*sigma^2 = Peak*beam area

  sigma=np.sqrt((-(beamwidth/2.0)**2.0)/(2.0*np.log(0.5))) 
                                                                                                                                                               
  beam_area=2.0*np.pi*sigma**2.0                                                                                                                                                                                          

  #Find the number of pixels in a beam                                                                                                                                                                                    

  pixels_in_beam = beam_area/pix_length**2                                                                                                                                                                                

  #convert from jy/beam to jy/pixel                                                                                                                                                                                       

  jyperpixel=value/pixels_in_beam                                                                                                                                                                                         

  return jyperpixel                                                                                                                                                                                        

datain['Concentration'] = 1 - (1.13*beamwidth**2.0*beam2pix(datain['S_int'],pix_length,beamwidth,PIXTYPE='arcsec')/(np.pi*datain['Reff']**2.0*datain['S_peak']))

print (datain)

# ----------------------------------------------------------------------------------- #
#           creating plots to look at correlations with contamination                 #
# ----------------------------------------------------------------------------------- #

# output plot: SCUBA-2 and contamination - peak flux

figname = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/contamination-850-flux-peak-scatter.eps"


plt.figure(figsize=(7,7))
plt.xlabel('SCUBA-2 850 Peak Flux Density (Jy beam$^{-1}$)')
plt.ylabel('CO contamination (%)')

plt.scatter(datain['S_peak'], datain['contamination']*100.0, marker = '.',linestyle="None", color='black')
plt.xscale('log')

plt.savefig(figname, format='eps') # saves the current figure
plt.close()


# output plot: SCUBA-2 and contamination - integ flux

figname = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/contamination-850-flux-int-scatter.eps"


plt.figure(figsize=(7,7))
plt.xlabel('SCUBA-2 850 Integrated Flux Density (Jy)')
plt.ylabel('CO contamination (%)')

plt.scatter(datain['S_int'], datain['contamination']*100.0, marker = '.',linestyle="None", color='black')
plt.xscale('log')
plt.savefig(figname, format='eps') # saves the current figure
plt.close()

# output plot: column density and contamination - peak flux

figname = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/contamination-column-density-scatter.eps"


plt.figure(figsize=(7,7))
plt.xlabel('N(H$_{2}$) (cm$^{-2}$)')
plt.ylabel('CO contamination (%)')

plt.scatter(datain['NH2cm'], datain['contamination']*100.0, marker = '.',linestyle="None", color='black')
plt.xscale('log')

plt.savefig(figname, format='eps') # saves the current figure
plt.close()

# output plot: mass and contamination - peak flux

figname = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/contamination-mass-scatter.eps"


plt.figure(figsize=(7,7))
plt.xlabel('Mass (M$_{\odot}$)')
plt.ylabel('CO contamination (%)')

plt.scatter(datain['Msolar_weird'], datain['contamination']*100.0, marker = '.',linestyle="None", color='black')
plt.xscale('log')

plt.savefig(figname, format='eps') # saves the current figure
plt.close()


# output plot: compactness and contamination - peak flux

figname = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/contamination-compactness-scatter.eps"


plt.figure(figsize=(7,7))
plt.xlabel('proxy for compactness (Peak Flux Density / Reff)')
plt.ylabel('CO contamination (%)')

plt.scatter((datain['S_peak']/datain['Reff']), datain['contamination']*100.0, marker = '.',linestyle="None", color='black')
plt.xscale('log')

plt.savefig(figname, format='eps') # saves the current figure
plt.close()

# output plot: Reff and contamination - peak flux

figname = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/contamination-reff-scatter.eps"


plt.figure(figsize=(7,7))
plt.xlabel('Reff (")')
plt.ylabel('CO contamination (%)')

plt.scatter((datain['Reff']), datain['contamination']*100.0, marker = '.',linestyle="None", color='black')
#plt.xscale('log')

plt.savefig(figname, format='eps') # saves the current figure
plt.close()

# output plot: concentration and contamination - peak flux

figname = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/contamination-concentration-scatter.eps"


plt.figure(figsize=(7,7))
plt.xlabel('Concentration')
plt.ylabel('CO contamination (%)')

plt.scatter((datain['Concentration']), datain['contamination']*100.0, marker = '.',linestyle="None", color='black')
plt.axvline(0.33, color='k', linestyle='solid')
plt.axvline(0.72, color='k', linestyle='solid')
#plt.xscale('log')

plt.savefig(figname, format='eps') # saves the current figure
plt.close()


# output plot: histogram of contamination

figname = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/contamination-histogram.eps"

datain['c'] = datain['contamination']*100

plt.figure(figsize=(7,7))
hist, bins = np.histogram(datain['c'], bins=30)
width = 0.8 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.bar(center, hist, align='center', width=width, alpha=0.7, facecolor='orange')
plt.xlabel('CO contamination (%)')
plt.ylabel('Number')

plt.savefig(figname, format='eps') # saves the current figure
plt.close()

#print (datain)
