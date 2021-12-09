import os

class Instance:

	def __init__(self):
		self.wd = None
		self.extension = None

	def clear_wd(self):
		self.wd = None
		return 'wd cleared.'

	def set_wd(self,wd):
		self.wd = wd
		os.chdir(wd)
		return self.wd

	def set_cwd_as_wd(self):
		self.wd = os.getcwd()
		return self.wd

	def set_extension(self, extension):
		self.extension = extension
		return self.extension
