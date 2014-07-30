*********************************************** 
This is a function that can be used to download
data from VizieR at the CDS in much the same 
way as the vizquery function in the astroquery* 
package except that it is quicker, avoids 
server issues and is far simpiler to run.
*********************************************** 

This query script uses the cdsclient which must
be installed as the script makes a command line
call to VizieR using the cdsclient. The 
cdsclient can be found at

    http://cdsarc.u-strasbg.fr/doc/cdsclient.html

and is quite simple to install.

This script can be used by either running it 
directly in the command line and giving the
script an 'ini' config file with the parameters
of the query;

    ./vizquery.py -i 2mass.ini

    or

    python vizquery.py -i 2mass.ini

or via importing the module by

    import vizquery

    or 
    
    import vizquery as ...

then running a query via

    vizquery.run_query(filename)

where the filename is the .ini config file
with the query parameters.

*https://github.com/astropy/astroquery
