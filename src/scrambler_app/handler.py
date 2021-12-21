from .scrambler import Scrambler, ScramblerGUI
from .gui.encryptiongui import EncryptionGUI
from .gui.stashgui import StashGUI
from .utils.instance import Instance
from .utils.configparser import ConfigParser

def handler():
	scrambler = Scrambler()
	instance = Instance()
	configparser = ConfigParser()
	encryptiongui = EncryptionGUI(scrambler, instance)
	stashgui = StashGUI(scrambler, instance, configparser)
	scramblergui = ScramblerGUI(scrambler, instance, encryptiongui, stashgui)
	scramblergui.run()