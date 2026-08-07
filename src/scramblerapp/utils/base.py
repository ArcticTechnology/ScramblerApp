# The Scrambler
# Copyright (c) 2023 Arctic Technology

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import pathlib
import secrets
from os.path import exists, isdir
from random import randrange
from typing import Type, Union

from tqdm import tqdm

from ..dircrawler.crawler import Crawler
from ..dircrawler.filemodder import FileModder
from .encryption import OpenSSLEncyptor as ossl


class Scrambler:

    def _randomize_and_remove_file(self, file_path: str) -> bool:
        r"""Randomize file header (4096 bytes) then remove it."""
        file = pathlib.Path(file_path)
        if not file.is_file():
            return False

        file_size: int = file.stat().st_size

        # 4096 bytes is the standard block size on file systems.
        bytes_to_overwrite: int = min(4096, file_size)

        if bytes_to_overwrite > 0:
            with file.open('r+b') as f:
                # Overwrite the file header randomly
                f.write(secrets.token_bytes(bytes_to_overwrite))
                f.flush()
                os.fsync(f.fileno())

        # Set file size to 0 bytes to overwrite the file system table.
        with file.open('wb') as f:
            f.truncate(0)

        # Remove file normally.
        file.unlink()

    def encrypt_msg(self,
                    password: str,
                    message: str,
                    decrypt: bool = False) -> dict:
        data = {'format': 'text', 'input': message, 'outpath': None}
        result = ossl.encrypt(password, data, decrypt)
        return result

    def encrypt_file(
        self,
        password: str,
        filepath: str,
        decrypt: bool = False,
        keep_org: bool = False,
        naked: bool = False,
        tag_options: dict[list[str]] = {
            'encrypt': ['openssl-c'],
            'decrypt': ['d', 'NAKED']
        }
    ) -> dict:
        result = {'status': None, 'message': None}

        if decrypt:
            index = 1 if naked else 0
            tag = tag_options['decrypt'][index]
            oldtags = tag_options['encrypt']
            newtags = tag_options['decrypt']
        else:
            tag = tag_options['encrypt'][0]
            oldtags = tag_options['decrypt']
            newtags = tag_options['encrypt']

        clean_filepath = Crawler.posixize(filepath)
        outpath = FileModder.add_tag(clean_filepath, tag, oldtags, newtags)

        if not exists(clean_filepath):
            result['status'] = 400
            result['message'] = 'Error failed to find file: ' + str(
                clean_filepath)
            return result

        if exists(outpath):
            result['status'] = 400
            result['message'] = 'Error output path already exists: ' + str(
                outpath)
            return result

        if outpath == clean_filepath:
            result['status'] = 400
            result['message'] = 'Action already performed on: ' + str(
                clean_filepath)
            return result

        data = {'format': 'file', 'input': clean_filepath, 'outpath': outpath}
        response = ossl.encrypt(password, data, decrypt)
        if response['status'] == 400:
            try:
                self._randomize_and_remove_file(outpath)
            except:
                pass
            return response

        if keep_org:
            result['status'] = response['status']
            result['message'] = response['message'] + ' (original retained).'
            return result

        try:
            self._randomize_and_remove_file(clean_filepath)
            result['status'] = 200
            result['message'] = response['message'] + ' (original deleted).'
        except:
            result['status'] = 400
            result['message'] = response[
                'message'] + ' (Error deleting original).'

        return result

    def encrypt_all_files(self,
                          password: str,
                          wd: str,
                          extension: Union[str, Type[None]] = None,
                          decrypt: bool = False,
                          keep_org: bool = False,
                          naked: bool = False,
                          tag_options: dict[list[str]] = {
                              'encrypt': ['openssl-c'],
                              'decrypt': ['d', 'NAKED']
                          },
                          depth: int = 1) -> dict:
        filepaths = Crawler.get_files(wd, extension=extension, depth=depth)
        if len(filepaths) <= 0:
            return {
                'status': 400,
                'message': 'Error: No files found.',
                'output': []
            }

        output = [
            self.encrypt_file(password,
                              filepath,
                              decrypt=decrypt,
                              keep_org=keep_org,
                              naked=naked,
                              tag_options=tag_options)['message']
            for filepath in tqdm(filepaths, desc='Progress')
        ]

        return {
            'status': 200,
            'message': 'Encrypt all files complete.',
            'output': output
        }
