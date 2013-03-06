from com.l2jserver.gameserver.handler import VoicedCommandHandler
from com.l2jserver.gameserver.handler import IVoicedCommandHandler

from java.util import Random
from com.l2jserver.gameserver.datatables import NpcTable
from com.l2jserver.gameserver.datatables import SpawnTable
from com.l2jserver.gameserver.model import L2Spawn
from com.l2jserver import Config
from com.l2jserver.gameserver.network.serverpackets import NpcHtmlMessage


class VCSpawn(IVoicedCommandHandler):

	commands = ["spawn"]

	html_spawn_input = '<html><body>�Ǫ� ID(�Ʀr)<edit var="npcid" width=140 height=12><br>�̤j�H���ƶq<edit var="qty" width=140 height=12><br>�d��<edit var="range" width=140 height=12><br>�ä[��<combobox width=140 var="once" list=�ä[;�@��><a action="bypass -h voice .%s $npcid $qty $range $once">�ͩ�</a></body></html>' % (commands[0],)
	
	def useVoicedCommand(self, command, player, params):
		if not player.isGM(): return
		mobid = 0
		max_mob = Random().nextInt(3) + 1
		dist = 400
		perm = False

		try:
			if params:
				param = params.split()
				mobid = int(param[0])
				max_mob = int(param[1])
				dist = int(param[2])
				perm = param[3].lower() == "true" or param[3] == "1" or param[3] == "�ä["
		except:
			pass
		
		def my_spawn(player, mobid, dist, perm):
			mobt = NpcTable.getInstance().getTemplate(mobid)
			if not mobt: return
			spawn = L2Spawn(mobt)
			spawn.setInstanceId(0)
			if Config.SAVE_GMSPAWN_ON_CUSTOM:
				spawn.setCustom(True)
			spawn.setLocx(player.getX()-dist+Random().nextInt(dist*2))
			spawn.setLocy(player.getY()-dist+Random().nextInt(dist*2))
			spawn.setLocz(player.getZ())
			spawn.setHeading(player.getHeading())
			spawn.setAmount(1);
			spawn.setRespawnDelay(0)
			if perm:
				SpawnTable.getInstance().addNewSpawn(spawn, True)
				spawn.init()
			else:
				spawn.stopRespawn()
				spawn.doSpawn()
		if mobid:
			for mob in xrange(max_mob):
				my_spawn(player, mobid, dist, perm)
		
		player.sendPacket(NpcHtmlMessage(player.getObjectId(), self.html_spawn_input))
			
	def getVoicedCommandList(self):
		return self.commands
		
	def __init__(self):
		VoicedCommandHandler.getInstance().registerHandler(self)
		print ".%s �i��" % " .".join(self.commands)
	
VCSpawn()