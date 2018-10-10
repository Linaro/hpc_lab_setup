#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

try:
    from test_models.parsing_strategy import ParsingStrategy
except ImportError:
    from ansible.module_utils.test_result_parser.test_models.parsing_strategy import ParsingStrategy

class SingleLabeledRow(ParsingStrategy):
    """ This Strategy parses tables in this format :
        [label] [label1] [lable2]
        [value] [value1] [value2]
        And puts the values in a label indexed dictionary"""
    def assignement(self, i, j, parsed_results, result_list, match_result):
        parsed_results[result_list[i]] = str(match_result[j][i])

class SingleParameterIndexedColumn(ParsingStrategy):
    """ This Strategy parses tables in this format :
        [label] [label1]
        [param] [value]
        [...]   [...]
        And puts the values in a parameter indexed dictionary"""
    def assignement(self, i, j, parsed_results, result_list, match_result):
        parsed_results[str(match_result[j][0])] = str(match_result[j][1])
