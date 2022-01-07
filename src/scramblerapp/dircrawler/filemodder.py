import os
from .crawler import Crawler

class FileModder:

	@classmethod
	def format_ext(self, raw_extension, ifblank='.txt', ifstar=None):
		if raw_extension == '*':
			return ifstar
		if raw_extension == '':
			return ifblank
		if raw_extension[0] != '.':
			return '.' + raw_extension
		else:
			return raw_extension

	@classmethod
	def add_msg(self, filepath, msg):
		indent_msg = '\n' + msg
		if Crawler.read_last_line(filepath) != indent_msg:
			with open(filepath,'a') as f:
				f.write(indent_msg)
			return 'Added message: ' + filepath
		else:
			return 'No message to add: ' + filepath

	@classmethod
	def rm_msg(self, filepath, msg):
		indent_msg = '\n' + msg
		if Crawler.read_last_line(filepath) == indent_msg:
			with open(filepath,'rb+') as f:
				Crawler.get_last_line(f)
				f.truncate()
			with open(filepath,'rb+') as f:
				Crawler.get_last_line(f)
				f.truncate()
			return 'Removed message: ' + filepath
		else:
			return 'No message to remove: ' + filepath

	@classmethod
	def write_msg_all(self, wd, msg='secret-msg', extension=None, remove=True):
		filepaths = Crawler.get_files(wd, extension=extension)

		if len(filepaths) <= 0:
			return 'No files found.'

		for filepath in filepaths:

			print(self.add_msg(filepath, msg=msg))

			if remove == True:
				print(self.rm_msg(filepath, msg=msg))

		return 'Write message complete.'

	@classmethod
	def add_extension(self, wd, extension):
		if extension == None or '.' not in extension:
			return 'No extension found.'

		filepaths = Crawler.get_files(wd, extension=None)

		if len(filepaths) <= 0:
			return 'No files found.'

		for filepath in filepaths:
			if '.' not in filepath:
				os.rename(filepath, filepath+extension)
				print('Renamed: ' + str(filepath))

		return Crawler.get_files(wd, extension)

	@classmethod
	def add_tag(self, filepath, newtag, curr_tag_options=[], new_tag_options=[]):

		extension = Crawler.get_extension(filepath)
		prefix = Crawler.get_prefix(filepath)

		current_tag = '-' + prefix.split('-')[-1]

		if current_tag in new_tag_options:
			return filepath

		if current_tag in curr_tag_options:
			return prefix.split(current_tag)[0] + newtag + extension
		else:
			return prefix + newtag + extension
