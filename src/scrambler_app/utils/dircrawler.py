import os;
from os.path import isfile, isdir, join

class DirCrawler:

	@classmethod
	def _get_pathnm(self,path):
		return path.split('/')[-1]

	@classmethod
	def _get_prefix(self,filepath):
		return os.path.splitext(filepath)[0]

	@classmethod
	def _get_extension(self,filepath):
		return os.path.splitext(filepath)[-1]

	@classmethod
	def get_folders(self,wd,fix=True):

		dpaths = []

		for root, dirname, _ in os.walk(wd):
			for d in dirname:
				dpath = join(root,d)
				if isdir(dpath):
					if ' ' in d and fix == True:
						npath = os.rename(dpath,join(root,d.replace(' ','_')))
						dpaths.append(npath)
					else:
						dpaths.append(dpath)

		return dpaths

	@classmethod
	def get_files(self,wd,extension=None,fix=True):

		filepaths = []

		for root, _ , files in os.walk(wd):
			for f in files:
				filepath = join(root,f)
				if isfile(filepath):
					if ' ' in f and fix == True:
						npath = os.rename(filepath,join(root,f.replace(' ','_')))
						filepaths.append(npath)
					else:
						filepaths.append(filepath)

		if extension == None or len(filepaths) == 0:
			return filepaths

		result = []

		for filepath in filepaths:
			if self._get_extension(filepath) == extension:
				result.append(filepath)

		return result

	@classmethod
	def _get_last_line(self, openedFile):
		try:
			openedFile.seek(-2, os.SEEK_END)
			while openedFile.read(1) != b'\n':
				openedFile.seek(-2, os.SEEK_CUR)
		except:
			pass

	@classmethod
	def read_last_line(self,filepath):
		with open(filepath,'rb') as f:
			self._get_last_line(f)
			last_line = '\n' + f.readline().decode(errors='replace')
			return last_line

	@classmethod
	def read_line(self,filepath,linenum):
		with open(filepath,'r') as f:
			for n, line in enumerate(f):
				if n == linenum:
					return line.rstrip('\n')
		return None

	@classmethod
	def read_file(self,filepath):
		lines = []
		with open(filepath,'r') as f:
			for line in f:
				if line[0] != '#':
					lines.append(line.rstrip('\n'))
		return lines
