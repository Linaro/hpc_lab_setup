#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os

try:
    from test_models.testmodel import TestModel
    from test_models.parsing_strategies import *
except ImportError:
    from ansible.module_utils.test_result_parser.test_models.testmodel import TestModel
    from ansible.module_utils.test_result_parser.test_models.parsing_strategies import *

class BiBwTestModel(TestModel):
    def __init__(self):
        super().__init__()
        self.fail_msg = "FAIL: Less than {0} Gb/s of BW !"
        self.parameters_regex = {
            'Dual-port': r'\bDual-port\s+:\s(\w+)',
            'Number of qps': r'\bNumber of qps\s+:\s(\d+)',
            'Connection type': r'\bConnection type\s+:\s(\w+)',
            'TX depth': r'\bTX depth\s+:\s(\d+)',
            'CQ Moderation': r'\bCQ Moderation\s+:\s(\d+)',
            'Mtu': r'\bMtu\s+:\s(\d+\[\w\])',
            'Link type': r'\bLink type\s+:\s(\w+)',
            'Max inline data': r'\bMax inline data\s+:\s(\d+\[\w\])',
            'rdma_cm QPs': r'\brdma_cm QPs\s+:\s(\w+)',
            'Data ex. method': r'\bData ex. method\s+:\s(\w+)',
            'Device': r'\bDevice\s+:\s(\w+)',
            'Transport type': r'\bTransport type\s+:\s(\w+)',
            'Using SRQ': r'\bUsing SRQ\s+:\s(\w+)'
        }
        self.result_list = ['bytes', 'iterations', 'BW Peak[Gb/s]', 'BW avg[Gb/s]', 'MsgRate[Mbps]']
        self.result_regex = re.compile(r'^\s+(\d+)\s+(\d+)\s+(\d+.\d+)\s+(\d+.\d+)\s+(\d+.\d+)\s+', re.M)
        self.failure_test = lambda results, threshold: float(results['BW avg[Gb/s]']) < float(threshold)
        self.strategy = SingleLabeledRow()

class MPIBiBwTestModel(TestModel):
    def __init__(self):
        super().__init__()
        self.fail_msg = "Less than {0} Gb/s of BW !"
        self.result_list = ['Size', 'Bandwidth']
        self.result_regex = re.compile(r'^(\d+)\s+(\d+.\d+)', re.M)
        self.failure_test = lambda results, threshold: float(results['4194304']) < float(threshold)
        self.strategy = SingleParameterIndexedColumn()

class BwTestModel(TestModel):
    def __init__(self):
        super().__init__()
        self.fail_msg = "Less than {0} Gb/s of BW !"
        self.parameters_regex = {
            'Dual-port': r'\bDual-port\s+:\s(\w+)',
            'Number of qps': r'\bNumber of qps\s+:\s(\d+)',
            'Connection type': r'\bConnection type\s+:\s(\w+)',
            'TX depth': r'\bTX depth\s+:\s(\d+)',
            'CQ Moderation': r'\bCQ Moderation\s+:\s(\d+)',
            'Mtu': r'\bMtu\s+:\s(\d+\[\w\])',
            'Link type': r'\bLink type\s+:\s(\w+)',
            'Max inline data': r'\bMax inline data\s+:\s(\d+\[\w\])',
            'rdma_cm QPs': r'\brdma_cm QPs\s+:\s(\w+)',
            'Data ex. method': r'\bData ex. method\s+:\s(\w+)',
            'Device': r'\bDevice\s+:\s(\w+)',
            'Transport type': r'\bTransport type\s+:\s(\w+)',
            'Using SRQ': r'\bUsing SRQ\s+:\s(\w+)'
        }
        self.result_list = ['bytes', 'iterations', 'BW Peak[Gb/s]', 'BW avg[Gb/s]', 'MsgRate[Mbps]']
        self.result_regex = re.compile(r'^\s+(\d+)\s+(\d+)\s+(\d+.\d+)\s+(\d+.\d+)\s+(\d+.\d+)\s+', re.M)
        self.failure_test = lambda results, threshold: float(results['BW avg[Gb/s]']) < float(threshold)
        self.strategy = SingleLabeledRow()

class MPIBwTestModel(TestModel):
    def __init__(self):
        super().__init__()
        self.fail_msg = "Less than {0} Gb/s of BW !"
        self.result_list = ['Size', 'Bandwidth']
        self.result_regex = re.compile(r'^(\d+)\s+(\d+.\d+)', re.M)
        self.failure_test = lambda results, threshold: float(results['4194304']) < float(threshold)
        self.strategy = SingleParameterIndexedColumn()

class LatencyTestModel(TestModel):
    def __init__(self):
        super().__init__()
        self.fail_msg = "Latency is above {0} usec !"
        self.parameters_regex = {
            'Dual-port': r'\bDual-port\s+:\s(\w+)',
            'Number of qps': r'\bNumber of qps\s+:\s(\d+)',
            'Connection type': r'\bConnection type\s+:\s(\w+)',
            'TX depth': r'\bTX depth\s+:\s(\d+)',
            'Mtu': r'\bMtu\s+:\s(\d+\[\w\])',
            'Link type': r'\bLink type\s+:\s(\w+)',
            'Max inline data': r'\bMax inline data\s+:\s(\d+\[\w\])',
            'rdma_cm QPs': r'\brdma_cm QPs\s+:\s(\w+)',
            'Data ex. method': r'\bData ex. method\s+:\s(\w+)',
            'Device': r'\bDevice\s+:\s(\w+)',
            'Transport type': r'\bTransport type\s+:\s(\w+)',
            'Using SRQ': r'\bUsing SRQ\s+:\s(\w+)'
        }
        self.result_list = ['bytes', 'iterations', 't_min[usec]',
                            't_max[usec]', 't_typical[usec]', 't_avg[usec]',
                            't_stdev[usec]', '99Perc[usec]', '99.9Perc[usec]']
        self.result_regex = re.compile(r'^\s+(\d+)\s+(\d+)\s+(\d+.\d+)\s+(\d+.\d+)\s+(\d+.\d+)\s+(\d+.\d+)\s+(\d+.\d+)\s+(\d+.\d+)\s+(\d+.\d+)\s+', re.M)
        self.failure_test = lambda results, threshold: float(results['t_avg[usec]']) > float(threshold)
        self.strategy = SingleLabeledRow()

class MPILatencyTestModel(TestModel):
    def __init__(self):
        super().__init__()
        self.fail_msg = "Latency superior to {0} usec !"
        self.result_list = ['Size', 'Bandwidth']
        self.result_regex = re.compile(r'^(\d+)\s+(\d+.\d+)', re.M)
        self.failure_test = lambda results, threshold: float(results['0']) > float(threshold)
        self.strategy = SingleParameterIndexedColumn()
