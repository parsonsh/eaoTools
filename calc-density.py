#!/local/python/bin/python
'''
using this script to do a rational check of
the calucation for column density
I'm using values in Pattle's 2016 GBS 
Cepheus paper for comparison
'''

import math
from astropy import constants as const
from astropy import units as u
from astropy.modeling.blackbody import blackbody_nu


#### TEST - COMPARE VALUES FORM PATTLE's 2016 PAPER:


Radiuspc = 0.028 *u.pc 	#### SANITY CHECK USING PATTLE's VALUES !!!!!!!!!!!!
Mass = 4.78 *u.solMass 	#### SANITY CHECK USING PATTLE's VALUES !!!!!!!!!!!!


Radiusm = Radiuspc.to(u.m)			# effective radius in m
Masskg = Mass.to(u.kg)

#		print (radius,radius.radian,Radiuspc, Radiusm)	


mH = 1.008 * const.u 					# mass of Hydrogen
mu = 2.86								# mean molecular weight


NH2 = Masskg / ( mH * mu * math.pi * (Radiusm**2))

NH2cm = NH2/100**2

print ('\nColumn density (cm-2 not m-2) = {} \n\n\n'.format(NH2cm))
		
