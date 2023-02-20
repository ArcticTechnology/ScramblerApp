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

import os; import random; import string
from typing import Type, Union
from .crawler import Crawler

class FileModder:

	@classmethod
	def read_file(self, filepath: str) -> list:
		lines = []
		with open(filepath,'r') as f:
			for line in f:
				if line[0] != '#':
					lines.append(line.rstrip('\n'))
		return lines

	@classmethod
	def read_line(self, filepath: str, linenum: int) -> str:
		with open(filepath,'r') as f:
			for n, line in enumerate(f):
				if n == linenum:
					return line.rstrip('\n')
		return ''

	@classmethod
	def _get_last_line(self, openedFile):
		try:
			openedFile.seek(-2, os.SEEK_END)
			while openedFile.read(1) != b'\n':
				openedFile.seek(-2, os.SEEK_CUR)
		except:
			pass

	@classmethod
	def read_last_line(self, filepath: str) -> str:
		with open(filepath, 'rb') as f:
			self._get_last_line(f)
			last_line = '\n' + f.readline().decode(errors='replace')
			return last_line

	@classmethod
	def format_ext(self, raw_extension: str, ifblank: str = '.txt',
				ifstar: Union[str, Type[None]] = None) -> Union[str, Type[None]]:
		if raw_extension == '*':
			return ifstar
		if raw_extension == '':
			return ifblank
		if raw_extension[0] != '.':
			return '.' + raw_extension
		else:
			return raw_extension

	@classmethod
	def add_tag(self, filepath: str, tag: str, oldtags: list = [],
				newtags: list = [], spliton: str = '-') -> str:
		newtags_complete = [spliton + t for t in newtags]
		oldtags_complete = [spliton + t for t in oldtags]

		rootdir = Crawler.get_rootdir(filepath)
		prefix = Crawler.get_prefix(filepath)
		extension = Crawler.get_extension(filepath)

		existing_tag = spliton + prefix.split(spliton)[-1]

		# If tag already applied then do not apply tag.
		if existing_tag in newtags_complete:
			return filepath

		if existing_tag in oldtags_complete:
			#If existing tag is in old tags, then update it to tag.
			filename = prefix.split(existing_tag)[0] + spliton + tag + extension
			return Crawler.joinpath(rootdir, filename)
		else:
			filename = prefix + spliton + tag + extension
			return Crawler.joinpath(rootdir, filename)

	@classmethod
	def add_randomized_tag(self, filepath: str, length: int = 5, spliton: str = '-') -> str:
		if length < 4: length = 4
		if length > 10: length = 10
		rootdir = Crawler.get_rootdir(filepath)
		prefix = Crawler.get_prefix(filepath)
		extension = Crawler.get_extension(filepath)
		rtag=''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
		filename = prefix + spliton + rtag + extension
		return Crawler.joinpath(rootdir, filename)
