#!/usr/bin/python3 -B
from scramblerapp import *

def main():
	scrambler = Scrambler()
	instance = Instance()
	encryptiongui = EncryptionGUI(scrambler, instance)
	scramblergui = ScramblerGUI(scrambler, instance, encryptiongui)
	scramblergui.run()

if __name__ == '__main__':
	raise SystemExit(main())
