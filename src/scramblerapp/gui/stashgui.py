from os.path import isfile
from getpass import getpass
from ..utils.commoncmd import CommonCmd as cmd

class StashGUI:

	def __init__(self, scrambler, instance, configparser):
		self.scrambler = scrambler
		self.instance = instance
		self.configparser = configparser

	def noconfig_warning(self):
		cmd.clear()
		print('Warning: Config file not found or empty. This is required to use Stash.')
		print(' ')
		print('Instructions on creating a config file:')
		print('1) Create your .config based off of .config-template')
		print('2) Place your .config file into {}'.format(self.configparser.rootpath))
		print('3) [Optional] Encrypt your .config file with this app (this will create .config-c)')
		print('4) [Optional] Delete your original .config file once .config-c is created')
		print(' ')
		print('See .config-template file as an example, located in:')
		print(self.configparser.rootpath)
		print(' ')
		print('Press any key to exit.')
		input(); cmd.clear(); return

	def optionscreen(self):
		if self.configparser.hasEncyptedTag() == False:
			print('Warning: Your .config does not appear to be encrypted! Be sure to encrypt it.')
		print(' ')
		print('What would you like to do?')
		print('[1] Stash files, [2] Retrieve stashed files, [3] Encrypt config file.')

	def option_enc_config(self):
		filepath = self.configparser.filepath
		if self.configparser.hasEncyptedTag() == True:
			cmd.clear()
			print('No action taken, .config-c appears to be encrypted already:')
			print(filepath)
			return
		print(' ')
		print('Are you sure you want to encrypt the following [y/n]:')
		print(filepath)
		confirm = input(); cmd.clear()
		if confirm != 'y': print('Exited, no action taken.'); return
		if isfile(filepath) != True: print('Invalid file, no action taken.'); return

		print('Encrypting: ' + filepath)
		print(' ')
		password = getpass('Password (>=16 chars required): ')
		if password == '': cmd.clear(); print('Password cannot be blank, no action taken.'); return
		if len(password) <= 15: 
			cmd.clear(); print('Password must be 16 characters or more, no action taken.')
			return
		print(' ')
		confirm = getpass('Please confirm password: ')
		cmd.clear()
		if password != confirm: print('Password mismatch, no action taken.'); return

		print('Encryption started...')
		result = self.scrambler.encrypt_file(password,filepath,
							decrypt=False,keep_org=False,naked=False)
		print(result['message'])
		print(' ')
		print('Encryption complete.')
		print(' ')
		input(); cmd.clear(); return

	def option_stash(self, inverse=False):
		"""
		Data format:
		{"origin_dir": "/home/origin_directory/",
		"stash_dir": "/home/stash_directory/",
		"stash_key": {
		"filename1": "stashed_filename1",
		"filename2": "stashed_filename2",
		"filename3": "stashed_filename3"}}
		"""
		print(' ')
		if self.configparser.hasEncyptedTag():
			print('Please enter the password to the .config-c file.')
			print(' ')
			password = getpass('Password: ')
			print(' ')
			if password == '': cmd.clear(); print('Password cannot be blank, no action taken.'); return
		else:
			password = None

		parser = self.configparser.parse(password)
		if parser['status'] != 200:
			cmd.clear(); print('Attempting to parse config file...')
			print(' ')
			if parser['status'] == 405:
				print('Error: config file formatted incorrectly.')
				print('Your config file should be formatted like .config-template before encrypting it.')
			else:
				print(parser['message'])
			print(' '); print('Press any key to exit.')
			input(); cmd.clear()
			print('Exited. No action taken.')
			return

		data = parser['output']
		if self.scrambler.invalid_stash_data(data):
			cmd.clear(); print('Attempting to parse config file...')
			print(' '); print('Error: config file formatted incorrectly.')
			print('Your config file should be formatted like .config-template before encrypting it.')
			print(' '); print('Press any key to exit.')
			input(); cmd.clear()
			print('Exited. No action taken.')
			return

		if password != None: cmd.clear(); print('Password to .config-c accepted!'); print(' ')
		if inverse == True:
			keyword = 'Retrieve'
			print('Are you sure you want to retrieve your stashed files to the following directory? [y/n]')
		else:
			keyword = 'Stash'
			print('Are you sure you want to stash files located in the following directory? [y/n]')
		print(data['origin_dir'])
		confirm = input()
		if confirm != 'y': cmd.clear(); print('Exited, no action taken.'); return

		cmd.clear()
		print('{} started...'.format(keyword))

		response = self.scrambler.stash_all(data, inverse=inverse)
		if response['status'] != 200:
			print(' '); print(response['message'])
			print(' '); print('Press any key to exit.')
			input(); cmd.clear()
			print('Exited. No action taken.')
			return

		for output in response['output']:
			print(output)

		print(' ')
		print(response['message'])
		input(); cmd.clear(); return

	def run(self):
		cmd.clear()
		load = self.configparser.load_config()
		if load['status'] != 200:
			self.noconfig_warning()
			print('Exited. No action taken.')
			return

		self.optionscreen()
		select = input()

		if select not in ('1','2','3'):
			#'[1] Stash files, [2] Retrieve stashed files, [3] Encrypt config file.'
			cmd.clear()
			print('Invalid selection. Try again.')
			return

		if select == '1':
			self.option_stash()
			return

		if select == '2':
			self.option_stash(inverse=True)
			return

		if select == '3':
			self.option_enc_config()
			return