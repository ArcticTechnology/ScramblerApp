import os

class CommonCmd:

	@classmethod
	def cls(self):
		os.system('cls' if os.name=='nt' else 'clear')

