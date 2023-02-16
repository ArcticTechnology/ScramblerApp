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

import shlex; import subprocess
from os import remove
from os.path import isdir, exists
from typing import Type, Union
from random import randrange
from datetime import datetime, timedelta
from .dircrawler.crawler import Crawler
from .dircrawler.filemodder import FileModder
from .utils.commoncmd import CommonCmd as cmd
from .utils.encryption import OpenSSLEncyptor as ossl

class Scrambler:

	def random_time(self) -> str:
		end = datetime.now()
		start = datetime.strptime('1/1/2005 12:00 AM', '%m/%d/%Y %I:%M %p')
		delta = end - start
		int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
		random_second = randrange(int_delta)
		return str(start + timedelta(seconds=random_second))

	def timetravel(self, path: str) -> dict:
		ppath = Crawler.escape(Crawler.posixize(path))
		command = shlex.split('touch -d "{t}" {p}'.format(t=self.random_time(),p=ppath))
		process = subprocess.run(command,
					stdout=subprocess.PIPE,stderr=subprocess.PIPE)

		returncode = process.returncode

		if returncode == 0:
			return {'status': 200, 'message': 'Timetravelled: ' + str(path)}
		else:
			return {'status': 400, 'message': 'Error timetravelling: ' + str(path)}

	def timetravel_files(self, path: str,
						extension: Union[str, Type[None]] = None) -> dict:
		files = Crawler.get_files(path, extension=extension)

		if len(files) <= 0:
			return {'status': 400, 'message': 'Error timetravelling: no files found.', 'output': []}

		output = [self.timetravel(f)['message'] for f in files]
		return {'status': 200, 'message': 'Timetravel files complete.', 'output': output}

	def timetravel_folders(self, path: str) -> dict:
		folders = Crawler.get_folders(path)

		if exists(path) != True:
			return {'status': 400, 'message': 'Error timetravelling: no directory found.', 'output': []}

		if len(folders) <= 0:
			output = ['No folders found to timetravel, no action taken.']
		else:
			output = [self.timetravel(folder)['message'] for folder in folders]

		output.append(self.timetravel(path)['message'])

		return {'status': 200, 'message': 'Timetravel folders complete.', 'output': output}

	def encrypt_msg(self, password: str, message: str, decrypt: bool = False) -> dict:
		data = {'format': 'text', 'input': message, 'outpath': None}
		result = ossl.encrypt(password, data, decrypt)
		return result

	def encrypt_file(self, password: str, filepath: str, decrypt: bool = False,
					keep_org: bool = False, naked: bool = False) -> dict:
		result = {'status': None, 'message': None}
		tag_options = {'encrypt' : ['c'],
			'decrypt' : ['d', 'NAKED']}

		if decrypt == True:
			index = 1 if naked == True else 0
			tag = tag_options['decrypt'][index]
			oldtags = tag_options['encrypt']
			newtags = tag_options['decrypt']
		else:
			tag = tag_options['encrypt'][0]
			oldtags = tag_options['decrypt']
			newtags = tag_options['encrypt']

		clean_filepath = Crawler.posixize(filepath)
		outpath = FileModder.add_tag(clean_filepath,tag,oldtags,newtags)

		if exists(clean_filepath) == False:
			result['status'] = 400
			result['message'] = 'Error failed to find file: ' + str(clean_filepath)
			return result

		if exists(outpath) == True:
			result['status'] = 400
			result['message'] = 'Error output path already exists: ' + str(outpath)
			return result

		if outpath == clean_filepath:
			result['status'] = 400
			result['message'] = 'Action already performed on: ' + str(clean_filepath)
			return result

		data = {'format': 'file', 'input': clean_filepath, 'outpath': outpath}
		response = ossl.encrypt(password, data, decrypt)
		if response['status'] == 400:
			try:
				remove(outpath)
			except:
				pass
			return response

		self.timetravel(outpath)

		if keep_org == True:
			result['status'] = response['status']
			result['message'] = response['message'] + ' (original retained).'
			return result

		try:
			remove(clean_filepath)
			result['status'] = 200
			result['message'] = response['message'] + ' (original deleted).'
		except:
			result['status'] = 400
			result['message'] = response['message'] + ' (Error deleting original).'

		return result

	def encrypt_all_files(self, password: str, wd: str,
					extension: Union[str, Type[None]] = None, decrypt: bool = False,
					keep_org: bool = False, naked: bool = False) -> dict:
		filepaths = Crawler.get_files(wd, extension=extension)
		if len(filepaths) <= 0: return {'status': 400, 'message': 'Error: No files found.', 'output': []}

		output = [self.encrypt_file(password,filepath,decrypt=decrypt,
					keep_org=keep_org,naked=naked)['message'] for filepath in filepaths]

		timetravel = self.timetravel_folders(wd)
		if timetravel['status'] != 200 or len(timetravel['output']) == 0:
			output.append('Error timetravelling folders, timetravelling skipped.')
		else:
			for o in timetravel['output']: output.append(o)

		return {'status': 200, 'message': 'Encrypt all files complete.', 'output': output}

