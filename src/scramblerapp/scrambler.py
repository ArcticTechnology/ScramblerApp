import shlex; import subprocess
from random import randrange
from datetime import datetime, timedelta
from os import remove
from os.path import isfile, isdir, exists
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
		command = shlex.split('touch -d "{t}" "{p}"'.format(t=self.random_time(),p=path))
		process = subprocess.run(command,
					stdout=subprocess.PIPE,stderr=subprocess.PIPE)

		returncode = process.returncode

		if returncode == 0:
			return {'status': 200, 'message': 'Timetravelled: ' + str(path)}
		else:
			return {'status': 400, 'message': 'Error timetravelling: ' + str(path)}

	def timetravel_files(self, dir, extension=None):
		files = Crawler.get_files(dir, extension=extension)

		if len(files) <= 0: return {'status': 400, 'message': 'Error timetravelling: no files found.', 'output': []}

		output = [self.timetravel(f)['message'] for f in files]
		return {'status': 200, 'message': 'Timetravel files complete.', 'output': output}

	def timetravel_folders(self, dir):
		folders = Crawler.get_folders(dir)

		if exists(dir) != True: return {'status': 400, 'message': 'Error timetravelling: no directory found.', 'output': []}

		if len(folders) <= 0:
			output = ['No folders found to timetravel, no action taken.']
		else:
			output = [self.timetravel(folder)['message'] for folder in folders]

		output.append(self.timetravel(dir)['message'])

		return {'status': 200, 'message': 'Timetravel folders complete.', 'output': output}

	def invalid_stash_data(self, data):
		no_origin_dir = 'origin_dir' not in data
		no_stash_dir = 'stash_dir' not in data
		no_stash_key = 'stash_key' not in data
		if no_origin_dir or no_stash_dir or no_stash_key:
			return True
		if type(data['origin_dir']) != str or type(data['stash_dir']) != str:
			return True
		if type(data['stash_key']) != dict:
			return True
		stash_key = data['stash_key']
		keys = list(stash_key.keys())
		values = list(stash_key.values())
		if len(keys) == 0 or len(values) == 0: return True
		if len(keys) != len(values): return True
		return False

	def stash(self, curr_filename, curr_dir, new_filename, new_dir, overwrite=False, remove=False, retrieve=False):
		curr_filepath = Crawler.joinpath(curr_dir, curr_filename)
		result = {'status': None, 'message': None}

		if exists(curr_filepath) != True:
			result['status'] = 400
			if retrieve == True:
				result['message'] = 'Error: Retrieval failed, specified file not found in stashed directory.'
			else:
				result['message'] = 'Error: File not found {}'.format(curr_filepath)
			return result

		if isfile(curr_filepath) != True: 
			result['status'] = 400
			if retrieve == True:
				result['message'] = 'Error: Retrieval failed, specified file in stashed directory is corrupt.'
			else:
				result['message'] = 'Error: File is corrupt {}'.format(curr_filepath)
			return result

		new_filepath = Crawler.joinpath(new_dir, new_filename)
		if exists(new_filepath) == True and overwrite == False:
			result['status'] = 400
			if retrieve == True:
				result['message'] = 'Error: File already exists {}'.format(new_filepath)
			else:
				result['message'] = 'Error: Stash failed, file already exists in stashed directory.'
			return result

		response = cmd.copyfile(curr_filepath,new_filepath)
		if response['status'] != 200: return response
		self.timetravel(new_filepath)
		if remove == True: 
			try:
				remove(curr_filepath)
			except:
				if retrieve == True:
					result['message'] = 'Error: Failed to remove file from stashed directory'
				else:
					result['message'] = 'Error: Failed to remove {}'.format(curr_filepath)
		return response

	def stash_all(self, data, retrieve=False):
		"""
		Data format:
		{"origin_dir": "/home/origin_directory/",
		"stash_dir": "/home/stash_directory/",
		"stash_key": {
		"filename1": "stashed_filename1",
		"filename2": "stashed_filename2",
		"filename3": "stashed_filename3"}}
		"""
		result = {'status': None, 'message': None, 'output': []}
		origin_dir = data['origin_dir']
		stash_dir = data['stash_dir']

		if isdir(origin_dir) == False: return {'status': 400,
				'message': 'Error: Could not find origin directory {}'.format(origin_dir), 'output': []}

		if isdir(stash_dir) == False: return {'status': 400,
				'message': 'Error: Could not find stash directory. Directory invalid or missing.', 'output': []}

		stash_key = data['stash_key']
		keys = list(stash_key.keys())
		values = list(stash_key.values())
		statuscodes = []

		for i in range(len(keys)):
			if keys[i] == '' or values[i] == '': return {'status': 400,
				'message': 'Error: Invalid config file, keys and values cannot be blank.',
				'output': []}

		for i in range(len(keys)):
			if retrieve == True:
				response = self.stash(values[i],stash_dir,keys[i],origin_dir,
										overwrite=False,remove=False,retrieve=retrieve)
			else:
				response = self.stash(keys[i],origin_dir,values[i],stash_dir,
										overwrite=True,remove=True,retrieve=retrieve)
			statuscodes.append(response['status'])
			result['output'].append(response['message'])

		if retrieve == True:
			keyword = 'Retrieve'
			if len(statuscodes) > 1 and 200 not in statuscodes:
				result['status'] = 400
				result['message'] = 'Error: No stashed files retrieved. Specified files did not exist.'
				return result
		else:
			keyword = 'Stash'
			if len(statuscodes) > 1 and 200 not in statuscodes:
				result['status'] = 400
				result['message'] = 'Error: No files to stash found in {}'.format(origin_dir)
				return result
			timetravel = self.timetravel(stash_dir)
			if timetravel['status'] == 200:
				result['output'].append('Timetravel completed for stash directory.')
			else:
				result['output'].append('Error timetravelling stash directory.')

		result['status'] = 200
		result['message'] = '{} completed.'.format(keyword)
		return result

	def encrypt_msg(self, password, message, decrypt=False):
		data = {'format': 'text', 'input': message, 'outpath': None}
		result = ossl.encrypt(password, data, decrypt)
		return result

	def encrypt_file(self, password, filepath,
					decrypt=False, keep_org=False, naked=False):
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

		outpath = FileModder.add_tag(filepath,tag,oldtags,newtags)

		if exists(filepath) == False:
			result['status'] = 400
			result['message'] = 'Error failed to find file: ' + filepath
			return result

		if exists(outpath) == True:
			result['status'] = 400
			result['message'] = 'Error output path already exists: ' + outpath
			return result

		if outpath == filepath:
			result['status'] = 400
			result['message'] = 'Action already performed on: ' + filepath
			return result

		data = {'format': 'file', 'input': filepath, 'outpath': outpath}
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
			remove(filepath)
			result['status'] = 200
			result['message'] = response['message'] + ' (original deleted).'
		except:
			result['status'] = 400
			result['message'] = response['message'] + ' (Error deleting original).'

		return result

	def encrypt_all_files(self, password, wd, extension=None,
					decrypt=False, keep_org=False, naked=False):
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

	def __init__(self, scrambler, instance, encryptiongui, stashgui):
		self.scrambler = scrambler
		self.instance = instance
		self.encryptiongui = encryptiongui
		self.stashgui = stashgui

	def splashscreen(self):
		cmd.clear()
		print('Welcome to the Scrambler!')

	def optionscreen(self):
		print('version: ' + self.instance.version_text)
		print(' ')
		print('What would you like to do?')
		print('(s) Set Dir, (e) Encrypt, (d) Decrypt, (st) Stash, (t) Timetravel, (q) Quit')

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
		print('You may specify a file type to timetravel. Leave blank for default .txt files.')
		print('Use * to timetravel all files regardless of type (this can be dangerous).')
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

			if select not in ('pwd','ls','s','e','d','st','t','q'):
				#'(s) Set Dir, (e) Encrypt, (d) Decrypt, (st) Stash, (t) Timetravel, (q) Quit'
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

			if select == 'st':
				self.stashgui.run()

			if select == 't':
				self.option_t()
