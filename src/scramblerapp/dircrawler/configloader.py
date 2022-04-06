import os; import json
from os.path import (
	basename, dirname, exists, normpath
)
from .crawler import Crawler
from .read import read_file
from ..utils.encryption import OpenSSLEncyptor as ossl

class ConfigLoader:

	def __init__(self):
		self.build_loc = 'pythonstarterpackage/config'
		self.dev_loc = 'config'
		self.possible_names = ['.config', '.config-d', '.config-NAKED', '.config-c']

		self.rootpath = ''
		self.env = ''
		self.configloc = ''
		self.configfile = ''
		self.load()

	def _get_rootpath(self) -> str:
		return dirname(dirname(__file__))

	def _get_env(self) -> str:
		if self.rootpath == '': return ''
		filename = basename(normpath(dirname(self.rootpath)))
		if filename == 'site-packages':
			return 'build'
		elif filename == 'src':
			return 'dev'
		else:
			return ''

	def _get_configloc(self) -> str:
		if self.env == 'build':
			return Crawler.joinpath(dirname(dirname(dirname(dirname(self.rootpath)))),
					self.build_loc)
		elif self.env == 'dev':
			return Crawler.joinpath(dirname(dirname(self.rootpath)),
					self.dev_loc)
		else:
			return ''

	def _get_configfile(self, filename: str) -> str:
		if self.configloc == '': return ''
		return Crawler.joinpath(self.configloc, filename)

	def _find(self) -> dict:
		self.rootpath = self._get_rootpath()
		self.env = self._get_env()
		self.configloc = self._get_configloc()

		for filename in self.possible_names:
			self.configfile = self._get_configfile(filename)
			if exists(self.configfile):
				return {'status': 200, 'message': 'Config file found.'}

		return {'status': 400, 'message': 'Warning: Config file not found.'}

	def hasContent(self) -> bool:
		if exists(self.configfile) == False: return False
		if os.stat(self.configfile).st_size > 0:
			return True
		else:
			return False

	def load(self) -> dict:
		find = self._find()
		if find['status'] == 400:
			return {'status': 400,
					'message': find['message']}
		if self.hasContent():
			return {'status': 200,
					'message': 'Config file successfully loaded.'}
		else:
			return {'status': 400,
					'message': 'Warning: Config file is empty.'}

	def parse(self) -> dict:
		try:
			content = ''.join(read_file(self.configfile))
		except:
			return {'status': 400,
						'message': 'Error: config file could not be read.', 'data': None}

		try:
			result = json.loads(content)
			return {'status': 200, 'message': 'Read config file complete.',
					'data': result}
		except:
			return {'status': 400,
				'message': 'Error: config file not structured correctly.',
				'data': None}

	def hasEncyptedTag(self) -> bool:
		filename = basename(normpath(self.configfile))
		if '.config-c' in filename:
			return True
		else:
			return False

	def enc_parse(self, password=None) -> dict:
		has_enctag = self.hasEncyptedTag()

		if has_enctag == True and password == None:
			return {'status': 400,
				'message': 'Error: config file requires password to read.', 'output': None}

		if has_enctag == True and password != None:
			data = {'format': 'file', 'input': self.configfile, 'outpath': None}
			response = ossl.encrypt(password, data, decrypt=True)

			if response['status'] != 200: return response

			try:
				result = json.loads(response['output'])
				return {'status': 200, 'message': 'Read config file complete.',
						'output': result}
			except:
				return {'status': 400,
					'message': 'Error: Failed to read config, file formatted incorrectly.',
					'output': None}

		if has_enctag == False:
			try:
				content = ''.join(read_file(self.configfile))
				result = json.loads(content)
				return {'status': 200, 'message': 'Read config file complete.',
						'output': result}
			except:
				return {'status': 400,
						'message': 'Error: Failed to read config, file formatted incorrectly.',
						'output': None}