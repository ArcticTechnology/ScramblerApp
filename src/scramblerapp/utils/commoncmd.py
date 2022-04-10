import shlex; import subprocess
from os import getcwd, listdir, system
from os.path import isfile, isdir
from ..dircrawler.crawler import Crawler

class CommonCmd:

	@classmethod
	def pwd(self, internal=False):
		if internal: return Crawler.stdpath(getcwd())

		command = 'pwd'
		process = subprocess.run(command,
			stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		returncode = process.returncode
		result = Crawler.stdpath(process.stdout.decode().rstrip('\n'))
		if returncode == 0:
			return result
		else:
			return 'Error: unable to print working directory.'

	@classmethod
	def ls(self) -> list:
		files = [f for f in listdir('.') if isfile(f)]
		folders = [d for d in listdir('.') if isdir(d)]
		files.sort()
		folders.sort()
		return folders + files

	@classmethod
	def clear(self):
		system('clear')

	@classmethod
	def copyfile(self, curr_filepath: str, new_filepath: str) -> dict:

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