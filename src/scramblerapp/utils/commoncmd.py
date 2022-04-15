# Common Commands
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

import shlex; import subprocess
from os import getcwd, listdir
from os.path import isfile, isdir
from ..dircrawler.crawler import Crawler

class CommonCmd:

	@classmethod
	def pwd(self, internal: bool = False) -> str:
		if internal: return Crawler.posixize(getcwd())

		command = 'pwd'
		process = subprocess.run(command,
			stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		returncode = process.returncode
		result = Crawler.posixize(process.stdout.decode().rstrip('\n'))
		if returncode == 0:
			return result
		else:
			return 'Error: unable to print working directory.'

	@classmethod
	def ls(self) -> list:
		files = [f for f in listdir('.') if isfile(f)]
		folders = [d for d in listdir('.') if isdir(d)]
		files.sort()
		folders.sort()
		return folders + files

	@classmethod
	def clear(self):
		subprocess.call('clear')

	@classmethod
	def copyfile(self, curr_filepath: str, new_filepath: str) -> dict:

		cfile = Crawler.escape(Crawler.posixize(curr_filepath))
		nfile = Crawler.escape(Crawler.posixize(new_filepath))

		command = shlex.split('cp {c} {n}'.format(c=cfile,n=nfile))
		print(command)
		process = subprocess.run(command,
			stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		returncode = process.returncode
		print(process.stderr.decode())
		if returncode == 0:
			return {'status': 200, 'message': 'File created: ' + str(new_filepath)}
		else:
			return {'status': 400, 'message': 'Error creating file for: ' + str(curr_filepath)}