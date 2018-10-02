import parsemetadata
from json import dump
import sys
import os, subprocess

print ('Python version is', sys.version)

def build(data, target):
    #Copy basemap file to target_directory
    with open('resources/basemap.html', 'r') as inputhtml:
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
            date, coordinates = parsemetadata.process(f)
            data_array.append((name,date,coordinates))
        result = {k:d for d,k in zip(zip(*data_array),['names','dates','coordinates'])}
        print(str(len(result['names']))+' images have been added to the map: ', result['names']) #Debug: to show dataset
        return result

def set_target(paths_to_files):
    target = os.path.dirname(os.path.commonprefix(paths_to_files))
    print('Setting '+str(target)+' as destination path.')
    return target


def main():
    #Read arguments
    script = sys.argv[0]
    filenames = sys.argv[1:]
    #Pick destination path for visualization filenames
    target_directory = set_target(filenames)
    #Process files
    pictures_data = get_metadata(filenames, target_directory) #Get name, date, coordinates
    pictures_data['centre'] = set_centre(pictures_data['coordinates']) #Find centre coordinates
    #Build the map
    build(pictures_data, target_directory)
    launch(target_directory+'/picturemap.html')

main()
