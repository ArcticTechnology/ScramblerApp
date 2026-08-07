# Dir Crawler
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
import re
import shlex
from os.path import basename, dirname, isdir, isfile, join
from typing import Type, Union


class Crawler:

    @classmethod
    def posixize(self, path: str) -> str:
        """
        If nt then replace any backslash with forwardslash that is
        preceding a non-whitespace character, and replace C:/c/ with C:/.
        """
        platform = os.name
        if platform == 'nt':
            formatted = re.sub(r'\\(?=\S)', r'/', path)
            if formatted[0:5] == 'C:/c/':
                formatted = formatted.replace('C:/c/', 'C:/')
            return formatted
        else:
            return path

    @classmethod
    def escape(self, path: str) -> str:
        """
        Use safe escaping.
        """
        return shlex.quote(path)

    @classmethod
    def joinpath(self, path: str, filename: str) -> str:
        joined = join(path, filename)
        return self.posixize(joined)

    @classmethod
    def get_basename(self, path: str) -> str:
        """Gets the file name if file or folder name if folder"""
        return basename(self.posixize(path))

    @classmethod
    def get_rootdir(self, path: str) -> str:
        return dirname(self.posixize(path))

    @classmethod
    def get_prefix(self, filepath: str) -> str:
        return self.get_basename(os.path.splitext(filepath)[-2])

    @classmethod
    def get_extension(self, filepath: str) -> str:
        return os.path.splitext(filepath)[-1]

    @classmethod
    def get_folders(self, wd: str) -> list:
        paths = []
        for root, dirname, _ in os.walk(wd):
            for d in dirname:
                path = self.joinpath(root, d)
                if isdir(path):
                    paths.append(path)
        return paths

    @classmethod
    def get_files(self,
                  wd: str,
                  extension: Union[str, Type[None]] = None,
                  depth: int = 1) -> list[str]:
        filepaths: list[str] = []
        for root_dir, sub_dirs, files_in_sub_dirs in os.walk(wd):
            # Stop traversal
            if depth <= 0:
                sub_dirs.clear()

            elif root_dir.rstrip(os.sep).count(os.sep) - wd.rstrip(
                    os.sep).count(os.sep) >= depth:
                # From official Python documentation:
                #
                # When topdown is True, the caller can modify the dirnames list
                # in-place (perhaps using del or slice assignment), and walk()
                # will only recurse into the subdirectories whose names remain
                # in dirnames; this can be used to prune the search, impose a
                # specific order of visiting, or even to inform walk() about
                # directories the caller creates or renames before it resumes
                # walk() again.
                #
                # Reset list: stop traversal.
                sub_dirs.clear()

            for f in files_in_sub_dirs:
                filepath = self.joinpath(root_dir, f)
                if isfile(filepath):
                    filepaths.append(filepath)

        if extension == None or len(filepaths) == 0:
            return filepaths

        result: list[str] = []
        for filepath in filepaths:
            if self.get_extension(filepath) == extension:
                result.append(filepath)

        return result
