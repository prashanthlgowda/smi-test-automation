# -*- coding: utf-8 -*-
"""
JSON Toolkit
~~~~~~~~~~~~
Series of tools designed around using JSON files

:Copyright: (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
:License: Apache 2.0, see LICENSE for more details.
:Author: Akash Kwatra

Created on June 26, 2017
"""

import logging
import json

LOG = logging.getLogger(__name__)

def select_directory(default_directory, override):
    """Compare default directory and override to determine json directory"""
    LOG.debug("Default Directory :: %s Override :: %s", default_directory, override)
    directory = override if override else default_directory
    LOG.info("Selected host was %s", directory)
    return directory

def create_json_reference(directory, filename):
    """Use the directory and filename, generate a json reference"""
    LOG.debug("Provided Directory: %s JSON File: %s", directory, filename)
    json_reference = "{}/{}".format(directory, filename)
    LOG.debug("Generated Reference :: %s", json_reference)
    return json_reference

def load_test_data(directory, task):
    """Load test data from provided json file"""
    with open(directory) as stream:
        data = json.load(stream)
        extention = data["services"][task]["url"]
        parameters = data["services"][task]["parameters"]
        payload = data["services"][task]["payload"]
        return extention, parameters, payload
