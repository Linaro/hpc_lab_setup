#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

class ParsingStrategy(object):
    def assignement(self, i, j, parsed_results, result_list, match_result):
        """ This is the non-common part of the parsing, as far as the set of
        test supported now are concerned"""
        return parsed_results

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
