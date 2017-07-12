# -*- coding: utf-8 -*-
"""
Test Toolkit
~~~~~~~~~~~~
Series of tools designed to control testing

:Copyright: (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
:License: Apache 2.0, see LICENSE for more details.
:Author: Akash Kwatra

Created on June 28, 2017
"""

import logging
from . import json, http, log, parse

LOG = logging.getLogger(__name__)

###################################################################################################
# Premade Tests
###################################################################################################

@log.exception(LOG)
def get_bad_data(end_class):
    """Run GET requests with missing or empty data, check for failure"""
    LOG.info("Begin GET tests for %s using bad data", end_class.__class__.__name__)
    for combo in _bad_data_combos(json.get_base_payload(end_class)):
        request = http.rest_get(end_class.URL, combo)
        with end_class.subTest(data=combo):
            end_class.assertTrue(has_status_code(request, ">=400"), "Expected Response Code : >= 400")

@log.exception(LOG)
def post_bad_data(end_class):
    """Run POST requests with missing or empty data, check for failure"""
    LOG.info("Begin POST tests for %s using bad data", end_class.__class__.__name__)
    for combo in _bad_data_combos(json.get_base_payload(end_class)):
        request = http.rest_post(end_class.URL, combo)
        with end_class.subTest(data=combo):
            end_class.assertTrue(has_status_code(request, ">=400"), "Expected Response Code : >= 400")

@log.exception(LOG)
def get_bad_data_except(end_class, good_combos):
    """Run GET requests with missing or empty data excluding those specified, check for failure"""
    LOG.info("Begin GET tests for %s using bad data with the following exceptions :: %s",
             end_class.__class__.__name__, good_combos)
    for combo in _bad_data_combos_except(json.get_base_payload(end_class), good_combos):
        request = http.rest_get(end_class.URL, combo)
        with end_class.subTest(data=combo):
            end_class.assertTrue(has_status_code(request, ">=400"), "Expected Response Code : >= 400")

@log.exception(LOG)
def post_bad_data_except(end_class, good_combos):
    """Run POST requests with missing or empty data excluding those specified, check for failure"""
    LOG.info("Begin POST tests for %s using bad data with the following exceptions :: %s",
             end_class.__class__.__name__, good_combos)
    for combo in _bad_data_combos_except(json.get_base_payload(end_class), good_combos):
        request = http.rest_post(end_class.URL, combo)
        with end_class.subTest(data=combo):
            end_class.assertTrue(has_status_code(request, ">=400"), "Expected Response Code : >= 400")

@log.exception(LOG)
def get_json(end_class):
    """Run tests specified in JSON using GET requests"""
    LOG.info("Begin JSON defined GET tests for %s", end_class.__class__.__name__)
    print("")
    for test_name in json.get_all_tests(end_class):
        skip, description, payload, status_code, response, error = json.get_test(end_class, test_name)
        if skip:
            print(skip)
        else:
            request = http.rest_get(end_class.URL, payload)
            with end_class.subTest(test=description):
                LOG.debug("Running Subtest : %s", description)
                end_class.assertTrue(compare_request(request, status_code, response), error)

@log.exception(LOG)
def post_json(end_class):
    """Run tests specified in JSON using POST requests"""
    LOG.info("Begin JSON defined POST tests for %s", end_class.__class__.__name__)
    print("")
    for test_name in json.get_all_tests(end_class):
        skip, description, payload, status_code, response, error = json.get_test(end_class, test_name)
        if skip:
            print(skip)
        else:
            request = http.rest_post(end_class.URL, payload)
            with end_class.subTest(test=description):
                LOG.debug("Running Subtest : %s", description)
                end_class.assertTrue(compare_request(request, status_code, response), error)


###################################################################################################
# Test Data Generators
###################################################################################################

def _bad_data_combos(payload):
    """Generate all combinations of empty and missing data"""
    for empty_combo in http.empty_data_combos(payload):
        yield empty_combo
    for incomplete_combo in http.missing_data_combos(payload):
        yield incomplete_combo

def _bad_data_combos_except(payload, good_combos):
    """Generate all combinations of empty and missing data except for those specified"""
    for bad_combo in _bad_data_combos(payload):
        valid_bad_combo = True
        for good_combo in good_combos:
            if set(good_combo) == set(bad_combo.keys()):
                valid_bad_combo = False
        if valid_bad_combo:
            yield bad_combo

###################################################################################################
# Test Results
###################################################################################################

def has_status_code(response, status_code):
    """Check if response status code is less than, greater than, or equal to specifed code"""
    check_status_code(response.status_code, status_code)

def check_status_code(status_code, exp_status):
    """Check if provided status code is less than, greater than, or equal to specifed code"""
    operation, exp_code = parse.status_code(exp_status)
    status_code, exp_code = int(status_code), int(exp_code)
    LOG.debug("Checking Response Status Code :: Expected : %s %s Actual : %s", operation, exp_code, status_code)
    if operation == '=' or operation == '==':
        return status_code == exp_code
    elif operation == '>':
        return status_code > exp_code
    elif operation == '<':
        return status_code < exp_code
    elif operation == '>=':
        return status_code >= exp_code
    elif operation == '<=':
        return status_code <= exp_code

def compare_request(request, status_code, exp_data):
    """
    Compare specified values in expected with those in response
    If status_code is specified, compare with response status code as well
    """
    if not check_status_code(request.status_code, status_code):
        LOG.error("============ BAD RESPONSE ============ :: Expected status code : %s Actual Status Code : %s",
                    status_code, request.status_code)
        return False
    else:
        request_data = json.load_response_data(request)
        return contains_expected(request_data, exp_data)

def contains_expected(container, expected):
    """Recursively check container to make sure expected is contained within"""
    if not isinstance(container, type(expected)):
        return False
    if isinstance(expected, (dict)):
        for item in expected:
            if item not in container:
                LOG.error("============ BAD RESPONSE ============ :: Expected key \"%s\" not contained in response", item)
                return False
            if not contains_expected(container[item], expected[item]):
                LOG.error("============ BAD RESPONSE ============ :: Key: %s Expected : %s Actual : %s",
                item, expected[item], container[item])
        return True
    if isinstance(expected, (list)):
        everything_found = True
        for item in expected:
            item_found = False
            for container_item in container:
                if contains_expected(container_item, item):
                    item_found = True
            if not item_found:
                everything_found = False
        return everything_found
    else:
        return container == expected