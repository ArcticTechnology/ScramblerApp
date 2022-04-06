# Temporary read helper function
# This will be added to filemodder soon

def read_file(filepath: str) -> list:
	lines = []
	with open(filepath,'r') as f:
		for line in f:
			if line[0] != '#':
				lines.append(line.rstrip('\n'))
	return lines