import os; import sys; import json
from .dircrawler import DirCrawler as dc
from .encryption import OpenSSLEncyptor as ossl

class ConfigParser:

	def __init__(self):
		self.build_loc = 'ScramblerApp/config'
		self.dev_loc = 'config'
		self.path_type = None
		self.rootpath = None
		self.filepath = None
		self.filename = None
		self.load_config()

	def _find(self, filename):
		build_rootpath = dc.joinpath(sys.prefix, self.build_loc)
		build_filepath = dc.joinpath(build_rootpath, filename)
		build_exists = os.path.exists(build_filepath)

		dev_rootpath = dc.joinpath(os.path.dirname(
			os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
			self.dev_loc)
		dev_filepath = dc.joinpath(dev_rootpath, filename)
		dev_exists = os.path.exists(dev_filepath)

		if build_exists == True:
			self.path_type = 'build'
			self.rootpath = build_rootpath
			self.filepath = build_filepath
			self.filename = filename
		elif dev_exists == True:
			self.path_type = 'dev'
			self.rootpath = dev_rootpath
			self.filepath = dev_filepath
			self.filename = filename
		else:
			self.path_type = 'build'
			self.rootpath = build_rootpath
			self.filepath = None
			self.filename = None

	def _find_config_file(self):
		possible_names = ['.config-c', '.config', '.config-d', '.config-NAKED']
		for name in possible_names:
			self._find(name)
			if self.filepath != None:
				return {'status': 200, 'message': 'Find config complete.'}
		return {'status': 400, 'message': 'Error: no config found.'}

	def hasContent(self):
		if self.filepath == None: return False
		if os.stat(self.filepath).st_size > 0:
			return True
		else:
			return False

	def hasEncyptedTag(self):
		if self.filename == '.config-c':
			return True
		else:
			return False

	def load_config(self):
		self._find_config_file()
		has_content = self.hasContent()
		if has_content == True: 
			return {'status': 200,
					'message': 'Load config file complete.'}
		else:
			return {'status': 400,
					'message': 'Error: config file not found or empty.'}

	def parse(self, password=None):
		has_enctag = self.hasEncyptedTag()

		try:
			file_content = ''.join(dc.read_file(self.filepath))
		except:
			return {'status': 400,
						'message': 'Error: config file could not be read.', 'output': None}

		if has_enctag == True and password == None:
			return {'status': 400,
				'message': 'Error: config file requires password to read.', 'output': None}

		if has_enctag == True and password != None:
			data = {'medium': 'text', 'input': file_content, 'outpath': None}
			response = ossl.encrypt(password, data, decrypt=True)

			if response['status'] != 200: return response

			try:
				result = json.loads(response['output'])
				return {'status': 200, 'message': 'Read config file complete.',
						'output': result}
			except:
				return {'status': 400,
					'message': response['message'],
					'output': None}

		if has_enctag == False:
			try:
				result = json.loads(file_content)
				return {'status': 200, 'message': 'Read config file complete.',
						'output': result}
			except:
				return {'status': 400,
					'message': 'Error: config file not structured correctly.',
					'output': None}