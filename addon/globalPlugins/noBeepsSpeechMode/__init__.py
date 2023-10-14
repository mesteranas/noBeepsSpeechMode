# -*- coding: UTF-8 -*-
#Plugin to switch only between Talk or Off speech modes
#Author: Alberto Buffolino
import config
from gui import SettingsPanel, NVDASettingsDialog, guiHelper
import imp
from winsound import PlaySound
import addonHandler
import globalPluginHandler
import wx
import speech
from . import msg as NVDALocale
addonHandler.initTranslation()
confspec = {
"notification": "integer(default=0)"}
config.conf.spec["NoBeepsSpeechMode"] = confspec
try:
	from globalCommands import SCRCAT_SPEECH
except:
	SCRCAT_SPEECH = None
class settings(SettingsPanel):
	title = _("No beeps speech mode")
	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.tlable = sHelper.addItem(wx.StaticText(self, label=_("select notification when you toggle speech on  or off"), name="ts"))
		self.sou= sHelper.addItem(wx.Choice(self, name="ts"))
		self.sou.Set([_("speek"),_("nvda on or off sound")])
		self.sou.SetSelection(config.conf["NoBeepsSpeechMode"]["notification"])
	def onSave(self):
		config.conf["NoBeepsSpeechMode"]["notification"]=self.sou.GetSelection()
	def postInit(self):
		self.sou.SetFocus()
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	NVDASettingsDialog.categoryClasses.append(settings)
	scriptCategory = SCRCAT_SPEECH

	def script_noBeepsSpeechMode(self, gesture):
		curMode = speech.getState().speechMode
		if curMode == speech.SpeechMode.talk:
			if config.conf["NoBeepsSpeechMode"]["notification"]==0:
				NVDALocale.message("Speech mode off")
			else:
				PlaySound("waves/exit.wav",1)
			speech.setSpeechMode(speech.SpeechMode.off)
		elif curMode == speech.SpeechMode.off:
			speech.setSpeechMode(speech.SpeechMode.talk)
			# Translators: no translation required (see msg.py)
			if config.conf["NoBeepsSpeechMode"]["notification"]==0:
				NVDALocale.message("Speech mode talk")
			else:
				PlaySound("waves/start.wav",1)

	# Translators: Message presented in input help mode,
	# this string is partially present in .po localization file of NVDA for the various languages.
	script_noBeepsSpeechMode.__doc__ = _("Toggles between the speech modes of off and talk. When set to off NVDA will not speak anything. If talk then NVDA wil just speak normally.")

	__gestures = {
		"kb:NVDA+s": "noBeepsSpeechMode",
	}
	def terminate(self):
		NVDASettingsDialog.categoryClasses.remove(settings)

