#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

from ansible.module_utils.test_result_parser.test_models.parsing_strategy import ParsingStrategy

class TestModel(object):
    def __init__(self):
        self.fail_msg = None
        self.parameters_regex = None
        self.result_regex = None
        self.result_list = None
        self.failure_test = None
        self.strategy = ParsingStrategy()

    def parse_output(self, test_output):
        return self.strategy.parse(test_output, self.result_regex,
                                   self.result_list, self.parameters_regex)
