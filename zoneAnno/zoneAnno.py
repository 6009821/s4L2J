import sys
from com.l2jserver.gameserver.model.quest		import State
from com.l2jserver.gameserver.model.quest		import QuestState
from com.l2jserver.gameserver.model.quest.jython	import QuestJython as JQuest

import time

from com.l2jserver.gameserver import Announcements
from com.l2jserver.gameserver.instancemanager import ZoneManager
from com.l2jserver.gameserver.model.zone.type import L2BossZone
from com.l2jserver.gameserver.model.actor.instance import L2PcInstance

class ZoneAnno(JQuest):
	qID = -1
	qn = "ZoneAnno"
	qDesc = "custom"
	
	blacklist = [] #�¦W��, �W�椧�������i �Ҧp ["GM","GM2"]
	
	no_data_show = True #zone_data �S���w�q����� �O�_���
	
	zone_data = {
		12000:{"name":"����","show":False}
		,12001:{"name":"�a�s","show":True}
		,12002:{"name":"�ڷ�","show":True}
		,12004:{"name":"���K�j�Y�e�q","show":False}
		,12005:{"name":"���K�j�Y��q","show":False}
		,12010:{"name":"���s","show":True}
		,12012:{"name":"�ƦZ","show":False}
		,12013:{"name":"������","show":False}
		,12015:{"name":"������","show":False}
		,12018:{"name":"�ڦC��","show":True}
	}
	
	def __init__(self, id = qID, name = qn, descr = qDesc):
		JQuest.__init__(self, id, name, descr)
		for zone in ZoneManager.getInstance().getAllZones(L2BossZone):
			self.addEnterZoneId(zone.getId())
		print "Init:" + self.qn + " loaded"

	def onEnterZone(self, player, zonetype):
		if isinstance(player, L2PcInstance) and not player.getName() in self.blacklist:
			area_name = zonetype.getName()
			if zonetype.getId() in self.zone_data.keys():
				if not self.zone_data[zonetype.getId()]["show"]:
					return JQuest.onEnterZone(self, player, zonetype)
				area_name = self.zone_data[zonetype.getId()]["name"]
			else:
				if not self.no_data_show:
					return JQuest.onEnterZone(self, player, zonetype)
			t = time.localtime()
			h = t[3]
			m = t[4]
			a = "%s �i�J%s�d��! ��%d��%d��" % (player.getName(), area_name, h, m)
			Announcements.getInstance().announceToAll(a)
		return JQuest.onEnterZone(self, player, zonetype)
		
ZoneAnno()
