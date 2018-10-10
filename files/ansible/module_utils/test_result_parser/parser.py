#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

from junitparser import TestCase, TestSuite, JUnitXml, Skipped, Error

from ansible.module_utils.test_result_parser.factory import TestFactory
from ansible.module_utils.test_result_parser.test_models import *

class TestParser(object):
    def __init__(self):
        self.test_factory = TestFactory()
        self.formatter = JUnitXml()
        self.format = '.xml'

    def parse(self, results_path, test_threshold, output_path, extra=''):
        result = ""
        filename = os.path.basename(results_path)
        with open(results_path, 'r') as output:
            result = output.read()

        test, test_type = self.test_factory.getTest(result)
        results, params = test.parse_output(result)

        testcase = TestCase(test_type)

        if test.failed(results, test_threshold):
            testcase.result = Error(test.fail_msg.format(test_threshold), test_type)

        suite = TestSuite(test_type + extra)
        for name, value in results.items():
            suite.add_property(name, value)

        for name, value in params.items():
            suite.add_property(name, value)

        testcase.system_out = result
        suite.add_testcase(testcase)

        junit = self.formatter
        junit.add_testsuite(suite)

        if output_path[-1] != '/':
            output_path += '/'
        junit.write(output_path + 'junit-' + filename + '-' + extra + self.format)
