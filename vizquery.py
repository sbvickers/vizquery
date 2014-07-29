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
                name of the file to be read.

        Returns
        --------
                names : list
                list of the objects in the file
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

    """
    with open(filename, 'a') as f:
        string = "{}" + ", {}" * (len(data) - 1) + " \n"
        string = string.format(*data)
        f.write(string)

        f.close()

def get_data(q_params, config):
    """
        queries VizieR using the cdsclient and returns the twomass data
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
        Runs the query by importing vizquery into python program

    """

    config = configparser.ConfigParser()
    config.read(filename)

    q_params = make_query(config['query'])

    get_data(q_params, config)

def main():
    """
        main function for testing
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
        quit()

# gets the query dictionary (need to change parameters in this dictionary to
# make different queries)
    q_params = make_query(config['query'])

# gets the first line of actual data from the output
    get_data(q_params, config)

if __name__ == '__main__':
    main()

