# !/usr/bin/python
# coding=utf-8
import os
import re
import sys
import argparse
import yaml
import jinja2
from jinja2 import Template, PackageLoader, Environment
import requests
requests.packages.urllib3.disable_warnings()
from requests.exceptions import HTTPError, ConnectionError, ProxyError, SSLError, Timeout, ReadTimeout
import logging
import json
import ast
import datetime as dt
import time


_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)
ch = logging.StreamHandler()
_log.addHandler(ch)
formatter = logging.Formatter('%(asctime)s- %(levelname)s - %(message)s')
ch.setFormatter(formatter)


class DataRequester():
    '''Class to do the requests and save the output to a file'''
    
    
    def __init__(self, url, file):
        self.url = url
        self.output_file =file

    def get_data_and_save_to_file(self):
        '''Requests the data from Render API and saves them to a file'''

        try:
            response = requests.get(self.url, verify = False, stream = True)

        except HTTPError as http_err:
            _log.error('HTTP error occurred: {http_err}')

        except ConnectionError as con_err:
            _log.error('ConnectionError occurred: {con_err_err}')

        except Exception as err:
            _log.error('Other error occurred: {err}')
        else:
            #This is prinetd also with some mistakes!!!!
            _log.info('Die Daten wurden erfolgreich gespeichert!')

        try:
            with open(self.output_file, "wb") as file:
                file.write(response.content)
        except IOError as e:
            print ("I/O error({0}): {1}").format(e.errno, e.strerror)



class UrlBuilder():
    '''Class responsible for building the urls'''
    
    
    def __init__(self, requester = DataRequester()):
        self.requester = requester

    def generate_request_data(self):
        '''Creates the last part of the Url using Jinja2 to reference the variables from the confData file (see result of this func:reference_variables_from_config_files()), and calls the the function
        that requests and saves the data'''

        urlsDict = self.create_url_query_string()
        processUserInput = UserInputController()
        args = parse_arguments()
        confData = processUserInput.resolve_variables_from_config_files()
        fromTime = processUserInput.convert_datetime_to_timestamp(args.fromTime)
        toTime = processUserInput.convert_datetime_to_timestamp(args.toTime)
        dir = args.outputdir
        urlWithFormat = ''
        formats = ''

        for title, dataset in confData.iteritems():
            dataset = dataset['formats']
            formats = '{{format}}'
            url = urlsDict[title] + '&format={0}'.format(formats)
            tmp = Template(url)

            for format in dataset:
                urlWithFormat = tmp.render(format=format)
                urlWithFormat = urlWithFormat + '&from=' + fromTime + '&until=' + toTime
                finalUrl = str(urlWithFormat)

                print (finalUrl)

                file = "{0}.{1}".format(title, format)
                directoryFile = os.path.join(dir, file)
                if not os.path.isdir(dir):
                    os.mkdir(dir)

                requester = DataRequester(finalUrl, directoryFile)
                requester.get_data_and_save_to_file()


    def create_url_query_string(self):
        '''Creates the first part of the Url to be used for requesting data from Graphite Server through Render API. The outcome is a list of the final Url s to be used at the requestData function'''

        processUserInput = UserInputController()
        confData = processUserInput.resolve_variables_from_config_files()
        url = processUserInput.args.url
        stable_Url_part = ('{0}graphite/render?').format(url)
        urlQueryStringDict = {}
        item = ''

        for title, dataset in confData.iteritems():
            item = dataset['target']
            urlQueryString = stable_Url_part + "target=" + item

            for key, value in dataset['params'].iteritems():
                urlQueryString = urlQueryString + '&{0}={1}'.format(key, value)
                urlQueryStringDict.update({title : urlQueryString})

        return urlQueryStringDict


class UserInputController():
    '''Class to process the user's input'''
    

    def __init__(self):
        self.args = self.parse_arguments()


    def resolve_variables_from_config_files(self):
        '''Takes the configuration files from user's input and assigns the correct values to the variables with the placeholders, using the Jinja2 template engine. Final outcome is a dict'''

        try:
            self.envConfData = yaml.load(open(os.path.expanduser(self.args.envConfFile)))
        except yaml.YAMLERROR as yml_err:
            _log.error('Error parsing Yaml file: {yml_err}')
        env = Environment(loader=PackageLoader('gather_util_data','templates'),trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(self.args.confFile)


        renderParams = {}
        for key in self.envConfData.keys():
            renderParams[key] = self.envConfData[key]
            results = template.render(renderParams)

        result = ast.literal_eval(results)

        return result



    def convert_datetime_to_timestamp(self, datetimeToConvert):
        '''Converts a datetime object to a timestamp.'''

        try:
            result = time.mktime(dt.datetime.strptime(datetimeToConvert,
                                             "%Y-%m-%d  %H:%M").timetuple())
            return str(int(result))

        except ValueError:
            raise ArgumentTypeError("Given Date {0} not valid".format(datetimeToConvert))



    def parse_arguments():
        '''The argparse module makes it easy to write user-friendly command-line interfaces. The program defines what arguments it requires, and argparse will figure out how to parse those out of sys.argv'''

        data_parser = argparse.ArgumentParser(description='Automate Gather of Utilization Data',
                                              fromfile_prefix_chars='@')

        data_parser.add_argument('-u','--url', help='URL of Graphiteserver',action='store', dest='url',default=None, required=True)
        data_parser.add_argument('-envcfg', '--envConfFile', default=None, help='environment configuration file', metavar="FILE", required=True)
        data_parser.add_argument('-cfg','--confFile', default=None, help='configuration file',
                                metavar="FILE", required=True)
        data_parser.add_argument('-from', '--fromTime', help='start time of the test')
        data_parser.add_argument('-to', '--toTime', help='end time of the test')
        data_parser.add_argument('-dir', '--outputdir',
                                  help='path of the output directory for the data fetched from GraphiteServer')
        data_parser.add_argument('-v', '--verbose', action='count', default=0)


        args = data_parser.parse_args()
        return args
    
    
    def chooseDirectory(self):
    '''Finds an existing directory, if given in CLI uesers input arguments. I not it's creating a new one'''
 
        if os.path.isdir(self.args.dir):
            os.path.exists(path)
        else:
            if not os.path.exists(dir):
                try:
                    os.makedirs(dir)
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise



def main():

    report = UrlBuilder()
    report.generate_request_data()


if __name__ == '__main__':


    main()
