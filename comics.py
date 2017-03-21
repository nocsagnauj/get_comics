#!/usr/bin/env python3

"""
This file downloads comics images from gocomics.com
The script is done in 'for' loops

The date and comic names are written in solid in the code
Next steps are:
 - iterate all the comics from a list
 - read from a config file or CLI the comic name, the start and end dates
 - read from environnement values so we can put this script in a docker file

 The environnement variables will be:
DEFAULT_DEST_ROOT_PATH
DEFAULT_SITE_PATH
DEFAULT_COMICS
COMIC-NAME_COMIC_URL_NAME
(i.e. BIGNATE_COMIC_URL_NAME)

"""

import os
import calendar
import urllib.request as urlrq
import argparse
from configparser import ConfigParser
from configparser import ExtendedInterpolation
from configparser import NoSectionError, NoOptionError

#Default values for parameters:
CODE_CONFIG_FILE = "./comics.ini"
CODE_DEFAULT_DEST_ROOT_PATH = "/tmp/comics_strips/"
CODE_DEFAULT_SITE_PATH = "http://www.gocomics.com/"
#Give list of comics to retrieve in UPPERCASE
CODE_DEFAULT_COMICS = "BIGNATE, PEARLSBEFORESWINE"


def parse_args():
    """
    Parse config file to retrieve program parameters
    """
    parser = argparse.ArgumentParser(
        description='Get CLI arguments for retrieving comics from gocomics.com',
        epilog='The options in the config_file can be passed as environnement values. \
                The env values have the format SECTION_KeyName.')
    parser.add_argument('--config_file',
                        type=str,
                        required=False,
                        default=CODE_CONFIG_FILE,
                        help='File with the parameters to retrieve \
                        the wished comics from gocomics.com')
    return parser.parse_args()

def get_parameter_from_sources(section_name, key_name, config_file):
    """
    Returns the value of 'section_name_key_name' parameter from
    the environnement values or from 'config_file'
    """
    parameter_full_name = section_name + '_' + key_name
    print("Let's try to find the parameter: {}".format(parameter_full_name))
    try:
        param_value = os.environ[parameter_full_name]
        print("Param_value from os is: {}".format(param_value))
    except KeyError: #Value not found in environnement values
        print("{} parameter is not in environnement values".format(parameter_full_name))
        #section_name,separator,key_name = parameter.partition('_')
        params = ConfigParser(interpolation=ExtendedInterpolation())
        params.read(config_file)
        try:
            param_value = params.get(section_name.upper(), key_name)
        except:
            print('\n////////////////////////////////')
            print("Unable to get the comic URL for comic: {}".format(section_name))
            print("Please set it as an environnement value or")
            print("as a key in its section of the config file.")
            print('////////////////////////////////\n')
            raise
    return param_value

#Creates the comic url in iterative way
if __name__ == "__main__":
    comics_params = ConfigParser(interpolation=ExtendedInterpolation())
    comics_params.read(parse_args().config_file)

    dest_root_path = get_parameter_from_sources('DEFAULT', 'DEST_ROOT_PATH', parse_args().config_file)
    #dest_root_path = comics_params.get('DEFAULT', 'DEST_ROOT_PATH')
    if dest_root_path[-1] != '/':
        dest_root_path += '/'
    #SITE_PATH = comics_params.get('DEFAULT','SITE_PATH')
    comics_list = comics_params.get('DEFAULT', 'COMICS').split(',')

    #print("Comics list: ", comics_list)

    mycal = calendar.Calendar()

    for current_comic in comics_list:
        current_comic = current_comic.strip()
        #comic_url_name = comics_params.get(current_comic.upper(),'COMIC_URL_NAME')
        try:
            comic_url_name = get_parameter_from_sources(current_comic.upper(),
                                                        'COMIC_URL_NAME',
                                                        parse_args().config_file)
        except NoSectionError:
            print('/'*40)
            print("Section {} was not found in INI file: {}".format(current_comic.upper(),
                                                                    parse_args().config_file))
            print('/'*40+'\n')
            #there was an exception, continue to next comic in comics_list
            continue
        except NoOptionError:
            print('/'*40)
            print("Parameter {} was not found in Section {}".format('COMIC_URL_NAME',
                                                                    current_comic.upper()))
            print('/'*40+'\n')
            #there was an exception, continue to next comic in comics_list
            continue
            #comic_url_name = CODE_DEFAULT_SITE_PATH + current_comic.lower()

        if comic_url_name[-1] == '/':
            comic_url_name = comic_url_name[:-1]
        comic_name = current_comic.lower()

        dest_path = dest_root_path+comic_name+'/'
        try:
            os.makedirs(dest_path)
        except OSError:
            print("Directory {0} already exists. Kudos for preparing the field.".format(dest_path))

        for year in range(2017, 2018):
            for month in range(1, 2):
                #if year==2014 and month<4:
                #    continue
                days = mycal.itermonthdays(year, month)
                for d in days:
                    if d > 0:
                        url_comic = comic_url_name + "/{0}/{1:02d}/{2:02d}".format(year, month, d)
                        #print (url_comic)

                        html_comic = urlrq.urlopen(url_comic)
                        html_comic_str = str(html_comic.read())
                        point_line = html_comic_str.find('data-image=')
                        start_url_img = html_comic_str.find("\"", point_line)+1
                        end_url_img = html_comic_str.find("\"", start_url_img)
                        url_img = html_comic_str[start_url_img:end_url_img]
                        #print (url_img)

                        html_img = urlrq.urlopen(url_img)
                        header_html_img = html_img.getheader('Content-Disposition')
                        point_filename = header_html_img.find('filename=')
                        start_filename = header_html_img.find("\"", point_filename)+1
                        end_filename = header_html_img.find("\"", start_filename)
                        full_filename = header_html_img[start_filename:end_filename]

                        #rename the comic with comic name instead of 'bn' or 'pb'
                        filename = comic_name+'20'+full_filename[2:]
                        print(filename)

                        urlrq.urlretrieve(url_img, dest_path+filename)
