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

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

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

    def unmarshallURL(self):
        url = self.args.upload
        if len(url.split('/')) < 3:
            raise EnvironmentError('SFTP URL is not valid %s' %
                                   url)
        if len(url.split('/')) == 4:
            sftp_dirpath = '/'
        else:
            sftp_dirpath = '/' + \
                     "/".join(url.split("/")[3:]) + '/'

        sftp_ip = url.split("/")[2:3][0]

        return sftp_ip, sftp_dirpath

    def checkTarballUpload(self, sftp_ip, sftp_dir):
        stdout = subprocess.check_output(['(echo "ls" && echo "exit") | \
                                          sftp -o ForwardAgent=yes -o \
                                          ConnectTimeout=60 -o \
                                          UserKnownHostsFile=/dev/null -o \
                                          StrictHostKeyChecking=no ' + sftp_ip +
                                          ':' + sftp_dir],
                                         stderr=subprocess.STDOUT, shell=True)
        print(stdout)
        if self.tarball_name in stdout.decode("utf-8"):
            return True
        else:
            return False


    def uploadSFTP(self, sftp_ip, sftp_dir):
        if self.checkTarballUpload(sftp_ip, sftp_dir) == False:
            with cd(self.cache_path):
                stdout = subprocess.check_output(['(echo "put ' + self.tarball_name + '" && echo "exit") | \
                                                  sftp -o ForwardAgent=yes -o ConnectTimeout=60 -o \
                                                  UserKnownHostsFile=/dev/null -o \
                                                  StrictHostKeyChecking=no ' +
                                                  sftp_ip + ':' + sftp_dir],
                                                 stderr=subprocess.STDOUT, shell=True)
            print(stdout)
            return 0
        else:
            print("Tarball already uploaded")


    def main(self):
        while self.checkLock():
            time.sleep(3)

        tarball = self.checkFile()

        if tarball != False:
            if self.args.upload != '':
                sftp_ip, sftp_dirpath = self.unmarshallURL()
                return self.uploadSFTP(sftp_ip, sftp_dirpath)
        else:
            self.downloadFile()
            if self.args.upload != '':
                sftp_ip, sftp_dirpath = self.unmarshallURL()
                return self.uploadSFTP(sftp_ip, sftp_dirpath)
            else:
                return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download and cache some tarballs')
    parser.add_argument('tarball_url', type=str,
                        help='The URL of the tarball to download')
    parser.add_argument('cache_path', type=str,
                        help='The path to the cache storage place')
    parser.add_argument('--upload', '-u', type=str, default='',
                        help='The sftp URL to upload the tarball to.')
    args = parser.parse_args()

    cacher = TarballCacher(parser, args)
    cacher.main()
