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
from ..dircrawler.crawler import Crawler
from ..utils.encryption import OpenSSLEncyptor

class Instance:

	def __init__(self):
		self.wd = None
		openssl = OpenSSLEncyptor.get_version()
		if openssl['status'] == 400:
			failure_msg1 = '\n OpenSSL is required to run this app. Make sure you have OpenSSL installed.'
			failure_msg2 = '\n Use command ```openssl version``` to check your openssl version.'
			raise Exception(openssl['message'] + ' ' + failure_msg1 + ' ' + failure_msg2)

		self.version_text = openssl['message']

	def clear_wd(self) -> dict:
		self.wd = None
		return {'status': 200, 'message': 'Working directory cleared.'}

	def set_wd(self, raw_wd: str) -> dict:
		if raw_wd == '': return {'status': 400,
					'message': 'Invalid input, no action taken.'}
		wd = Crawler.posixize(raw_wd)
		if os.path.isdir(wd) == False:
			return {'status': 400, 'message': 'Invalid input, no action taken.'}
		self.wd = wd
		os.chdir(wd)
		return {'status': 200, 'message': 'Working directory set: {}'.format(wd)}

	def set_cwd_as_wd(self) -> dict:
		curr_dir = os.getcwd()
		wd = Crawler.posixize(curr_dir)
		if os.path.isdir(wd) == False:
			return {'status': 400, 'message': 'Invalid input, no action taken.'}
		self.wd = wd
		return {'status': 200, 'message': 'Working directory set: {}'.format(wd)}
