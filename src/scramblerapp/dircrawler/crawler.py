# Dir Crawler
# Copyright (c) 2022 Arctic Technology LLC

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
from os.path import isfile, isdir, join, abspath
from types import NoneType
from typing import Union

class Crawler:

	@classmethod
	def stdpath(self, path: str) -> str:
		platform = os.name
		if platform == 'nt':
			result = abspath(path).replace('\\','/')
			if result[0:5] == 'C:/c/': return result.replace('C:/c/','C:/')
			return result
		else:
			return abspath(path)

	@classmethod
	def joinpath(self, path: str, filename: str) -> str:
		platform = os.name
		if platform == 'nt':
			result = abspath(join(path,filename)).replace('\\','/')
			if result[0:5] == 'C:/c/': return result.replace('C:/c/','C:/')
			return result
		else:
			return abspath(join(path, filename))

	@classmethod
	def get_filenm(self, path: str) -> str:
		result = self.stdpath(path)
		return result.split('/')[-1]

	@classmethod
	def get_prefix(self, filepath: str) -> str:
		return os.path.splitext(filepath)[0]

	@classmethod
	def get_extension(self, filepath: str) -> str:
		return os.path.splitext(filepath)[-1]

	@classmethod
	def get_folders(self, wd: str, fix=True) -> list:

		dpaths = []

		for root, dirname, _ in os.walk(wd):
			for d in dirname:
				dpath = self.joinpath(root,d)
				if isdir(dpath):
					if ' ' in d and fix == True:
						npath = os.rename(dpath,self.joinpath(root,d.replace(' ','_')))
						dpaths.append(npath)
					else:
						dpaths.append(dpath)

		return dpaths

	@classmethod
	def get_files(self, wd: str, extension: Union[str, NoneType] = None, fix: bool = True) -> list:

		filepaths = []

		for root, _ , files in os.walk(wd):
			for f in files:
				filepath = self.joinpath(root,f)
				if isfile(filepath):
					if ' ' in f and fix == True:
						npath = os.rename(filepath,self.joinpath(root,f.replace(' ','_')))
						filepaths.append(npath)
					else:
						filepaths.append(filepath)

		if extension == None or len(filepaths) == 0:
			return filepaths

		result = []

		for filepath in filepaths:
			if self.get_extension(filepath) == extension:
				result.append(filepath)

		return result