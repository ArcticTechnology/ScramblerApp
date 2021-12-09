import os;
import shlex; import subprocess
from os.path import isfile, isdir

class CommonCmd:

	@classmethod
	def pwd(self):
		command = 'pwd'
		process = subprocess.run(command,
			stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		returncode = process.returncode
		if returncode == 0:
			return process.stdout.decode().rstrip('\n')
		else:
			return ('Error printing directory.' + '\n' +
					'Error Code: ' + process.stderr.decode())

	@classmethod
	def ls(self):
		files = [f for f in os.listdir('.') if isfile(f)]
		folders = [d for d in os.listdir('.') if isdir(d)]
		files.sort()
		folders.sort()
		return folders + files

	@classmethod
	def cls(self):
		os.system('cls' if os.name=='nt' else 'clear')

	@classmethod
	def cp_file(self,localfilepath,newfilepath):

		lfilelex = shlex.quote(localfilepath)
		nfilelex = shlex.quote(newfilepath)

		command = shlex.split('cp {l} {n}'.format(l=lfilelex,n=nfilelex))
		process = subprocess.run(command,
			stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		returncode = process.returncode
		if returncode == 0:
			return 'File created: ' + newfilepath
		else:
			return ('Error creating file for: ' + localfilepath + '\n' +
					'Error Code: ' + process.stderr.decode())
