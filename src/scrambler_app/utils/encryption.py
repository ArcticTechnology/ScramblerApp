import shlex; import subprocess

class OpenSSLEncyptor:

	@classmethod
	def encrypt(self, password, data, decrypt=False):
		"""
		Example data inputs:
		data = {'medium': 'file', 'input': '/filepath/example', 'outpath': '/example-c'}
		data = {'medium': 'text', 'input': 'hello world', 'outpath': None}
		"""
		medium_options = ('file', 'text')
		result = {'status': None, 'message': None, 'output': None}
		if type(data) != dict: del password; return {'status': 400,
								'message': 'Error: Input data incorrect format.'}
		if data['medium'] not in medium_options: del password; return {'status': 400,
								'message': 'Error: Invalid medium.'}

		passwd = shlex.quote(password)
		dashd = ' -d' if decrypt == True else ''
		keyword = 'Decrypt' if decrypt == True else 'Encrypt'
		keywording = 'decrypting' if decrypt == True else 'encrypting'

		if data['medium'] == 'text':
			inputtext = data['input']
			if "'" in inputtext or '"' in inputtext:
				del passwd; del password; return {'status': 405,
				'message': 'Error: Quote characters not allowed.'}
			text = shlex.quote(data['input'])
			pipetext = shlex.split('echo "{t}"'.format(t=text))
			command = shlex.split('openssl aes-256-cbc{d} -a -salt -pbkdf2 -k {p}'.format(
						d=dashd,p=passwd))

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
				del passwd; del password; return result
			except:
				result['status'] = 400
				result['message'] = 'Error: {}ion failed. Make sure your password is correct.'.format(keyword)
				del passwd; del password; return result

		if data['medium'] == 'file':
			try:
				filepath = shlex.quote(data['input'])
				outpath = shlex.quote(data['outpath'])
			except:
				del passwd; del password; return {'status': 200, 'message': 'Error: Invalid medium.'}

			c = 'openssl aes-256-cbc{d} -a -salt -pbkdf2 -in {f} -out {o} -k {p}'.format(
							d=dashd,f=filepath,o=outpath,p=passwd)
			command = shlex.split(c)
			process = subprocess.run(command,
							stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			#stdout = process.stdout.decode() #to see error code
			returncode = process.returncode

			if returncode == 0:
				result['status'] = 200
				result['message'] = '{}ed: '.format(keyword) + outpath
				del passwd; del password; return result
			else:
				result['status'] = 400
				result['message'] = 'Error {}: '.format(keywording) + filepath
				del passwd; del password; return result