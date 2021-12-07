#!/usr/bin/python3 -B
import sys
from scrambler import *

def main(args=None):
	if args is None:
		args = sys.argv[1:]

	scrambler = Scrambler()
	scrambler.run()

if __name__ == '__main__':
	sys.exit(main())
