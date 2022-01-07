import os;
import shlex; import subprocess
from os.path import isfile, isdir
from ..dircrawler.crawler import Crawler

class CommonCmd:

	@classmethod
	def pwd(self):
		command = 'pwd'
		process = subprocess.run(command,
			stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		returncode = process.returncode
		result = Crawler.stdpath(process.stdout.decode().rstrip('\n'))
		if returncode == 0:
			return result
		else:
			return 'Error unable to print working directory.'

	@classmethod
	def ls(self):
		files = [f for f in os.listdir('.') if isfile(f)]
		folders = [d for d in os.listdir('.') if isdir(d)]
		files.sort()
		folders.sort()
		return folders + files

	@classmethod
	def clear(self):
		os.system('clear')

	@classmethod
	def copyfile(self,curr_filepath,new_filepath):

		cfilelex = shlex.quote(curr_filepath)
		nfilelex = shlex.quote(new_filepath)

		command = shlex.split('cp {c} {n}'.format(c=cfilelex,n=nfilelex))
		process = subprocess.run(command,
			stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		returncode = process.returncode
		if returncode == 0:
			return {'status': 200, 'message': 'File created: ' + new_filepath}
		else:
			return {'status': 400, 'message': 'Error creating file for: ' + curr_filepath}