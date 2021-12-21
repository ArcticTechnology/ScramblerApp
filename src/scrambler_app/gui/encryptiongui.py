from os.path import isfile, isdir
from getpass import getpass
from ..utils.commoncmd import CommonCmd as cmd

class EncryptionGUI:

	def __init__(self, scrambler, instance):
		self.scrambler = scrambler
		self.instance = instance

	def optionscreen(self, decrypt=False):
		if decrypt == True:
			keyword = 'DECRYPT'
		else:
			keyword = 'ENCRYPT'

		print('What would you like to {}?'.format(keyword))
		print('[1] A Message, [2] A File, [3] All Files, [4] Columns in a Dataframe')

	def option_enc_msg(self, decrypt=False):
		if decrypt == True:
			keyword = 'Decrypt'
			pass_msg = 'Password: '
		else:
			keyword = 'Encrypt'
			pass_msg = 'Password (>=16 chars required): '
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
			if len(password) <= 15:
				cmd.clear(); print('Password must be 16 characters or more, no action taken.')
				del password; return
			print(' ')
			confirm = getpass('Please confirm password: ')

		cmd.clear()
		if password != confirm: del password; del confirm; print('Password mismatch, no action taken.'); return

		result = self.scrambler.encrypt_msg(password,message,decrypt)
		if result['status'] != 200: print(result['message']); return

		print('{}ion complete.'.format(keyword))
		print(' ')

		if decrypt == True:
			print('secret: {}'.format(result['output']))
		else:
			print('hash: {}'.format(result['output']))
		print(' ')
		print('Press any key to exit.')
		del password; del confirm
		input(); cmd.clear(); return

	def option_enc_file(self, decrypt, keep_org, naked=False, all=False):
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
			pass_msg = 'Password (>=16 chars required): '

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
			extension = self.scrambler.formatted_ext(raw_extension)
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
			if len(password) <= 15: cmd.clear(); print('Password must be 16 characters or more, no action taken.'); return
			print(' ')
			confirm = getpass('Please confirm password: ')

		cmd.clear()
		if password != confirm: del password; del confirm; print('Password mismatch, no action taken.'); return

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
		del password; del confirm
		input(); cmd.clear(); return

	def run(self, decrypt):
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