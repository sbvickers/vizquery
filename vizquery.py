#! /usr/bin/env python3

import subprocess
import configparser
import argparse
import os

def make_query(config):
    """
        Returns a dictionary of parameters to fill a VizieR query using the 
        vizquery program (see. http://cdsarc.u-strasbg.fr/doc/vizquery.htx for
        more info)

        Parameters
        --------
                config : configparser
                configparser object of an input ini file with the parameters of
                the query

        Returns
        --------

                query : dictionary
                query is a dictionary of all the parameters for the VizieR query
    """

    query = {}

    items = ['object', 'radius', 'max_out', 'source', 'output', 'mime', 'sort']

    for item in items
        query[item] = str(config[item])

    return query

def get_list(filename):
    """
        gets a list of objects from a csv file then returns a list

        Parameters
        ---------
                filename : string
                Name of the file with object names/coordinates.

        Returns
        --------
                names : list
                List of the names/coordinates of the objects in the file.
    """

    import csv

    names = []

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            names.append(row[0])

        f.close()

    return names

def do_query(q_params, ignores):
    """
        Performs a vizieR query using the cdsclient then pips the output
        removing extraneous lines and returning only the required data.

        Parameters
        ---------
                q_params : dictionary
                Dictionary of parameters for the query.

                ignores : list
                List of strings to ignore when cycling through rows of data.

        Returns
        ---------
                data : list
                A list of the required data fields or None if no data found.
    """

    query = "vizquery -source='{source}' -c='{object}' -c.rs='{radius}' -out='{output}' -sort='_r' -out.max='{max_out}' -mime='{mime}'".format(**q_params)

    (output, err) = subprocess.Popen(query, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()

    rows = output.decode('utf-8').split('\n')

    for row in rows:
        if (row) and not any([x in row for x in ignores]):
            return row.split(';')

    return None

def save_data(data, filename):
    """
        Saves the data to a file where the filename has been defined in the .ini
        file.

        Parameters
        ----------
                data : list
                A list of the name/coordinates and the data that has been
                requested in the .ini file.

                filename : string
                The name of the file to write the data too.

        Returns
        ----------
                None
    """
    with open(filename, 'a') as f:
        string = "{}" + ", {}" * (len(data) - 1) + " \n"
        string = string.format(*data)
        f.write(string)

        f.close()

def get_data(q_params, config):
    """
        Takes either a list of objects or a single object and queries VizieR for
        the specified data and then saves it to an output file.

        Parameters 
        ----------
                q_params : dictionary
                A dictionary of the parameters to use in the query.

                config : configparser
                A configparser object used to get the parameters from the .ini
                config file.

        Returns
        ----------
                None
    """

    out_list = [str(x) for x in config['query']['outputs'].split()]
    header = ['name/pos'] + out_list
    ignores = ['---', '#'] + out_list + [str(x) for x in config['processing']['units'].split()]

    print( header )

    if not q_params['object']:
        names = get_list(str(config['files']['in_file']))
        out_file = str(config['files']['out_file'])

        if os.path.exists(out_file):
            import datetime as dt
            append = str(dt.datetime.now()).split('.')
            out_file = out_file + "_{}".format(append[len(append)-1])

        save_data(header, out_file)

        for name in names:
            q_params['object'] = name
            data = do_query(q_params, ignores)

            if data:
                data = [name] + data
                save_data(data, out_file)
            else:
                save_data([name] + ['---'] * len(out_list), out_file)

            print( data )

    else:
        data = do_query(q_params, ignores)
        print( data )

def run_query(filename):
    """
        This is the function that can be called to run the VizieR query when
        importing the module into another module.

        Parameters
        ----------
                filename : string
                The filename of the .ini config file with the parameters for the
                query.

        Returns
        ----------
                None
    """

    config = configparser.ConfigParser()
    try:
        config.read(filename)
    except configparser.NoSectionError as e:
        print( "{} is not a valid input file.".format(args.input_file))
    else:
        q_params = make_query(config['query'])
        get_data(q_params, config)

def main():
    """
        This is the main function called when this script is run directly from
        the terminal. 

        The script requires an input for the config file which can be given by
        
            ./vizquery.py -i 2mass.ini

            or

            python vizquery.py -i 2mass.ini

        This function  performs the same operations as run_query().

        Parameters
        ----------
                None

        Returns
        ----------
                None
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', type=str, dest='input_file', help='Specify input ini file with the query parameters.')
    args = parser.parse_args()

    assert args.input_file, "Input file not defined."
    assert os.path.exists(args.input_file), "No such file exists." 

    config = configparser.ConfigParser()

    try:
        config.read(args.input_file)
    except configparser.NoSectionError as e:
        print( "{} is not a valid input file.".format(args.input_file))
    else:
        q_params = make_query(config['query'])
        get_data(q_params, config)

if __name__ == '__main__':
    main()

