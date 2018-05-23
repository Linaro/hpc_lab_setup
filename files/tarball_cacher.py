#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Toolchain and large tarball cacher.

    Usage: tarball_cacher.py [tarball_url] [path_to_chache]
"""

import os
import subprocess
import argparse
import time

class TarballCacher(object):
    def __init__(self, argparse_parser, argparse_args):
        self.parser = argparse_parser
        self.args = argparse_args
        self.cache_path = os.path.abspath(self.args.cache_path)
        self.tarball_name = self.args.tarball_url.split("/")[-1]
        self.tarball_lock = self.tarball_name + '.lock'

    def checkLock(self):
        if os.path.isfile(os.path.join(self.cache_path,
                                       self.tarball_lock)):
            return True
        else:
            return False

    def checkFile(self):
        if os.path.isfile(os.path.join(self.cache_path,
                                       self.tarball_name)):
            return os.path.join(self.cache_path, self.tarball_name)
        else:
            return False

    def downloadFile(self):
        download_cmd = ['wget', '-P', self.cache_path, self.args.tarball_url]
        subprocess.check_output(['touch', os.path.join(self.cache_path,
                                                       self.tarball_lock)])
        subprocess.check_output(download_cmd)
        subprocess.check_output(['rm', os.path.join(self.cache_path,
                                                    self.tarball_lock)])
        return 0

    def main(self):
        while self.checkLock():
            time.sleep(3)

        tarball = self.checkFile()
        if tarball != False:
            return 0
        else:
            return self.downloadFile()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download and cache some tarballs')
    parser.add_argument('tarball_url', type=str,
                        help='The URL of the tarball to download')
    parser.add_argument('cache_path', type=str,
                        help='The path to the cache storage place')
    args = parser.parse_args()

    cacher = TarballCacher(parser, args)
    cacher.main()
