#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Base Factory class, with common logic for finding and loading models
"""
import os
import re

try:
    import test_models.testmodel
    from test_models.test_model_implementations import *
except ImportError:
    import ansible.module_utils.test_result_parser.test_models.testmodel
    from ansible.module_utils.test_result_parser.test_models.test_model_implementations import *

class TestFactory(object):
    def __init__(self):
        self.model_types = {
                             'bibwtest_openmpi3_model': {'Bi-Directional Bandwidth Test': r'\s+OSU\sMPI\s(\w+[-]\w+\s\w+\s\w+)'},
                             'bibwtest_model': {'Bidirectional BW Test': r'\s+RDMA_Write\s(\w+\s\w+\s\w+)'},
                             'bwtest_model': {'BW Test': r'\s+RDMA_Write\s(\w+\s\w+)'},
                             'bwtest_openmpi3_model': {'Bandwidth Test': r'\s+OSU\sMPI\s(\w+\s\w+)'},
                             'latency_model': {'Latency Test': r'\s+RDMA_Write\s(\w+\s\w+)'},
                             'latency_openmpi3_model': {'Latency Test': r'\s+OSU\sMPI\s(\w+\s\w+)'},
                           }

    def getTest(self, test_output):
        return self._find_model(test_output)

    def _get_model_name(self, test_output):
        for model_name, model_type in self.model_types.items():
            for field, regex in model_type.items():
                match = re.search(regex, test_output)
                if match is not None and match.group(1) == field:
                    return model_name

        return False

    def _find_model(self, condition):
        model = self._get_model_name(condition)
        if model == False:
            raise ImportError("Unable to find matching Test Model")
        if model == 'bibwtest_model':
            return BiBwTestModel(), model
        elif model == 'bwtest_model':
            return BwTestModel(), model
        elif model == 'latency_model':
            return LatencyTestModel(), model
        elif model == 'bibwtest_openmpi3_model':
            return MPIBiBwTestModel(), model
        elif model == 'bwtest_openmpi3_model':
            return MPIBwTestModel(), model
        elif model == 'latency_openmpi3_model':
            return MPILatencyTestModel(), model
