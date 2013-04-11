from com.l2jserver.gameserver.handler import VoicedCommandHandler
from com.l2jserver.gameserver.handler import IVoicedCommandHandler

from com.l2jserver.gameserver import Announcements

class VCPlayerAnno(IVoicedCommandHandler):
	isCritical = True #�O�_�����n���i�Φ����

	commands = ["���i"]
	
	def useVoicedCommand(self, command, player, params):
		Announcements.getInstance().announceToAll("%s:%s" % (player.getName(), params), self.isCritical)
			
	def getVoicedCommandList(self):
		return self.commands
		
	def __init__(self):
		VoicedCommandHandler.getInstance().registerHandler(self)
		print "vcPlayerAnno registered"
		print "���a�i�� .���i"

VCPlayerAnno()
