#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

from junitparser import TestCase, TestSuite, JUnitXml, Skipped, Error

try:
    from factory import TestFactory
    from test_models import *
except ImportError:
    from ansible.module_utils.test_result_parser.factory import TestFactory
    from ansible.module_utils.test_result_parser.test_models import *

class TestParser(object):
    def __init__(self, json_or_xml):
        if str(json_or_xml) == "xml":
            self.formatter = JUnitXml()
            self.format = '.xml'
        else:
            # TODO: Implement a JSON format compatible with SQUAD
            # This means using the python (l)xml ElementTree (<=> TestSuite())
            self.formatter = None
            self.format = '.json'

        self.test_factory = TestFactory()

    def main(self, results_path, test_threshold, output_path, extra=''):
        result = ""
        filename = os.path.basename(results_path)
        with open(results_path, 'r') as output:
            for line in output.readlines():
                result += line

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

        if self.formatter is None:
            raise ValueError("No Formatter given !")

        junit = self.formatter
        junit.add_testsuite(suite)

        if output_path[-1] != '/':
            output_path+='/'
        junit.write(output_path + 'junit-' + filename + '-' + extra + self.format)

if __name__ == '__main__':
    """ This is used to test the module logic without Ansible
        NOTE: argparse is not needed otherwise, no need to include it everytime"""
    import argparse

    parser = argparse.ArgumentParser(description="Point of entry to test the \
                                     test_tesult_parser", add_help=False)
    parser.add_argument('-f', '--formatter', type=str, default='xml',
                        required=False, help="Formatter to use XML or JSON")
    parser.add_argument('-r', '--results-path', type=str, default='',
                        required=True, help="Path to the test results' file")
    parser.add_argument('-t', '--threshold', type=str, default='',
                        required=True, help="Threshold to fail or pass the test")
    parser.add_argument('-o', '--output-path', type=str, default='./',
                        required=False, help="Path to where the JUnit should be outputted")
    parser.add_argument('-e', '--extra-tag', type=str, default='',
                        required=False, help="Extra tag for the JUnit filename")
    args = parser.parse_args()
    test_parser = TestParser(args.formatter)
    test_parser.main(args.results_path, args.threshold, args.output_path,
                     args.extra_tag)
