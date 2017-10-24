#!/local/python/bin/python
'''
using this script to do a rational check of
the calucation for mass I'm using values 
in Pattle's 2016 GBS Cepheus paper
for comparison
'''

import math
import numpy as np
from astropy import constants as const
from astropy import units as u
from astropy.modeling.blackbody import blackbody_nu


#### OUR INPUT FROM HER PAPER SOURCE 1:

Sum_1_corrected = 2.31 * u.Jy #### FLUX
Radiuspc = 0.028 *u.pc #### SANITY CHECK USING PATTLE's VALUES !!!!!!!!!!!!
temperature = 10.7 * u.K #### SANITY CHECK USING PATTLE's VALUES !!!!!!!!!!!! 20 or 10.7
distance = 300 * u.pc  #### SANITY CHECK USING PATTLE's VALUES !!!!!!!!!!!! 8000


####### Values specific to this analysis:

wavelength = 850E-6 * u.m				# considering 850um

frequency = wavelength.to(u.Hz, equivalencies=u.spectral())

beta = 2.0								# dust emissivity

distancem = distance.to(u.m) 

kappa = 0.1 * ((frequency/(1E12 *u.Hz))**beta) * (u.cm**2 / u.gram)	# dust mass opacity


print (const.h)
print (const.k_B)

BT =  (2 * const.h * frequency**3.0 / const.c**2.0) * (1/ (np.exp( (const.h*frequency)/(const.k_B*temperature)) - 1.0))
BTunits = BT.decompose().to(u.J/(u.m*u.m))
print (BTunits)


flux_nu = blackbody_nu(wavelength, temperature)
print ('\nwavelength = {}'.format(wavelength))
print ('frequency = {}'.format(frequency))
print ('F850      = {}'.format(Sum_1_corrected))
print ('Distance  = {}'.format(distance))
print ('kappa850  = {}'.format(kappa))
print ('B850(T)   = {}'.format(flux_nu))
print ('Flux int  = {}\n'.format(Sum_1_corrected))



# FIRST CALCULATE MASS:

M = (Sum_1_corrected) * ((distancem)**2.0) / (kappa * BTunits) # converting Sum_1 > W/Hz/m2

print (M)

Msolar_weird = M.decompose().to(u.M_sun)
#Msolar = M/const.M_sun

print ('Mass = {:.2f} \n'.format(Msolar_weird))
