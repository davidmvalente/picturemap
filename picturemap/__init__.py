from .parsemetadata import *
from json import dump
import sys
import os, subprocess


def build(data, target):
    #Copy basemap file to target_directory
    with open(os.path.dirname(__file__)+'/basemap.html', 'r') as inputhtml:
        with open(target+'/picturemap.html', 'w') as outputhtml:
            print('Writing '+target+'/picturemap.html')
            for line in inputhtml:
                outputhtml.write(line)
    #Export data to JSON
    with open(target+'/picturemap_data.json', 'w') as outfile:
        print('Writing '+target+'/picturemap_data.json')
        outfile.write('var picturemap_obj = ')
        dump(data, outfile, sort_keys=True)

def launch(filepath):
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', filepath))
    elif os.name == 'nt': # For Windows
        os.startfile(filepath)
    elif os.name == 'posix': # For Linux, Mac, etc.
        subprocess.call(('xdg-open', filepath))

def set_centre(coordinates):
    return [sum(i)/len(i) for i in zip(*coordinates)] #Average coordinates

def get_metadata(filenames, target_directory):
        data_array = []
        for f in filenames:
            name = str(os.path.relpath(f, target_directory)) #Relative path to file
            date, coordinates = process(f)
            if coordinates[0] != None and coordinates[1] != None:
                data_array.append((name,date,coordinates))
        result = {k:d for d,k in zip(zip(*data_array),['names','dates','coordinates'])}
        print(str(len(result['names']))+' images have been added to the map: ', result['names']) #Debug: to show dataset
        return result

def set_target(paths_to_files):
    target = os.path.dirname(os.path.commonprefix(paths_to_files))
    print('Setting '+str(target)+' as destination path.')
    return target
