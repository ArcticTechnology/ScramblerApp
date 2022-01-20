# This allows execution on calling the name the directory: python3 -m <packagename>
# See: https://stackoverflow.com/questions/4042905/what-is-main-py
from scramblerapp.main import main

if __name__ == '__main__':
	raise SystemExit(main())