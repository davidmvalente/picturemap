from .parsemetadata import *
from json import dump
import sys
import os
import subprocess
from tqdm import tqdm

def build(data, target):
    '''Create a Leaflet.js template 'picturemap.html' file in the target directory and a JSON 'picturemap_data.json' data file. '''
    #Copy basemap file to target_directory
    with open(os.path.dirname(__file__)+'/basemap.html', 'r') as inputhtml:
        with open(target+'picturemap.html', 'w') as outputhtml:
            for line in inputhtml:
                outputhtml.write(line)
    #Export data to JSON
    with open(target+'picturemap_data.json', 'w') as outfile:
        outfile.write('var picturemap_obj = ')
        dump(data, outfile, sort_keys=True)

def launch(filepath):
    '''Run the 'picturemap.html' file'''
    print('Launching ', filepath)
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', filepath))
    elif os.name == 'nt': # For Windows
        os.startfile(filepath)
    elif os.name == 'posix': # For Linux, Mac, etc.
        subprocess.call(('xdg-open', filepath))

def set_centre(coordinates):
    return [sum(i)/len(i) for i in zip(*coordinates)] #Average coordinates

def get_metadata(filenames, target_directory):
        '''Extract GPS and DateTime metadata from a list of picture filenames.'''
        data_array = []
        without_coordinates = 0 # DEBUG:

        for f in filenames:
            name = str(os.path.relpath(f, target_directory)) #Relative path to file
            date, coordinates = process(f) #Does the dirty work!

            if all(x is not None for x in coordinates):
                data_array.append((name,date,coordinates))
            else:
                without_coordinates += 1 ## DEBUG:

        result = {k:d for d,k in zip(zip(*data_array),['names','dates','coordinates'])}
        total_valid_images = test_metadata(result)
        return result

def test_metadata(picture_data):
    '''Assert the shape and content of the data array is correct'''
    if  len(picture_data) < 1:
        raise FileNotFoundError('No images with GPS coordinates found.')

    #Check if data array is properly constructed
    assert 'names' in picture_data
    assert 'dates' in picture_data
    assert 'coordinates' in picture_data

    #Check if all arrays have the same lenght
    total_pictures = set(len(picture_data[key]) for key in picture_data)
    assert len(total_pictures) <= 1
    total_pictures = total_pictures.pop()

    #Check elements are not None
    assert all(name is not None for name in picture_data['names']) == True
    assert all(date is not None for date in picture_data['dates']) == True
    assert all(c[0] is not None and c[1] is not None for c in picture_data['coordinates']) == True

    return total_pictures

def set_target(paths_to_files):
    '''Find highest common directory of all target files.'''
    target = os.path.dirname(os.path.commonprefix(paths_to_files))

    if target == '':
        target = './'
    elif target[-1] != '/':
        target = target+'/'
    else:
        print('Warning!')

    return target
