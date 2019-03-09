# Probe-Data-Analysis-for-Road-Slope

### The output file using append mode instead of override mode
### Make sure you delete output csv file every time before you run the code


## format of output files:
### slope.csv format:
##### linkPVID, slopeInfo
#####   linkPVID	is the published versioned identifier for the link.
#####   slopeInfo	contains an array of slope entries consisting of the distance from reference node (in decimal meters) and slope at that point (in decimal degrees). The array entries are delimited by a vertical bar character and the distance from reference node and slope values are separated by a forward slash character (dist/slope|dist/slope). This entire field will be null if there is no slope data for the link.


### evaluateSlope.csv format:
##### linkPVID, Average derive slope, Average surveyed slope, Percentage different
#####   linkPVID	is the published versioned identifier for the link.
#####   Average derive slope	is the derive average slope calculate by each probe data point
#####   Average surveyed slope	is the slope info provide in link data file. It leaves null if no data provide.
#####   Percentage different   is the calculated percentage difference between derive slope and surveyed slope. The null data in surveyed slope convert to 0 for calculate convenience. 
