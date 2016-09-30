##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import re
import ConfigParser
import logging
import fileinput

import consts.files as files
import consts.parameters as parameters

# ------------------------------------------------------
# List of common variables
# ------------------------------------------------------

LOG = None
CONF_FILE = None
DEPLOYMENT_UNIT = None
ITERATIONS = None

BASE_DIR = None
TEMPLATE_DIR = None
TEMPLATE_NAME = None
TEMPLATE_EXTENSION = None

# ------------------------------------------------------
# Initialization and Input 'heat_templates/'validation
# ------------------------------------------------------


def init(api=False):
    global BASE_DIR
    # BASE_DIR = os.getcwd()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = BASE_DIR.replace('/heat', '')
    BASE_DIR = InputValidation.validate_directory_exist_and_format(
        BASE_DIR, "Error 000001")

    conf_file_init(api)
    log_init()
    general_vars_init(api)


def conf_file_init(api=False):
    global CONF_FILE
    if api:
        CONF_FILE = ConfigurationFile(files.get_sections_api(),
                                      '/tmp/bottlenecks.conf')
    else:
        CONF_FILE = ConfigurationFile(cf.get_sections(),
                                      '/tmp/bottlenecks.conf')


def general_vars_init(api=False):
    global TEMPLATE_EXTENSION
    global TEMPLATE_NAME
    global TEMPLATE_DIR
    global ITERATIONS

    TEMPLATE_EXTENSION = '.yaml'

    # Check Section in Configuration File
    InputValidation.validate_configuration_file_section(
        files.GENERAL,
        "Section " + files.GENERAL +
        "is not present in configuration file")

    InputValidation.validate_configuration_file_section(
        files.OPENSTACK,
        "Section " + files.OPENSTACK +
        "is not present in configuration file")

    TEMPLATE_DIR = '/tmp/heat_templates/'

    if not api:
        # Validate template name
        InputValidation.validate_configuration_file_parameter(
            files.GENERAL,
            files.TEMPLATE_NAME,
            "Parameter " + files.TEMPLATE_NAME +
            "is not present in configuration file")
        TEMPLATE_NAME = CONF_FILE.get_variable(files.GENERAL,
                                               files.TEMPLATE_NAME)
        InputValidation.validate_file_exist(
            TEMPLATE_DIR + TEMPLATE_NAME,
            "The provided template file does not exist")

    # Validate and assign Iterations
    if files.ITERATIONS in CONF_FILE.get_variable_list(files.GENERAL):
        ITERATIONS = int(CONF_FILE.get_variable(files.GENERAL,
                                                files.ITERATIONS))
    else:
        ITERATIONS = 1


def log_init():
    global LOG
    LOG = logging.getLogger()
    LOG.setLevel(level=logging.DEBUG)
    log_formatter = logging.Formatter("%(asctime)s --- %(message)s")
    file_handler = logging.FileHandler("{0}/{1}.log".format("./", "benchmark"))
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)
    LOG.addHandler(file_handler)

# ------------------------------------------------------
# Configuration file access
# ------------------------------------------------------


class ConfigurationFile:
    """
    Used to extract data from the configuration file
    """

    def __init__(self, sections, config_file='conf.cfg'):
        """
        Reads configuration file sections

        :param sections: list of strings representing the sections to be
                         loaded
        :param config_file: name of the configuration file (string)
        :return: None
        """
        InputValidation.validate_string(
            config_file, "The configuration file name must be a string")
        InputValidation.validate_file_exist(
            config_file, 'The provided configuration file does not exist')
        self.config = ConfigParser.ConfigParser()
        self.config.read(config_file)
        for section in sections:
            setattr(
                self, section, ConfigurationFile.
                _config_section_map(section, self.config))

    @staticmethod
    def _config_section_map(section, config_file):
        """
        Returns a dictionary with the configuration values for the specific
        section

        :param section: section to be loaded (string)
        :param config_file: name of the configuration file (string)
        :return: dict
        """
        dict1 = dict()
        options = config_file.options(section)
        for option in options:
            dict1[option] = config_file.get(section, option)
        return dict1

    def get_variable(self, section, variable_name):
        """
        Returns the value correspondent to a variable

        :param section: section to be loaded (string)
        :param variable_name: name of the variable (string)
        :return: string
        """
        message = "The variable name must be a string"
        InputValidation.validate_string(variable_name, message)
        if variable_name in self.get_variable_list(section):
            sect = getattr(self, section)
            return sect[variable_name]
        else:
            exc_msg = 'Parameter {} is not in the {} section of the ' \
                      'conf file'.format(variable_name, section)
            raise ValueError(exc_msg)

    def get_variable_list(self, section):
        """
        Returns the list of the available variables in a section
        :param section: section to be loaded (string)
        :return: list
        """
        try:
            return getattr(self, section)
        except:
            msg = 'Section {}  not found in the configuration file'.\
                format(section)
            raise ValueError(msg)

# ------------------------------------------------------
# Manage files
# ------------------------------------------------------


