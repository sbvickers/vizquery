*********************************************** 
This readme is for the config.ini file required
by the vizquery.py script to run a VizieR query.
*********************************************** 

## **files** ##

The *in_file* is a file with **SIMBAD** resolvable 
object names or coordinates (RA and DEC).

The *out_file* is the file where the output will
be written, if the *out_file* already exists then
data will be written to the *out_file* followed 
by an underscore and some numbers dependent on
the cpu time.

## **query** ##

The *source* is the name of the source in
VizieR i.e. for 2MASS the *source* would be

    II/246/out

and IRAS would be 

    II/125/main.

*object* should remain empty as the script will
only query that object if *object* is not empty.

The *radius* of the query is in arcseconds.

For the *output* all the columns that are desired
should be written here on a single line with a 
space between each column.

The objects are sorted by *radius* from the 
centre of the query.

The total number of results that you want VizieR
to return is given by the *max_out* parameter.

*mime* is just to set the output to a comma 
separated variable format. **do not change**.

## **processing** ## 

The *units* of the output data should be listed
here, this is just to ensure that lines of data
with units in it are removed when cycling through
the lines of data returned from VizieR.

I have included an example .ini file called 2mass.ini
for querying the 2MASS catalogue.
