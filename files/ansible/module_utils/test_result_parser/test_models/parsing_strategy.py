#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

class ParsingStrategy(object):
    def assignement(self, i, j, parsed_results, result_list, match_result):
        """ This is the non-common part of the parsing, as far as the set of
        test supported now are concerned"""
        raise NotImplementedError("This is a virtual method, please redefine in derived class")

    def parse(self, test, result_regex, result_list, parameters_regex):
        """ This is the common part of the parsing, it is in the strategy
        object as it allows for overriding this behaviour for other tests
        that might not fit this algorithm"""
        parsed_results = dict()
        parsed_params = dict()

        # The structure of the matches mostly determines the assignement method
        match_result = re.findall(result_regex, test)

        # if no matches were found and if the number of matches is not the
        # number of desired results
        if len(match_result) == 1 and len(match_result[0]) != len(result_list):
            raise RuntimeError("Couldn't parse enough results")

        # iterate over the matches and the results list to fill the
        # parsed_results array appropriately
        for j in range(0, len(match_result)):
            for i in range(0, len(result_list)):
                self.assignement(i, j, parsed_results, result_list, match_result)

        # Parse the parameters
        for field, regex in parameters_regex.items():
            match = re.search(regex, test)
            if match is not None:
                parsed_params[field] = str(match.group(1))
            else:
                raise RuntimeError("Couldn't parse parameters correctly : %s" %
                                  regex)

        return parsed_results, parsed_params

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
