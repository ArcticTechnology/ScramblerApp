import os
import sys
import json

class Configurations:

	@classmethod
	def get_config(self):
		build_path = os.path.abspath(os.path.join(
			sys.prefix, 'ScramblerApp/config', 'config.json'))
		dev_path = os.path.abspath(os.path.join(os.path.dirname(
			os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
			'config', 'config.json'))

		if os.path.exists(build_path):
			path = build_path
		else:
			path = dev_path

		with open(path, 'r') as f:
			return json.load(f)