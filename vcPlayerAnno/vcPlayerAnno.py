from com.l2jserver.gameserver.handler import VoicedCommandHandler
from com.l2jserver.gameserver.handler import IVoicedCommandHandler
from com.l2jserver.gameserver.datatables import ItemTable
from com.l2jserver.gameserver.network.serverpackets import InventoryUpdate
from com.l2jserver.gameserver import Announcements

class VCPlayerAnno(IVoicedCommandHandler):
	isCritical = True #�O�_�����n���i�Φ����
	requireItemId = 57 #�ݨD�D�� ID
	requireItemCount = 100 #�ݨD�D��ƶq
	messageLength = 50 #�T�����׭���

	commands = ["���i"]
	
	def useVoicedCommand(self, command, player, params):
		if not player: return
		inv = player.getInventory()
		if not inv: return
		ditem = inv.destroyItemByItemId("vcplayeranno", self.requireItemId, self.requireItemCount, player, None) 
		if ditem:
			player.sendMessage("���ӤF %s %d ��" % (ditem.getName(), self.requireItemCount))
			Announcements.getInstance().announceToAll("%s:%s" % (player.getName(), params[:self.messageLength]), self.isCritical)
			iu = InventoryUpdate()
			iu.addModifiedItem(ditem)
			player.sendPacket(iu)
		else:
			item = ItemTable.getInstance().getTemplate(self.requireItemId)
			name = ""
			if item:
				name = item.getName()
			player.sendMessage("�һݹD�㤣�� �ݭn %s %d ��" % (name, self.requireItemCount))
			
	def getVoicedCommandList(self):
		return self.commands
		
	def __init__(self):
		VoicedCommandHandler.getInstance().registerHandler(self)
		print "vcPlayerAnno registered"
		print "���a�i�� .���i"

VCPlayerAnno()
