#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

try:
    from test_models.parsing_strategy import ParsingStrategy
except ImportError:
    from ansible.module_utils.test_result_parser.test_models.parsing_strategy import ParsingStrategy

class TestModel(object):
    def __init__(self):
        self.fail_msg = "Default Failure Message"
        self.parameters_regex = dict()
        self.result_regex = re.compile(r'', re.M)
        self.result_list = []
        self.failure_test = lambda results, threshold : False
        self.strategy = ParsingStrategy()

    def failed(self, parsed_results, test_threshold):
        return self.failure_test(parsed_results, test_threshold)

    def parse_output(self, test_output):
        return self.strategy.parse(test_output, self.result_regex,
                                   self.result_list, self.parameters_regex)
