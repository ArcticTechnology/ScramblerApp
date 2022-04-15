#!/usr/bin/python3 -B
from .scrambler import Scrambler, ScramblerGUI
from .gui.encryptiongui import EncryptionGUI
from .gui.stashgui import StashGUI
from .gui.instance import Instance
from .dircrawler.configloader import ConfigLoader

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