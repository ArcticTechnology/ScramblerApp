import os
import sys
import json

class ConfigParser:

	def __init__(self, scrambler):
		self.scrambler = scrambler
		self.build_loc = 'ScramblerApp/config'
		self.dev_loc = 'config'
		self.path_type = None
		self.rootpath = None
		self.filepath = None
		self.filename = None

	def _find(self, filename): #filename should be .config or .config-c
		build_rootpath = os.path.abspath(os.path.join(sys.prefix, self.build_loc))
		build_filepath = os.path.abspath(os.path.join(build_rootpath, filename))
		build_exists = os.path.exists(build_filepath)

		dev_rootpath = os.path.abspath(os.path.join(os.path.dirname(
			os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
			self.dev_loc))
		dev_filepath = os.path.abspath(os.path.join(dev_rootpath, filename))
		dev_exists = os.path.exists(dev_filepath)

		if build_exists == True:
			self.path_type = 'build'
			self.rootpath = build_rootpath
			self.filepath = build_filepath
		elif dev_exists == True:
			self.path_type = 'dev'
			self.rootpath = dev_rootpath
			self.filepath = dev_filepath
		else:
			self.path_type = None
			self.rootpath = None
			self.filepath = None

	def _find_config_file(self):
		possible_names = ['.config-c', '.config', '.config-d']

		for name in possible_names:
			self._find(name)
			if self.filepath != None:
				self.filename = name
				break

	def _hasContent(self):
		if self.filepath == None: return False
		if os.stat(self.filepath).st_size > 0:
			return True
		else:
			return False

	def _hasEncyptedTag(self):
		if self.filename == '.config-c':
			return True
		else:
			return False

	def get_config(self, password=None, needs_enc=False):
		result = {'status': None, 'message': None, 'output': None}
		self._find_config_file()

		if self._hasContent() != True:
			result['status'] = 400
			result['message'] = 'Error: config file not found or empty.'
			return result

		if self._hasEncyptedTag() == True and password==None:
			result['status'] = 400
			result['message'] = 'Error: config file requires password to read.'
			return result

		if self._hasEncyptedTag():
			# Try to Read and decrypt the message using openssl
			self.scrambler.encrypt_file(self.filepath,password,
					decrypt=True,keep_org=True,naked=False)

		# else: 
		### Try to Read
		### if needs_enc == True, encrypt the config file, delete the existing file.
			self.scrambler.encrypt_file(self.filepath,password,
					decrypt=False,keep_org=False,naked=False)


#	def get_config(self):
		#with open(path, 'r') as f:
		#	return json.load(f)
#		return self.file

