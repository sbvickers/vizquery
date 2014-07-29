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
                configparser object of an input ini file with the parameters of the
                query
        

        Returns
        --------

                query : dictionary
                query is a dictionary of all the parameters for the VizieR query

    """

    query = {}

    query['object'] = str(config['object'])

    query['radius'] = str(config['radius'])     

    query['max'] = str(config['max_out'])       # maximum number of lines to be return

    query['source'] = str(config['source'])     # catalogue for query

    query['output'] = str(config['outputs'])    # the columns that you actually want

    query['mime'] = str(config['mime'])

    query['sort'] = str(config['sort'])

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

def not_unit(row):
    """
        check if line contains a unit
    """

    units = ['Jy', 'mag', 'mJy', 'cW/m2/nm']

    for unit in units:
        if unit in row:
            return False

    return True

def do_query(q_params, nots):
    """
        performs a vizieR query using the cdsclient then pips the output
        removing extraneous lines and returning only the required data.

        Parameters
        ---------
                q_params : dictionary
                Dictionary of parameters for the query.

        Returns
        ---------
                data : list
                A list of the required data fields.
    """

    query_string = "vizquery -source='{source}' -c='{object}' -c.rs='{radius}' -out='{output}' -sort='_r' -out.max='{max}' -mime='{mime}'"

    query = query_string.format(**q_params)

    (output, err) = subprocess.Popen(query, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()

    rows = output.decode('utf-8').split('\n')

    for row in rows:
        if (row) and not any([x in row for x in nots]):
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

    print( header )

    if q_params['object'] is '':
        names = get_list(str(config['files']['IN_FILE']))

        out_file = str(config['files']['OUT_FILE'])

        if os.path.exists(out_file):
            import datetime as dt
            append = str(dt.datetime.now()).split('.')
            out_file = out_file + "_{}".format(append[len(append)-1])

        save_data(header, out_file)

        for name in names:

            q_params['object'] = name


            data = do_query(q_params, [str(x) for x in config['processing']['nots'].split()] + out_list)
            if data:
                data = [name] + data

                save_data(data, out_file)

            else:
                save_data([name] + ['---'] * len(out_list), out_file)

            print( data )

    else:
        data = do_query(q_params, [str(x) for x in config['processing']['nots'].split()] + [str(x) for x in config['query']['outputs'].split()])

        print( data )
        #save_data(data, config)

    return None

def run_query(filename):
    """
        Runs the query by importing vizquery into python program

    """

    config = configparser.ConfigParser()
    config.read(filename)

    q_params = make_query(config['query'])

    data = get_data(q_params, config)


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
    data = get_data(q_params, config)

if __name__ == '__main__':
    main()