def get_heat_template_params():
    """
    Returns the list of deployment parameters from the configuration file
    for the heat template

    :return: dict
    """
    heat_parameters_list = CONF_FILE.get_variable_list(
        files.DEPLOYMENT_PARAMETERS)
    testcase_parameters = dict()
    for param in heat_parameters_list:
        testcase_parameters[param] = CONF_FILE.get_variable(
            files.DEPLOYMENT_PARAMETERS, param)
    return testcase_parameters


def get_testcase_params():
    """
    Returns the list of testcase parameters from the configuration file

    :return: dict
    """
    testcase_parameters = dict()
    parameters = CONF_FILE.get_variable_list(files.TESTCASE_PARAMETERS)
    for param in parameters:
        testcase_parameters[param] = CONF_FILE.get_variable(
            files.TESTCASE_PARAMETERS, param)
    return testcase_parameters


def get_file_first_line(file_name):
    """
    Returns the first line of a file

    :param file_name: name of the file to be read (str)
    :return: str
    """
    message = "name of the file must be a string"
    InputValidation.validate_string(file_name, message)
    message = 'file {} does not exist'.format(file_name)
    InputValidation.validate_file_exist(file_name, message)
    res = open(file_name, 'r')
    return res.readline()


def replace_in_file(file, text_to_search, text_to_replace):
    """
    Replaces a string within a file

    :param file: name of the file (str)
    :param text_to_search: text to be replaced
    :param text_to_replace: new text that will replace the previous
    :return: None
    """
    message = 'text to be replaced in the file must be a string'
    InputValidation.validate_string(text_to_search, message)
    message = 'text to replace in the file must be a string'
    InputValidation.validate_string(text_to_replace, message)
    message = "name of the file must be a string"
    InputValidation.validate_string(file, message)
    message = "The file does not exist"
    InputValidation.validate_file_exist(file, message)
    for line in fileinput.input(file, inplace=True):
        print(line.replace(text_to_search, text_to_replace).rstrip())

# ------------------------------------------------------
# Shell interaction
# ------------------------------------------------------


def run_command(command):
    LOG.info("Running command: {}".format(command))
    return os.system(command)

# ------------------------------------------------------
# Expose variables to other modules
# ------------------------------------------------------


def get_base_dir():
    return BASE_DIR


def get_template_dir():
    return TEMPLATE_DIR

# ------------------------------------------------------
# Configuration Variables from Config File
# ------------------------------------------------------


def get_deployment_configuration_variables_from_conf_file():
    variables = dict()
    types = dict()
    all_variables = CONF_FILE.get_variable_list(files.EXPERIMENT_VNF)
    for var in all_variables:
        v = CONF_FILE.get_variable(files.EXPERIMENT_VNF, var)
        type = re.findall(r'@\w*', v)
        values = re.findall(r'\"(.+?)\"', v)
        variables[var] = values
        try:
            types[var] = type[0][1:]
        except IndexError:
            LOG.debug("No type has been specified for variable " + var)
    return variables

# ------------------------------------------------------
# benchmarks from Config File
# ------------------------------------------------------


def get_benchmarks_from_conf_file():
    requested_benchmarks = list()
    benchmarks = CONF_FILE.get_variable(
        files.GENERAL, files.BENCHMARKS).split(', ')
    for benchmark in benchmarks:
        requested_benchmarks.append(benchmark)
    return requested_benchmarks


class InputValidation(object):

    @staticmethod
    def validate_string(param, message):
        if not isinstance(param, str):
            raise ValueError(message)
        return True

    @staticmethod
    def validate_integer(param, message):
        if not isinstance(param, int):
            raise ValueError(message)
        return True

    @staticmethod
    def validate_dictionary(param, message):
        if not isinstance(param, dict):
            raise ValueError(message)
        return True

    @staticmethod
    def validate_file_exist(file_name, message):
        if not os.path.isfile(file_name):
            raise ValueError(message + ' ' + file_name)
        return True

    @staticmethod
    def validate_directory_exist_and_format(directory, message):
        if not os.path.isdir(directory):
            raise ValueError(message)
        if not directory.endswith('/'):
            return directory + '/'
        return directory

    @staticmethod
    def validate_configuration_file_parameter(section, parameter, message):
        params = CONF_FILE.get_variable_list(section)
        if parameter not in params:
            raise ValueError(message)
        return True

    @staticmethod
    def validate_configuration_file_section(section, message):
        if section not in files.get_sections():
            raise ValueError(message)
        return True

    @staticmethod
    def validate_boolean(boolean, message):
        if isinstance(boolean, bool):
            return boolean
        if isinstance(boolean, str):
            if boolean == 'True':
                return True
            if boolean == 'False':
                return False
        raise ValueError(message)

    @staticmethod
    def validate_os_credentials(credentials):
        if not isinstance(credentials, dict):
            raise ValueError(
                'The provided openstack_credentials '
                'variable must be in dictionary format')

        credential_keys = ['user', 'password', 'ip_controller', 'heat_url',
                           'auth_uri', 'project']
        missing = [
            credential_key
            for credential_key in credential_keys
            if credential_key not in credentials.keys()
        ]
        if len(missing) == 0:
            return True
        msg = 'OpenStack Credentials Error! ' \
              'The following parameters are missing: {}'.\
            format(", ".join(missing))
        raise ValueError(msg)
