#!/local/python/bin/python
'''
This script will grab take the ATLASGAL SCUBA-2 matched data that have had
the apperture correction applied to the peak fluxes and plot a scatter diagram 
'''

import math
import matplotlib.pyplot as plt
import numpy as np
import astropy
from astropy import units as u
from astropy.table import vstack, Table


# ----------------------------------------------------------------------------------- #
#                  the input data - Galactic Centre and ATLASGAL                      #
# ----------------------------------------------------------------------------------- #


# reading in ATLASGAL with SCUBA-2 data file:

datafileA = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850um_fellwalker_out_ATLASGAL.csv"
datainA = astropy.io.ascii.read(datafileA, names=['atlas_name','gal_long_peak','gal_lat_peak','gal_long_centre','gal_lat_centre','major','minor','pa','effective_radius','peak_flux','peak_flux_error','int_flux','int_flux_error','flags','SNR','Name','l_max','b_max','l','b','Reff','S_peak','S_int'])

# reading in ATLASGAL with SCUBA-2 convolved data file:

datafileAC = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850um_fellwalker_out_convolved-to-ATLASGAL.csv"
datainAC = astropy.io.ascii.read(datafileAC, names=['atlas_name','gal_long_peak','gal_lat_peak','gal_long_centre','gal_lat_centre','major','minor','pa','effective_radius','peak_flux','peak_flux_error','int_flux','int_flux_error','flags','SNR','Name','l_max','b_max','l','b','Reff','S_peak','S_int'])


# ----------------------------------------------------------------------------------- #
#                SCUBA-2 peak flux vs integrated flux scatter plot                    #
# ----------------------------------------------------------------------------------- #

# output plot: first SCUBA-2 and ATLASGAL - peak flux

figname = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850-flux-peak-atlasgal-scatter.eps"


plt.figure(figsize=(7,7))
plt.xlabel('SCUBA-2 850 Peak Flux (Jy beam$^{-1}$)')
plt.ylabel('ATLASGAL 870 Peak Flux (Jy beam$^{-1}$)')

plt.loglog(datainA['S_peak'], datainA['peak_flux'], marker = '.',linestyle="None", label='thing', color='black')

plt.loglog([0.1, 5, 10000], [0.1, 5, 10000], ls="--",  label='other thing', color='orange')

plt.xlim(min(0.9*datainA['S_peak']), 1.1*max(datainA['S_peak']))
plt.ylim(min(0.9*datainA['peak_flux']), 1.1*max(datainA['peak_flux']))

#plt.legend(loc='best')

plt.savefig(figname, format='eps') # saves the current figure

plt.close()

# output plot: second SCUBA-2 convolved to ATLASGAL and ATLASGAL - peak flux

figname = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850-flux-peak-atlasgal-convolved-scatter.eps"
 

plt.figure(figsize=(7,7))
plt.xlabel('SCUBA-2 850 Peak Flux Density (Jy beam$^{-1}$)')
plt.ylabel('ATLASGAL 870 Peak Flux Density (Jy beam$^{-1}$)')

plt.loglog(datainAC['S_peak'], datainAC['peak_flux'], marker = '.',linestyle="None", color='black')

plt.loglog([0.1, 5, 10000], [0.1, 5, 10000], ls="--",  label='other thing', color='orange')

plt.xlim(min(0.9*datainA['S_peak']), 1.1*max(datainA['S_peak']))
plt.ylim(min(0.9*datainA['peak_flux']), 1.1*max(datainA['peak_flux']))

plt.savefig(figname, format='eps') # saves the current figure
plt.close()




# output plot: again SCUBA-2 and ATLASGAL - integrated flux

figname = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850-flux-atlasgal-scatter.eps"


plt.figure(figsize=(7,7))
plt.xlabel('SCUBA-2 850 Flux Density (Jy)')
plt.ylabel('ATLASGAL 870 Flux Density (Jy)')

plt.loglog(datainA['S_int'], datainA['int_flux'], marker = 'o',linestyle="None", label='thing', color='black')

plt.loglog([0.1, 5, 10000], [0.1, 5, 10000], ls="--",  label='other thing', color='orange')

plt.xlim(min(0.9*datainA['S_int']), 1.1*max(datainA['S_int']))
plt.ylim(min(0.9*datainA['int_flux']), 1.1*max(datainA['int_flux']))

#plt.legend(loc='best')

plt.savefig(figname, format='eps') # saves the current figure

plt.close()



# output plot: again SCUBA-2 convolved to ATLASGAL and ATLASGAL - integrated flux

figname = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850-flux-atlasgal-convolved-scatter.eps"
 

plt.figure(figsize=(7,7))
plt.xlabel('SCUBA-2 850 Flux Density (Jy)')
plt.ylabel('ATLASGAL 870 Flux Density (Jy)')

plt.loglog(datainAC['S_int'], datainAC['int_flux'], marker = 'o',linestyle="None", color='black')

plt.loglog([0.1, 5, 10000], [0.1, 5, 10000], ls="--",  label='other thing', color='orange')

plt.xlim(min(0.9*datainA['S_int']), 1.1*max(datainA['S_int']))
plt.ylim(min(0.9*datainA['int_flux']), 1.1*max(datainA['int_flux']))

plt.savefig(figname, format='eps') # saves the current figure
plt.close()



