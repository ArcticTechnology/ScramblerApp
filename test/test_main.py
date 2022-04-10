#!/usr/bin/python3 -B
from scramblerapp import *

def main():
	scrambler = Scrambler()
	instance = Instance()
	configloader = ConfigLoader()
	encryptiongui = EncryptionGUI(scrambler, instance)
	stashgui = StashGUI(scrambler, instance, configloader)
	scramblergui = ScramblerGUI(scrambler, instance, encryptiongui, stashgui)
	scramblergui.run()

if __name__ == '__main__':
	raise SystemExit(main())
