import shlex; import subprocess
from os.path import exists

class OpenSSLEncyptor:

	@classmethod
	def get_version(self) -> dict:
		c = 'openssl version'
		command = shlex.split(c)
		process = subprocess.run(command,
			stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		returncode = process.returncode
		if returncode != 0:
			return {'status': 400, 'message': 'Error: Failed to load OpenSSL.', 'version': None}

		message = process.stdout.decode().rstrip('\n')
		version = message[:4].lower()
		if version == 'open' or version == 'libr':
			return {'status': 200, 'message': message[:27], 'version': version}
		else:
			return {'status': 400,
				'message': 'Error, incompatible verison of OpenSSL: {}'.format(message),
				'version': version}

	@classmethod
	def encrypt(self, password: str, data: dict, decrypt=False) -> dict:
		"""
		Example data inputs:
		data = {'format': 'file', 'input': '/filepath/example', 'outpath': '/example-c'}
		data = {'format': 'text', 'input': 'hello world', 'outpath': None}
		"""
		format_options = ('file', 'text')

		if type(data) != dict:
			return {'status': 400, 'message': 'Error: Input data incorrect format.',
					'output': None}

		if data['format'] not in format_options:
			return {'status': 400, 'message': 'Error: Format type incorrect.',
					'output': None}

		version = self.get_version()
		if version['status'] != 200:
			return {'status': 400, 'message': version['message'],
					'output': None}

		passwd = shlex.quote(password)
		_d = ' -d' if decrypt == True else ''
		_pbkdf2 = ' -pbkdf2' if version['version'] == 'open' else ''

		if data['format'] == 'file':
			inpath = data['input']
			outpath = data['outpath']
			return self._encrypt_file(inpath,outpath,_d,_pbkdf2,passwd,decrypt)

		if data['format'] == 'text':
			inputtext = data['input']
			return self._encrypt_msg(inputtext,_d,_pbkdf2,passwd,decrypt)

	@classmethod
	def _encrypt_file(self, inpath: str, outpath: str, _d: str, _pbkdf2: str, passwd: str, decrypt: bool) -> dict:
		result = {'status': None, 'message': None, 'output': None}
		if exists(inpath) == False:
			return {'status': 400, 'message': 'Error: Invalid input path.'}

		_inpath = ' -in {}'.format(inpath)
		_outpath = '' if outpath == None else ' -out {}'.format(outpath)
		c = 'openssl aes-256-cbc{d} -a -salt{p}{i}{o} -pass pass:{pa}'.format(
						d=_d,p=_pbkdf2,i=_inpath,o=_outpath,pa=passwd)
		command = shlex.split(c)
		process = subprocess.run(command,
						stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		returncode = process.returncode

		if returncode == 0 and outpath == None:
			raw_output = process.stdout.decode()
			if '\n' in raw_output:
				output = ' '.join(raw_output.split('\n'))
			else:
				output = raw_output
			result['status'] = 200
			result['message'] = '{}ion completed.'.format('Decrypt' if decrypt else 'Encrypt')
			result['output'] = output
			return result
		elif returncode == 0 and outpath != None:
			result['status'] = 200
			result['message'] = '{}ed: '.format('Decrypt' if decrypt else 'Encrypt') + outpath
			return result
		else:
			result['status'] = 400
			if decrypt == True:
				result['message'] = 'Error: Failed to decrypt message, make sure your password is correct.'
			else:
				result['message'] = 'Error: Encryption failed, could not encrypt message.'
			return result

	@classmethod
	def _encrypt_msg(self, inputtext: str, _d: str, _pbkdf2: str, passwd: str, decrypt: bool) -> dict:
		result = {'status': None, 'message': None, 'output': None}
		if "'" in inputtext or '"' in inputtext:
			result['status'] = 405; result['message'] = 'Error: Quote characters not allowed.'
			return result

		text = shlex.quote(inputtext)
		pipetext = shlex.split('echo "{t}"'.format(t=text))
		command = shlex.split('openssl aes-256-cbc{d} -a -salt{p} -pass pass:{pa}'.format(
					d=_d,p=_pbkdf2,pa=passwd))

		try:
			pipe = subprocess.Popen(pipetext, stdout=subprocess.PIPE)
			process = subprocess.check_output(command, stdin=pipe.stdout,
					stderr=subprocess.DEVNULL)
			pipe.wait()
			raw_output = process.decode()
			clean1 = raw_output[:-1] if raw_output[-1] == "\n" else raw_output
			clean2 = clean1[:-1] if clean1[-1] == "\r" else clean1
			clean3 = clean2[:-1] if clean2[-1] == "'" else clean2
			final_clean = clean3[1:] if clean3[0] == "'" else clean3

			result['status'] = 200
			result['message'] = '{}ion completed.'.format('Decrypt' if decrypt else 'Encrypt')
			result['output'] = final_clean
			return result

		except:
			result['status'] = 400
			if decrypt == True:
				result['message'] = 'Error: Failed to decrypt message, make sure your password is correct.'
			else:
				result['message'] = 'Error: Encryption failed, could not encrypt message.'
			return result