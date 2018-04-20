#!/usr/bin/env python3

import argparse
import subprocess
import os
import re

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

GIT_URLS = { 'lulesh':'https://github.com/BaptisteGerondeau/LULESH.git' }
BENCHMARK_LIST = ['lulesh']

parser = argparse.ArgumentParser(description='Run some benchmark.')
parser.add_argument('name', metavar='benchmark_name', type=str,
                    help='The name of the benchmark to be run')
parser.add_argument('machine_type', type=str,
                    help='The type of the machine to run the benchmark on')
parser.add_argument('compiler', type=str,
                    help='The compiler with which to compile the benchmark')
parser.add_argument('--compiler-flags', type=str,
                    help='The compiler flags to use with compiler')
parser.add_argument('--benchmark-options', type=str,
                    help='The benchmark options to use with the benchmark')
parser.add_argument('--build-number', type=str,
                    help='The number of the benchmark run this is')

args = parser.parse_args()

identity = str(args.name + '_' + args.compiler + '_' + args.compiler_flags.replace(" ", "") +
               '_' + args.machine_type + '_' + args.benchmark_options.replace(" ", "") +
               '_' + args.build_number)
execname = re.sub("[^a-zA-Z0-9_]+", "", identity).lower()
report_name = identity + '.report'

make_cmd = []
make_cmd += 'make'
make_cmd += 'CXX=' + args.compiler
make_cmd += 'CXXFLAGS=' + args.compiler_flags

if args.name.lower() == 'lulesh':
    make_cmd += 'LULESH_EXEC="' + execname + '"'

if args.name.lower() in BENCHMARK_LIST:
    subprocess.run(['mkdir', identity])
    with cd(identity):
        subprocess.run(['git', 'clone', GIT_URLS[args.name.lower()], args.name.lower()], check=True)
        with cd(args.name.lower()):
            subprocess.run(make_cmd, check=True)
            with open(report_name, 'w') as fd:
                subprocess.check_call(['./' + execname, args.benchmark_options],
                        stderr=subprocess.STDOUT, stdout=fd)
