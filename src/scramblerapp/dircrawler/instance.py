import os
from .crawler import Crawler

class Instance:

	def __init__(self):
		self.wd = None

	def clear_wd(self):
		self.wd = None
		return {'status': 200, 'message': 'Working directory cleared.'}

	def set_wd(self,raw_wd):
		if raw_wd == '': return {'status': 400,
					'message': 'Invalid input, no action taken.'}
		wd = Crawler.stdpath(raw_wd)
		if os.path.isdir(wd) == False:
			return {'status': 400, 'message': 'Invalid input, no action taken.'}
		self.wd = wd
		os.chdir(wd)
		return {'status': 200, 'message': 'Working directory set: {}'.format(wd)}

	def set_cwd_as_wd(self):
		curr_dir = os.getcwd()
		wd = Crawler.stdpath(curr_dir)
		if os.path.isdir(wd) == False:
			return {'status': 400, 'message': 'Invalid input, no action taken.'}
		self.wd = wd
		return {'status': 200, 'message': 'Working directory set: {}'.format(wd)}
