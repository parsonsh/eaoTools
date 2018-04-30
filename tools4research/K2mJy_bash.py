def K2mJy(weather,MODE = 'tau225',WAVELENGTH = 850):
    '''

    This function was developed by Dr. Harriet Parsons in her paper: The Dusty Galactic Center as Seen by SCUBA-2.
    The paper was accepted by ApJ in late 2017.

    in         = tau225 or PWV. Set the kwarg MODE appropriately.

    out        = The conversion factor to transform K*km/s into mJy/beam 
    

    *** KWARGS

    MODE       = 'tau225'. Choice of 'tau225' of 'PWV' (STR). 
    WAVELENGTH = 850.      Choice of 450 or 850 (INT or STR).


    '''

    import numpy as np

    
#    print ('\n\n The factor that will be derived converts a map which is in K*km/s to mJy/beam.\n \
#    \t You have selected a wavelength of '+str(WAVELENGTH)+' microns. \n \
#    \t The input weather grade is expressed as '+MODE+'.\n')

    ###
    # First, figure out if we are working at 450 or 850 microns and build the function coefficients
    ###

    try:

        if np.logical_or(WAVELENGTH == 850, WAVELENGTH == '850'):
            alpha   = 0.574
            beta    = 0.1151  
            gamma   = 0.0485
            delta   = 0.0109
            epsilon = 0.000856

        elif np.logical_or(WAVELENGTH == 450, WAVELENGTH == '450'):
            alpha   = 0.761
            beta    = 0.0193
            gamma   = 0.0506
            delta   = 0.0141
            epsilon = 0.00125

        test = alpha*beta

    ###
    # Raise an exception if the user entered an invalid wavelength
    ###

    except NameError:

        print('\n'+str(WAVELENGTH)+' is not a valid wavelength. Acceptable values: 450 or 850. Can be entered as a STR or an INT.\n')

    ###
    # Now make sure we have a PWV value - convert tau225 to PWV if the user enters a tau225 value
    ###

    try:

        if MODE == 'tau225':
            PWV = (weather - 0.017) / 0.04 # mm
        elif MODE == 'PWV':
            PWV = weather

    ###
    # Raise an exception is they did not specify a correct input weather mode.
    ###

    except NameError:
        print ('\n'+MODE+' is not a valid mode. Must be "tau225" or "PWV"\n')


    ###
    # Calculate the conversion factor
    ###
    
    C = alpha + beta*PWV - gamma*PWV**2 + delta*PWV**3 - epsilon*PWV**4 # (mJy beam^-1) / (K km s^-1) 

    #print ('\n Conversion Factor calculated! \n C_'+str(WAVELENGTH)+' = '+str(C,5)+'\n')

    print (C)

    return (C)
