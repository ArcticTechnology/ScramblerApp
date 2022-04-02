import shlex; import subprocess

class OpenSSLEncyptor:

	@classmethod
	def get_version(self):
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
	def encrypt(self, password: str, data: dict, decrypt=False, pbkdf2=True):
		"""
		Example data inputs:
		data = {'medium': 'file', 'input': '/filepath/example', 'outpath': '/example-c'}
		data = {'medium': 'text', 'input': 'hello world', 'outpath': None}
		"""
		medium_options = ('file', 'text')
		result = {'status': None, 'message': None, 'output': None}
		if type(data) != dict: return {'status': 400,
								'message': 'Error: Input data incorrect format.'}
		if data['medium'] not in medium_options: return {'status': 400,
								'message': 'Error: Invalid medium.'}

		passwd = shlex.quote(password)
		_d = ' -d' if decrypt == True else ''
		_pbkdf2 = ' -pbkdf2' if pbkdf2 == True else ''
		keyword = 'Decrypt' if decrypt == True else 'Encrypt'

		if data['medium'] == 'text':
			inputtext = data['input']
			if "'" in inputtext or '"' in inputtext:
				return {'status': 405, 'message': 'Error: Quote characters not allowed.'}
			text = shlex.quote(data['input'])
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
				result['message'] = '{} completed.'.format(keyword)
				result['output'] = final_clean
				return result

			except:
				result['status'] = 400
				if decrypt == True:
					result['message'] = 'Error: Decryption failed. Make sure your password is correct.'.format(keyword)
				else:
					result['message'] = 'Error: Encryption failed, could not encrypt message.'.format(keyword)
				return result

		if data['medium'] == 'file':
			try:
				filepath = shlex.quote(data['input'])
				outpath = shlex.quote(data['outpath'])
			except:
				return {'status': 200, 'message': 'Error: Invalid medium.'}

			c = 'openssl aes-256-cbc{d} -a -salt{p} -in {f} -out {o} -pass pass:{pa}'.format(
							d=_d,p=_pbkdf2,f=filepath,o=outpath,pa=passwd)
			command = shlex.split(c)
			process = subprocess.run(command,
							stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			#stdout = process.stdout.decode() #to see error code
			returncode = process.returncode

			if returncode == 0:
				result['status'] = 200
				result['message'] = '{}ed: '.format(keyword) + outpath
				return result
			else:
				result['status'] = 400
				if decrypt == True:
					result['message'] = 'Error: Decryption failed. Make sure your password is correct.'.format(keyword)
				else:
					result['message'] = 'Error: Encryption failed, could not encrypt file.'.format(keyword)
				return result