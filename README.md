# EAO Tools

This is a respository for all useful scrips I use for my EAO/JCMT work.

## tools4research

a directory containing useful modeuls for research purposes

## allreduce-sc2.pl

script used to reduce SCUBA-2 data when provided <ut> <obsid> and <name>. 
data reduced using makemap with the dimmconfig already specified in the script

### calc-density.py

I want this to be the function I call in future for all future density calculations

### calc-mass.py

I want this to be the function I call in future for all future mass calculations

### cal-concentration.py

Yet to be writtien - I want this to be the function I call in future concentration calculations

### email_help.py

This code will take a file containing: 

```
first_name last_name email@address
```

and return a file containing:

```
first_name last_name <email@address>,
```

required for inputting emails into google groups for the Large Programs under open enrollment. 

### fellwalker-apeture-correction.py

Remnant from my Parsons et al. 2017 paper - initially used to calculate the aperture correction for SCUBA-2 data. 

 ### fellwalker-manipulation-plots.py

Scripts I used for my work for Parsons et al. 2017 where I calculated mass, dencisty and concentration estimates.

### fellwalker-manipulation.py

Remnant from my Parsons et al. 2017 paper - to produce the output catalogue files with the physical parameters 

### get-project-data.py

This script will grab all data associated with a project and produce output files containin the raw data

* requires OMP database access (i.e. only runs at EAO)

###  obsrep-collate.py

Script to collate the information produced by the observer report form and produce stats/plots by semester:

```
python obsrep-collate.py -y 2017 -s A
```

### pirep-collate.py

Script to collate the information produced by the pi reports and produce stats/plots by semester:

```
python pirep-collate.py -y 2017 -s A
```

### physical-parameters.py

Script to caluclate a bunch of physical parameters and to plot vs contamination.

### sc2-appeture-correction.txt

requred for fellwalker-apeture-correction.py script. 

### scuba2-atlasgal-plots.py

This script  take the ATLASGAL SCUBA-2 matched data that have had
the apperture correction applied to the peak fluxes and plot a scatter diagram

### user-report-form.py

This script generate the files needed to send an  ompbulk message to projects (PI and UH) who were awarded time within a semester.