class ScramblerGUI:

	def __init__(self, scrambler, instance, encryptiongui):
		self.scrambler = scrambler
		self.instance = instance
		self.encryptiongui = encryptiongui

	def splashscreen(self):
		cmd.clear()
		print('Welcome to the Scrambler!')

	def optionscreen(self):
		print('version: ' + self.instance.version_text)
		print(' ')
		print('What would you like to do?')
		print('(s) Set Dir, (e) Encrypt, (d) Decrypt, (t) Timetravel, (q) Quit')

	def comingsoon(self):
		cmd.clear()
		print('Feature not yet available, no action taken.')

	def option_pwd(self):
		cmd.clear()
		if self.instance.wd == None:
			print('Error: No working directory set. Please set working directory first.'); return
		else:
			print('Working directory: {}'.format(cmd.pwd())); return

	def option_ls(self):
		cmd.clear()
		if self.instance.wd == None:
			print('Error: No working directory set. Please set working directory first.'); return

		ls = cmd.ls()

		if len(ls) == 0:
			print('Working directory is empty.'); return
		else:
			print(' '.join(ls)); return

	def option_s(self):
		print(' ')
		print('What directory do you want to set as your working directory?')
		raw_wd = input()
		cmd.clear()
		setwd = self.instance.set_wd(raw_wd)
		print(setwd['message'])
		return

	def option_t(self):
		cmd.clear()
		if self.instance.wd == None:
			print('Error: No working directory set. Please set working directory first.'); return

		print('Warning: You are about to timetravel all files and folders in the following directory and its subdirectories.')
		print('Timetravel will alter the metadata to a scrambled date/time in the past of everything in:')
		print(self.instance.wd)
		print(' ')
		print('You may specify a file type. Leaving blank will default to .txt files.')
		print('Use * for all files regardless of type (this can be dangerous).')
		print(' ')
		raw_extension = input('Specify a file type [Optional]: ')
		extension = FileModder.format_ext(raw_extension, ifblank='.txt')
		print(' ')
		if extension == None:
			confirm = input('Are you sure you want to timetravel all folders and files of all types [y/n]: ')
		else:
			confirm = input('Are you sure you want to timetravel all folders and files with extension {} [y/n]: '.format(extension))
		cmd.clear()
		if confirm != 'y': print('Exited, no action taken.'); return
		if isdir(self.instance.wd) != True: print('Invalid path, no action taken.'); return

		print('Timetravel started...')
		tt_files = self.scrambler.timetravel_files(self.instance.wd, extension=extension)
		if tt_files['status'] != 200 or len(tt_files['output']) == 0:
			print('No files found to timetravel, no action taken.')
		else:
			for f in tt_files['output']: print(f)

		tt_folders = self.scrambler.timetravel_folders(self.instance.wd)
		if tt_folders['status'] != 200 or len(tt_folders['output']) == 0:
			print('No folders found to timetravel, no action taken.')
		else:
			for folder in tt_folders['output']: print(folder)

		print(' ')
		print('Timetravel complete.')
		input(); cmd.clear(); return

	def run(self):
		cmd.clear()
		self.splashscreen()

		while True:
			self.optionscreen()
			select = input()

			if select not in ('pwd','ls','s','e','d','t','q'):
				#'(s) Set Dir, (e) Encrypt, (d) Decrypt, (t) Timetravel, (q) Quit'
				cmd.clear(); print('Invalid selection. Try again.')

			if select == 'q':
				cmd.clear()
				break

			if select == 'pwd':
				self.option_pwd()

			if select == 'ls':
				self.option_ls()

			if select == 's':
				self.option_s()

			if select == 'e':
				self.encryptiongui.run(decrypt=False)

			if select == 'd':
				self.encryptiongui.run(decrypt=True)

			if select == 't':
				self.option_t()
