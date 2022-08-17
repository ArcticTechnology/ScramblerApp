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

from os.path import isfile, isdir
from getpass import getpass
from ..dircrawler.filemodder import FileModder
from ..utils.commoncmd import CommonCmd as cmd

class EncryptionGUI:

	def __init__(self, scrambler, instance):
		self.scrambler = scrambler
		self.instance = instance

	def optionscreen(self, decrypt: bool = False):
		if decrypt == True:
			keyword = 'DECRYPT'
		else:
			keyword = 'ENCRYPT'

		print('What would you like to {}?'.format(keyword))
		print('[1] A Message, [2] A File, [3] All Files, [4] Columns in a Dataframe')

	def option_enc_msg(self, decrypt: bool = False):
		if decrypt == True:
			keyword = 'Decrypt'
			pass_msg = 'Password: '
		else:
			keyword = 'Encrypt'
			pass_msg = 'Password (>10 chars required): '
		cmd.clear()
		print('What is the message you want to {}?'.format(keyword.upper()))
		print(' ')
		message = input('Input your message: ')
		if message == '': cmd.clear(); print('Exited, no action taken.'); return
		print(' ')

		password = getpass(pass_msg)
		if password == '':
			cmd.clear(); print('Password cannot be blank, no action taken.'); return

		if decrypt == True:
			confirm = password
		else:
			if len(password) < 10:
				cmd.clear(); print('Password must greater than 10 characters, no action taken.')
				return
			print(' ')
			confirm = getpass('Please confirm password: ')

		cmd.clear()
		if password != confirm: print('Password mismatch, no action taken.'); return

		result = self.scrambler.encrypt_msg(password,message,decrypt)
		if result['status'] != 200: print(result['message']); return

		print('{}ion complete.'.format(keyword))
		print(' ')

		if decrypt == True:
			print('secret: {}'.format(result['output']))
		else:
			print('cipher: {}'.format(result['output']))
		print(' ')
		print('Press any key to exit.')
		input(); cmd.clear(); return

	def option_enc_file(self, decrypt: bool, keep_org: bool,
						naked: bool = False, all: bool = False):
		wd = self.instance.wd

		if decrypt == True:
			keyword = 'decrypt'
			keywording = 'Decrypting'
			keywordion = 'Decryption'
			pass_msg = 'Password: '
		else:
			keyword = 'encrypt'
			keywording = 'Encrypting'
			keywordion = 'Encryption'
			pass_msg = 'Password (>10 chars required): '

		if wd == None: cmd.clear(); print('Error: No working directory set. Please set working directory first.'); return

		if all == True:
			cmd.clear()
			print('Warning: You are about to {} all files in the following directory and its subdirectories.'.format(keyword.upper()))
			print('This will OVERWRITE the original files. Make sure to backup the contents of this directory:')
			print(wd)
			print(' ')
			print('You may specify a file type to {}. Leave blank for default .txt files.'.format(keyword))
			print('Use * to {} all files regardless of type (this can be dangerous).'.format(keyword))
			print(' ')
			raw_extension = input('Specify a file type [Optional]: ')
			extension = FileModder.format_ext(raw_extension)
			print(' ')
			if extension == None:
				confirm = input('Are you sure you want to {} all files of all types [y/n]: '.format(
					keyword))
			else:
				confirm = input('Are you sure you want to {} all files with extension {} [y/n]: '.format(
					keyword,extension))
			cmd.clear()
			if confirm != 'y': print('Exited, no action taken.'); return
			if isdir(wd) != True: print('Invalid path, no action taken.'); return
			if extension == None:
				print(keywording + ' all files in: ' + wd)
			else:
				print(keywording + ' all ' + extension + ' in: ' + wd)
		else:
			print(' ')
			print('Which file do you want to {}?'.format(keyword.upper()))
			filename = input()
			if filename == '': cmd.clear(); print('Exited, no action taken.'); return
			print(' ')
			print('Are you sure you want to {} the following [y/n]:'.format(keyword))
			print(filename)
			confirm = input(); cmd.clear()
			if confirm != 'y': print('Exited, no action taken.'); return
			if isfile(filename) != True: print('Invalid file, no action taken.'); return
			print(keywording + ': ' + filename)

		print(' ')
		password = getpass(pass_msg)
		if password == '': cmd.clear(); print('Password cannot be blank, no action taken.'); return

		if decrypt == True:
			confirm = password
		else:
			if len(password) < 10: cmd.clear(); print('Password must greater than 10 characters, no action taken.'); return
			print(' ')
			confirm = getpass('Please confirm password: ')

		cmd.clear()
		if password != confirm: print('Password mismatch, no action taken.'); return

		print('{} started...'.format(keywordion))

		if all == True:
			result = self.scrambler.encrypt_all_files(password,wd,extension=extension,
							decrypt=decrypt,keep_org=keep_org,naked=naked)
			if result['status'] != 200:
				print(result['message'])
			else:
				for output in result['output']: print(output)
		else:
			result = self.scrambler.encrypt_file(password,filename,
							decrypt=decrypt,keep_org=keep_org,naked=naked)
			print(result['message'])

		print(' ')
		print('{} complete.'.format(keywordion))
		input(); cmd.clear(); return

	def run(self, decrypt: bool):
		cmd.clear()
		print(' ')
		self.optionscreen(decrypt)
		select = input()

		if select not in ('1','2','3','4'):
			#'[1] A Message, [2] A File, [3] All Files, [4] Columns in a Dataframe'
			cmd.clear()
			print('Invalid selection. Try again.')
			return

		if select == '1':
			self.option_enc_msg(decrypt=decrypt)
			return

		if select == '2':
			if decrypt == True:
				self.option_enc_file(decrypt=decrypt,keep_org=True,naked=True)
			else:
				self.option_enc_file(decrypt=decrypt,keep_org=True)
			return

		if select == '3':
			if decrypt == True:
				self.option_enc_file(decrypt=decrypt,keep_org=False,all=True)
			else:
				self.option_enc_file(decrypt=decrypt,keep_org=False,all=True)
			return

		if select == '4':
			cmd.clear()
			print('Feature not yet available, no action taken.')
			return