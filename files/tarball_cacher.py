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
        return os.path.isfile(os.path.join(self.cache_path,
                                           self.tarball_lock))

    def checkFile(self):
        return os.path.isfile(os.path.join(self.cache_path,
                                           self.tarball_name))

    def downloadFile(self):
        # TODO: Use urlretrieve
        download_cmd = ['wget', '-P', self.cache_path, self.args.tarball_url]
        subprocess.check_output(['touch', os.path.join(self.cache_path,
                                                       self.tarball_lock)])
        subprocess.check_output(download_cmd)
        subprocess.check_output(['rm', os.path.join(self.cache_path,
                                                    self.tarball_lock)])

    def unmarshallURL(self):
        # TODO: This looks really unnecessary
        url = self.args.upload
        if len(url.split('/')) < 3:
            raise EnvironmentError('SFTP URL is not valid %s' % url)
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
        return self.tarball_name in stdout.decode("utf-8")

    def uploadSFTP(self, sftp_ip, sftp_dir):
        if not self.args.upload:
            return 0

        print("Uploading the file to SFTP")
        full_path = os.path.join(self.cache_path, self.tarball_name)
        stdout = subprocess.check_output(['(echo "put ' + full_path + '" && echo "exit") | \
                                          sftp -o ForwardAgent=yes -o ConnectTimeout=60 -o \
                                          UserKnownHostsFile=/dev/null -o \
                                          StrictHostKeyChecking=no ' +
                                          sftp_ip + ':' + sftp_dir],
                                          stderr=subprocess.STDOUT, shell=True)
        return 0

    def main(self):
        sftp_ip, sftp_dirpath = self.unmarshallURL()

        # If file exists in the server, don't even download a copy
        if self.checkTarballUpload(sftp_ip, sftp_dirpath):
            print("Tarball already uploaded")
            return 0

        # If another process is caching the same file, wait max 3 min
        count = 180
        while self.checkLock():
            time.sleep(1)
            count -= 1
            if count == 0:
                raise TimeoutError("Waited 3min for file lock on %s" %
                                   self.tarball_name)

        # If file is not local, download
        if not self.checkFile():
            print("Downloading the file into the cache")
            self.downloadFile()

        # Upload
        return self.uploadSFTP(sftp_ip, sftp_dirpath)

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
