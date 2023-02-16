#!/usr/bin/python3 -B
from .scrambler import Scrambler, ScramblerGUI
from .gui.encryptiongui import EncryptionGUI
from .gui.instance import Instance

def main():
	scrambler = Scrambler()
	instance = Instance()
	encryptiongui = EncryptionGUI(scrambler, instance)
	scramblergui = ScramblerGUI(scrambler, instance, encryptiongui)
	scramblergui.run()

if __name__ == '__main__':
	raise SystemExit(main())