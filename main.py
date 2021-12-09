#!/usr/bin/python3 -B
import sys
from scrambler_app import *

def main(args=None):
	if args is None: args = sys.argv[1:]
	handler()

if __name__ == '__main__':
	sys.exit(main())
