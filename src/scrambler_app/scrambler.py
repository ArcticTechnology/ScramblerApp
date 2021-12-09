import os; import base64; import random; import json
import shlex; import subprocess
from os.path import isfile, isdir, join, exists
from getpass import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from .utils.dircrawler import DirCrawler as dc
from .utils.filemodder import FileModder as fm
from .utils.commoncmd import CommonCmd as cmd

class Scrambler:

	def timetravel(self,path,hours_ago=None):
		if hours_ago == None: hours_ago = random.randrange(1,121000)

		pathlex = shlex.quote(path)
		hourslex = shlex.quote(str(hours_ago))

		cmd = 'touch -d "{h} hours ago" {p}'.format(h=hourslex,p=pathlex)
		cmdlex = shlex.split(cmd)

		process = subprocess.run(cmdlex,
					stdout=subprocess.PIPE,stderr=subprocess.PIPE)

		returncode = process.returncode

		if returncode == 0:
			return 'DT changed for: ' + path
		else:
			return ('Error changing DT for: ' + path + '\n' +
									'Error Code: ' + process.stderr.decode())

	def timetravel_files(self, wd, extension):
		files = dc.get_files(wd, extension=extension)

		if len(files) <= 0: return 'No files found.'

		for f in files: print(self.timetravel(f))

		return 'Scramble files complete.'

	def timetravel_folders(self, wd):
		folders = dc.get_folders(wd)

		if len(folders) <= 0: return 'No folders found.'

		for folder in folders: print(self.timetravel(folder))

		print(self.timetravel(wd))

		return 'Scramble folders complete.'

	def stash(self, input_file_names, output_file_names, old_dir, new_dir, inverse=False):
		if output_file_names == '' or input_file_names == '':
			return 'Error: output and target cannot be blank.'

		if inverse == True:
			message = 'Retrieve complete.'
		else:
			message = 'Stash complete.'

		inputs = input_file_names.split(' ')
		outputs = output_file_names.split(' ')

		curr_files = []
		new_files = []

		for i in inputs:

			if len(i) > 0:
				curr_files.append(join(old_dir,i))

		for o in outputs:
			if inverse != True and exists(join(new_dir,o)) == True:
				return 'Error: file already exists in {}'.format(join(new_dir,o))

			if len(o) > 0:
				new_files.append(join(new_dir,o))

		if len(curr_files) != len(new_files):
			return 'Error: the number of input files and output files must equal.'

		for i in range(len(new_files)):
			if i < len(curr_files):
				if isfile(join(old_dir,curr_files[i])) != True:
					print('Not found: {}'.format(join(old_dir,curr_files[i])))
				else:
					if new_files[i] != '':
						print(cmd.cp_file(curr_files[i],new_files[i]))
						if inverse == True:
							print(self.timetravel(new_files[i]))
							print(self.timetravel(new_dir))
			else:
				break

		return message

	def stash_all(self, wd, config_data, inverse=False):
		target_dir = config_data['target_dir']
		if isdir(target_dir) != True:
			return 'Error: could not find target dir {}'.format(target_dir)

		nms = config_data['file_names']

		if inverse == True:
			input_file_names = ' '.join(list(nms.keys()))
			output_file_names = ' '.join(list(nms.values()))
			old_dir = wd
			new_dir = target_dir
		else:
			input_file_names = ' '.join(list(nms.values()))
			output_file_names = ' '.join(list(nms.keys()))
			old_dir = target_dir
			new_dir = wd

		return self.stash(input_file_names,output_file_names,old_dir,new_dir,inverse)

	def _get_fernettoken(self, password, salt_byte):
		pass_byte = bytes(password, encoding='utf-8')
		kdf = PBKDF2HMAC(
			algorithm=hashes.SHA256(),
			length=32,
			salt=salt_byte,
			iterations=320000,
			backend=default_backend())
		token = Fernet(base64.urlsafe_b64encode(kdf.derive(pass_byte)))

		del password; del pass_byte
		return token

	def _prepend_salt(self, encryption_results):
		if encryption_results['status'] != 200: return encryption_results['message']

		output = encryption_results['output']

		return output['hash'] + '.' + output['salt']

	def _extract_salt(self, message):
		if '.' in message:
			extension = dc._get_extension(message)
			return extension[1:]
		else:
			raise ValueError('Error: Failed to extract salt.')

	def openssl_enc(self, password, data, decrypt=False):
		# data = {'medium': 'file', 'input': '/filepath/example', 'outpath': '/example-c', 'salt': None}
		# data = {'medium': 'text', 'input': 'hello world', 'outpath': None, 'salt': None}
		medium_options = ['file', 'text']
		result = {'status': None, 'message': None, 'output': None}
		if type(data) != dict: return {'status': 200, 'message': 'Error: Input data incorrect format.'}
		if data['medium'] not in medium_options: return {'status': 200, 'message': 'Error: Invalid medium.'}

		passwd = shlex.quote(password)
		dashd = ' -d' if decrypt == True else ''
		keyword = 'Decrypt' if decrypt == True else 'Encrypt'

		if data['medium'] == 'text':
			# If ' or " in text throw an error Cannot garuntee quote char
			text = shlex.quote(data['input'])
			#c = 'echo "{t}" | openssl aes-256-cbc{d} -a -salt -pbkdf2 -k {p}'.format(
			#			t=text,d=dashd,p=passwd)

			pipetext = shlex.split('echo "{t}"'.format(t=text))
			command = shlex.split('openssl aes-256-cbc{d} -a -salt -pbkdf2 -k {p}'.format(
						d=dashd,p=passwd))
			pipe = subprocess.Popen(pipetext, stdout=subprocess.PIPE)
			process = subprocess.check_output(command, stdin=pipe.stdout)
			pipe.wait()
			# figure out how to get error
			raw_output = process.decode()
			# error handling the output
			clean1 = raw_output[:-1] if raw_output[-1] == "\n" else raw_output
			clean2 = clean1[:-1] if clean1[-1] == "'" else clean1
			clean3 = clean2[1:] if clean2[0] == "'" else clean2

			result['status'] = 200
			result['message'] = 'Success...'
			result['output'] = clean3
			return result

		if data['medium'] == 'file':
			try:
				filepath = shlex.quote(data['input'])
				outpath = shlex.quote(data['outpath'])
			except:
				return {'status': 200, 'message': 'Error: Invalid medium.'}

			c = 'openssl aes-256-cbc{d} -a -salt -pbkdf2 -in {f} -out {o} -k {p}'.format(
							d=dashd,f=filepath,o=outpath,p=passwd)
			command = shlex.split(c)
			process = subprocess.run(command,
							stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			#stdout = process.stdout.decode() #to see error code
			returncode = process.returncode

			if returncode == 0:
				result['status'] = 200
				result['message'] = '{}ed: '.format(keyword) + filepath
				return result
			else:
				result['status'] = 400
				result['message'] = 'Error {}ing: '.format(keyword) + filepath
				return result

	def encrypt_msg(self, message, password, salt=None, decrypt=False):
		result = {'status': None, 'message': None, 'output':{}}

		#=== Create Salt ===
		if decrypt==True:
			if type(salt) != str:
				result['status'] = 400
				result['message'] = 'Error: Salt of type str is required.'
				del password
				return result
			salt_byte = base64.urlsafe_b64decode(bytes(salt,'utf-8'))
		else:
			if salt != None:
				result['status'] = 400
				result['message'] = 'Error: Leave salt=None for encryption, it will auto-generate.'
				del password
				return result
			salt_byte = os.urandom(16)
			salt = base64.urlsafe_b64encode(salt_byte).decode('utf-8')

		msg_byte = bytes(message, encoding='utf-8')
		token = self._get_fernettoken(password, salt_byte)

		#=== Create Hash ===
		if decrypt==True:
			try:
				hash = base64.urlsafe_b64decode(msg_byte)
				hash_readable = token.decrypt(hash).decode('utf-8')
			except:
				result['status'] = 400
				result['message'] = 'Error: Unable to decrypt hash. Potentially invalid password or salt.'
				del password
				return result
		else:
			hash = token.encrypt(msg_byte)
			hash_readable = base64.urlsafe_b64encode(hash).decode('utf-8')

		result['status'] = 200
		result['message'] = 'Successfully completed.'
		result['output']['hash'] = hash_readable
		result['output']['salt'] = salt

		del password
		return result

	def encrypt_file(self,filepath,password,
					decrypt=False,keep_org=True,naked=False):

		result = {'status': None, 'message': None}
		keyword = 'Decrypt' if decrypt == True else 'Encrypt'

		tag_options = {'encrypt' : ['-c'],
			'decrypt' : ['-d', '-NAKED']}
 
		if decrypt == True:
			option = ' -d' #openssl
			index = 1 if naked == True else 0
			npath = fm.add_tag(filepath,tag_options['encrypt'],
								tag_options['decrypt'],tag_options['decrypt'][index])
		else:
			option = ' ' #openssl
			npath = fm.add_tag(filepath,tag_options['decrypt'],
								tag_options['encrypt'],tag_options['encrypt'][0])

		if npath == filepath:
			result['status'] = 400
			result['message'] = 'Action already performed on: ' + filepath 
			return result

### Openssl
		filelex = shlex.quote(filepath)
		passlex = shlex.quote(password)
		npathlex = shlex.quote(npath)

		cmd = 'openssl aes-256-cbc{o} -a -salt -pbkdf2 -in {f} -out {n} -k {p}'.format(
					o=option,f=filelex,n=npathlex,p=passlex)
		cmdlex = shlex.split(cmd)

		process = subprocess.run(cmdlex,
					stdout=subprocess.PIPE,stderr=subprocess.PIPE)
####


		travel = self.timetravel(npath)

		result['returncode'] = process.returncode
		result['stdout'] = process.stdout.decode()
		result['travel'] = travel

		if result['returncode'] != 0:
			result['status'] = 400
			result['message'] = ('{} Error for: '.format(keyword) + filepath + '\n' +
									'Error Code: ' + process.stderr.decode())
			os.remove(npath)
			del password; del passlex; return result

		if keep_org == True:
			result['status'] = 200
			result['message'] = ('Created: ' + npath + '\n' +
									'Kept Original: ' + filepath)
			del password; del passlex; return result

		try:
			os.remove(filepath)
			result['status'] = 200
			result['message'] = ('Created: ' + npath + '\n' +
								'Removed: ' + filepath)
		except:
			result['status'] = 400
			result['message'] = ('Created: ' + npath + '\n' +
								'Error Removing: ' + filepath)

		del password; del passlex; return result

	def encrypt_all_files(self, wd, password, extension=None,
					decrypt=False,keep_org=False,naked=False):
		filepaths = dc.get_files(wd, extension=extension)

		if len(filepaths) <= 0: return 'Error: No files found.'

		result = {}

		for filepath in filepaths:
			filenm = dc._get_pathnm(filepath)
			result[filenm] = self.encrypt_file(filepath,password,
							decrypt=decrypt,keep_org=keep_org,naked=naked)
			print(result[filenm]['message'])

		self.timetravel_folders(wd)

		del password; return result

	def load_config_old(self,wd):
		"""Config file structure:
			{'target_dir': '/dir/test', 'file_names': {
				'name1': 'linked_name1',
				'name2': 'linked_name2'}}
		"""
		config_file_path = join(wd,'config')

		if isfile(config_file_path) != True:
			return {'status': 400, 'message': 'No config file found.'}

		config_file = dc.read_file(config_file_path)

		if len(config_file) == 0:
			return {'status': 400, 'message': 'Config file empty.'}

		try:
			config = json.loads(''.join(config_file))
		except:
			return {'status': 400, 'message': 'Config file not structured correctly.'}

		if 'target_dir' not in config or 'file_names' not in config:
			return {'status': 400, 'message': 'target_dir and file_names not found in config file.'}

		if type(config['file_names']) is not dict:
			return {'status': 400, 'message': 'file_names is not of type dict in config file.'}

		return {'status': 200, 'message': 'Config file loaded successfully.',
				'data': config}

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
			keyword = 'decrypt'
			additional_needed = ', your salt, and your password.'
		else:
			keyword = 'encrypt'
			additional_needed = ' and a password.'

		cmd.cls()
		print('Please provide the message you want to {}{}'.format(keyword,additional_needed))
		print(' ')
		message = input('Input your message: ')
		if message == '': cmd.cls(); print('Exited, no action taken.'); return
		print(' ')

		if decrypt == True:
			try:
				salt = self.scrambler._extract_salt(message)
			except:
				salt = input('Input your salt: ')
				if salt == '': cmd.cls(); print('Salt cannot be blank, no action taken.'); return
				print(' ')
		else:
			salt = None

		password = getpass('Please enter password: ')
		if password == '': cmd.cls(); print('Password cannot be blank, no action taken.'); return

		if decrypt == True:
			confirm = password
		else:
			print(' ')
			confirm = getpass('Please confirm password: ')

		cmd.cls()
		if password != confirm: del password; del confirm; print('Password mismatch, no action taken.'); return

		result = self.scrambler.encrypt_msg(message,password,salt,decrypt)
		if result['status'] != 200: print(result['message']); return

		print('Status: successfully {}ed!'.format(keyword))
		print(' ')
		print('==== Output Details ====')
		print(' ')

		if decrypt == True:
			print('message: {}'.format(result['output']['hash']))
			print(' ')
			print('salt: {}'.format(result['output']['salt']))
		else:
			print('hash: {}'.format(self.scrambler._prepend_salt(result)))
			print(' ')
			print('Important: Salt is prepended after the "." at the end of the hash. Store it safely.')

		print(' ')
		del password; del confirm
		input()
		cmd.cls()
		return

	def option_enc_file(self, decrypt, keep_org, naked=False, all=False):
		wd = self.instance.wd
		extension = self.instance.extension

		if decrypt == True:
			keyword = 'decrypt'
			keywording = 'Decrypting'
		else:
			keyword = 'encrypt'
			keywording = 'Encrypting'

		if wd == None: cmd.cls(); print('Error: No directory set. Please set directory.'); return
		print(' ')

		if all == True:
			print('Are you sure you want to {} all {} files in the following [y/n]:'.format(
					keyword,extension))
			print(wd)
			print(' ')
			response = input(); cmd.cls()
			if response != 'y': print('Exited, no action taken.'); return
			if isdir(wd) != True: print('Invalid path, no action taken.'); return
			print(keywording + ' all ' + extension + ' in: ' + wd)
		else:
			print('Which file do you want to {}?'.format(keyword))
			filepath = input()
			if filepath == '': cmd.cls(); print('Exited, no action taken.'); return
			print(' ')
			print('Are you sure you want to {} the following [y/n]:'.format(keyword))
			print(filepath)
			print(' ')
			response = input(); cmd.cls()
			if response != 'y': print('Exited, no action taken.'); return
			if isfile(filepath) != True: print('Invalid file, no action taken.'); return
			print(keywording + ': ' + filepath)

		print(' ')
		password = getpass('Please enter password: ')
		if password == '': cmd.cls(); print('Password cannot be blank, no action taken.'); return

		if decrypt == True:
			confirm = password
		else:
			print(' ')
			confirm = getpass('Please confirm password: ')

		cmd.cls()
		if password != confirm: del password; del confirm; print('Password mismatch, no action taken.'); return

		print('{} started...'.format(keywording))

		if all == True:
			result = self.scrambler.encrypt_all_files(wd,password,extension=extension,
									decrypt=decrypt,keep_org=keep_org,naked=naked)
		else:
			result = self.scrambler.encrypt_file(filepath,password,
										decrypt=decrypt,keep_org=keep_org,naked=naked)
			print(result['message'])

		print(' ')
		print('{} complete.'.format(keywording))
		print(' ')
		del password; del confirm
		input()
		cmd.cls()
		return

	def run(self, decrypt):
		cmd.cls()

		while True:
			self.optionscreen(decrypt)
			select = input()

			if select not in ('1','2','3','4'):
				#'[1] A Message, [2] A File, [3] All Files, [4] Columns in a Dataframe'
				cmd.cls()
				print('Invalid selection. Try again.')
				break

			if select == '1':
				self.option_enc_msg(decrypt=decrypt)
				break

			if select == '2':
				if decrypt == True:
					self.option_enc_file(decrypt=decrypt,keep_org=True,naked=True)
				else:
					self.option_enc_file(decrypt=decrypt,keep_org=True)
				break

			if select == '3':
				if decrypt == True:
					self.option_enc_file(decrypt=decrypt,keep_org=False,all=True)
				else:
					self.option_enc_file(decrypt=decrypt,keep_org=False,all=True)
				break

			if select == '4':
				cmd.cls()
				print('Feature not yet available, no action taken.')
				break

class ScramblerGUI:

	def __init__(self, scrambler, instance, encryptiongui):
		self.scrambler = scrambler
		self.instance = instance
		self.encryptiongui = encryptiongui
		self.config = None

	def install_config(self):
		self.instance.set_cwd_as_wd()
		self.config = self.scrambler.load_config_old(self.instance.wd)
		if self.config['status'] == 200:
			print('(Config file installed.)')
		return self.config

	def splashscreen(self):
		cmd.cls()
		print('Welcome to the Scrambler!')

	def optionscreen(self):
		print(' ')
		print('What would you like to do?')
		print('(s) Set Dir, (e) Encrypt, (d) Decrypt, (st) Stash, (r) Retrieve, (t) Timetravel, (q) Quit')

	def wipscreen(self):
		cmd.cls()
		print('Feature not yet available, no action taken.')

	def option_s(self):
		print(' ')
		print('Which directory do you want to set?')
		wd = input()
		cmd.cls()

		if os.path.isdir(wd) != True:
			print('Invalid path, no action taken.')
		else:
			print('Directory set: ' + self.instance.set_wd(wd))

		return

	def option_st(self,inverse=False):
		has_config = False; target_dir = ''
		input_file_names = ''; output_file_names = ''

		if type(self.config) is dict and self.config['status'] == 200:
			has_config = True
			target_dir = self.config['data']['target_dir']

		# Get rid of the manual option ONLY allow the config option.
		if inverse == True:
			keywording = 'Retrieve'
			target_msg = 'Which directory are you retrieving the target files from?'
			confirm_msg = 'Are you sure you want to retrieve your files to the following [y/n]:'
		else:
			keywording = 'Stashing'
			target_msg = 'Which directory are the target files located that you want to stash?'
			confirm_msg = 'Are you sure you want to output your stashed files to the following [y/n]:'

		if self.instance.wd == None:
			cmd.cls()
			print('Error: No directory set. Please set directory.')
			return

		if has_config == False:
			print(' ')
			print('What do you want the name of your output file to be?')
			output_file_names = input()

			if output_file_names == '':
				cmd.cls()
				print('Exited, no action taken.')
				return

			print(' ')
			print('What is the name of your target file?')
			input_file_names = input()

			if input_file_names == '':
				cmd.cls()
				print('Exited, no action taken.')
				return

			print(' ')
			print(target_msg)
			target_dir = input()

			if target_dir == '':
				cmd.cls()
				print('Exited, no action taken.')
				return

		print(' ')
		print(confirm_msg)

		if inverse == True:
			print(target_dir)
		else:
			print(self.instance.wd)

		response = input()
		cmd.cls()

		if response == 'y':
			if os.path.isdir(self.instance.wd) == True:
				print('{} started...'.format(keywording))

				if has_config == True:
					print(self.scrambler.stash_all(
						wd = self.instance.wd,
						config_data = self.config['data'],
						inverse = inverse))
				else:
					if inverse == True:
						print(self.scrambler.stash(
							input_file_names = input_file_names,
							output_file_names = output_file_names,
							old_dir = self.instance.wd,
							new_dir = target_dir,
							inverse=True))
					else:
						print(self.scrambler.stash(
							input_file_names = input_file_names,
							output_file_names = output_file_names,
							old_dir = target_dir,
							new_dir = self.instance.wd))
				print(' ')
				input()
				cmd.cls()
			else:
				print('Invalid path, no action taken.')
		else:
			print('Exited, no action taken.')

	def option_t(self, extension):
		if self.instance.wd == None: cmd.cls(); print('Error: No directory set. Please set directory.'); return

		print(' ')
		print('Are you sure you want to timetravel the following [y/n]: ')
		print(self.instance.wd)
		print(' ')

		response = input(); cmd.cls()

		if response != 'y': print('Exited, no action taken.'); return
		if os.path.isdir(self.instance.wd) != True: print('Invalid path, no action taken.'); return

		print('Timetravel started...')
		self.scrambler.timetravel_files(self.instance.wd, extension=extension)
		self.scrambler.timetravel_folders(self.instance.wd)
		print('Timetravel complete.')
		print(' ')
		input()
		cmd.cls()
		return

	def option_pwd(self):
		cmd.cls()
		if self.instance.wd == None: 
			print('Error: No directory set. Please set directory.')

		print('Current directory: {}'.format(cmd.pwd()))

	def option_ls(self):
		cmd.cls()
		if self.instance.wd == None: print('Error: No directory set. Please set directory.')

		ls = cmd.ls()

		if len(ls) == 0:
			print('Directory is empty.')
		else:
			print(' '.join(ls))

		return

	def run(self):
		cmd.cls()
		self.splashscreen()
		self.install_config()

		while True:
			self.optionscreen()
			select = input()

			if select not in ['q','pwd','ls','s','e','d','st','r','t','q']:
				#'(s) Set Dir, (e) Encrypt, (d) Decrypt, (st) Stash, (r) Recall, (t) Timetravel, (q) Quit'
				cmd.cls(); print('Invalid selection. Try again.')

			if select == 'q':
				cmd.cls()
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

			if select == 'st':
				self.wipscreen()

			if select == 'r':
				self.wipscreen()

			if select == 't':
				self.option_t(extension=self.instance.extension)
