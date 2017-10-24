#!/local/python/bin/python
'''
This script will grab my galactic centre data 
and the JPS data  to create the 
plots needed for my Galactic Centre data paper
'''

import math
import matplotlib.pyplot as plt
import numpy as np
import astropy
from astropy.table import vstack, Table


# ----------------------------------------------------------------------------------- #
#                the input data - Galactic Centre, JPS and ATLASGAL                   #
# ----------------------------------------------------------------------------------- #


# input: Galactic Centre data:

GCfile = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850um_fellwalker_out.csv"
datain = astropy.io.ascii.read(GCfile, names=['PIDENT','Name','l_max','b_max','l','b','Reff','S_peak','S_peak_error','S_int','S_int_error','SNR'])

# input: JPS data:

jpsfile = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/jps_catalogue.csv"
jpsdata = astropy.io.ascii.read(jpsfile, names=('jps_name','iau_id','l_peak','b_peak','l_cen','b_cen','ellipse_major','ellipse_minor','ellipse_pa','effective_radius','peak_flux','peak_flux_error','int_flux','int_flux_error','snr'))

# ----------------------------------------------------------------------------------- #
#                SCUBA-2 peak flux vs integrated flux scatter plot                    #
# ----------------------------------------------------------------------------------- #

# output plot:

figname = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850-flux-flux-scatter.eps"


plt.figure(figsize=(7,7))
plt.xlabel('Peak Flux Density (Jy beam$^{-1}$)')
plt.ylabel('Integrated Flux Density (Jy)')
plt.loglog(datain['S_peak'], datain['S_int'], marker = 'o',linestyle="None",color='black')

plt.loglog([0.1, 5, 10000], [0.1, 5, 10000], ls="--", c="orange", label='other thing')

plt.xlim(min(0.9*datain['S_peak']), 1.1*max(datain['S_peak']))
plt.ylim(min(0.9*datain['S_int']), 1.1*max(datain['S_int']))

plt.savefig(figname, format='eps') # saves the current figure
plt.close()

# ----------------------------------------------------------------------------------- #
#                         log-log flux histograms of SCUBA-2 & JPS                    #
# ----------------------------------------------------------------------------------- #

# output plot:

figname = "/Users/hparsons/Documents/EAO/Research/GalacticCenter/catalogue/850-flux-peak-hist.eps"


# plotting and fitting to the data:

plt.figure(figsize=(7,7))

plt.xlabel('Peak Flux Density (Jy beam$^{-1}$)', fontsize=15)
plt.ylabel('Number', fontsize=15)

#hist, bins = np.histogram((datain['Peak_1']),  bins)#bins=200)
bins = 10**(np.arange(0,2.3,0.05))
# wi dth = 0.8 * (bins[1] - bins[0])
# center = (bins[:-1] + bins[1:]) / 2
# plt.bar(center, hist, align='center', width=width, alpha=0.7, facecolor='orange',log=True)

plt.yscale('log')
plt.xscale('log')


plt.hist((jpsdata['peak_flux']),bins=bins,alpha=0.7, color='blue',lw=1, histtype='bar', rwidth=0.8) 
plt.hist((datain['S_peak']),bins=bins,alpha=1.0, color='orange',lw=1, histtype='bar', rwidth=0.8) 


plt.savefig(figname, format='eps') # saves the current figure
plt.close()







