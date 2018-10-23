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
                             'bibwtest_openmpi3_model': r'\s+OSU\sMPI\sBi-Directional\sBandwidth\sTest',
                             'bwtest_openmpi3_model': r'\s+OSU\sMPI\sBandwidth\sTest',
                             'latency_openmpi3_model': r'\s+OSU\sMPI\sLatency\sTest',
                             'bibwtest_model': r'\s+RDMA_Write\sBidirectional\sBW\sTest',
                             'bwtest_model': r'\s+RDMA_Write\sBW\sTest',
                             'latency_model': r'\s+RDMA_Write\sLatency\sTest',
                           }

    def getTest(self, test_output):
        model = self._get_model_name(test_output)
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
        else:
            raise ImportError("Unable to find matching Test Model")

    def _get_model_name(self, test_output):
        for model, regex in self.model_types.items():
            match = re.search(regex, test_output)
            if match is not None:
                return model

        return None
