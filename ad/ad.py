from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest
from com.l2jserver import Config as C
from java.net import URL
from java.io import DataOutputStream
from java.net import URLEncoder
from com.l2jserver.gameserver.model import L2World

class Quest(JQuest):
	"""
	�o�}�� �|�۰ʧ�p�A �n����p�A�C��
	�Φ۰ʧ�s�p�A���򥻳]�w,��T��p�A�C��
	�����a�d��
	�p�G�p�A���� ��s�K�|����
	�p�A�C���p�A�Ƨ� �� �̪��s�� �Ƴ̫e
	�p�G�p�A���� �K�|�C�C�Q����U��. 
	���}���A �}���۰ʧ�s�� ���A�S����̤W��
	�ҥH �`�O�i�H�ݨ� ��������p�A
	"""
	qID = -1
	qn = "ad"
	qDesc = "custom"

	updateInterval = 1000 * 60 * 5 #�h�[��s�@�� (�O���W�K) �w�] 5����
	link = "http://www.l2jtw.com" #�s�� �ۦ�ק� ����A������ �� �׾�
	intro = """
	�p�A²��...�ۦ�ק�
	""" #�p�A²�� �ۦ�ק�

	param = u"""RATE_XP=%0.2f&RATE_SP=%0.2f&RATE_PARTY_XP=%0.2f&RATE_PARTY_SP=%0.2f&PARTY_XP_CUTOFF_LEVEL=%d&PET_XP_RATE=%0.2f&RATE_DROP_ITEMS=%0.2f&RATE_DROP_ITEMS_BY_RAID=%0.2f&RATE_DROP_MANOR=%d&RATE_QUEST_DROP=%0.2f&ADENA_RATE=%0.2f&BUFFS_MAX_AMOUNT=%d&TRIGGERED_BUFFS_MAX_AMOUNT=%d&DANCES_MAX_AMOUNT=%d&RUN_SPD_BOOST=%d&MAX_RUN_SPEED=%d&MAX_PCRIT_RATE=%d&MAX_MCRIT_RATE=%d&MAX_PATK_SPEED=%d&MAX_MATK_SPEED=%d&MAX_EVASION=%d&MAX_SUBCLASS=%d&BASE_SUBCLASS_LEVEL=%d&MAX_SUBCLASS_LEVEL=%d&INVENTORY_MAXIMUM_NO_DWARF=%d&INVENTORY_MAXIMUM_DWARF=%d&INVENTORY_MAXIMUM_QUEST_ITEMS=%d&WAREHOUSE_SLOTS_NO_DWARF=%d&WAREHOUSE_SLOTS_DWARF=%d&WAREHOUSE_SLOTS_CLAN=%d&MAX_ADENA=%d&MAXIMUM_ONLINE_USERS=%d&ENCHANT_CHANCE_ELEMENT_STONE=%0.2f&ENCHANT_CHANCE_ELEMENT_CRYSTAL=%0.2f&ENCHANT_CHANCE_ELEMENT_JEWEL=%0.2f&ENCHANT_CHANCE_ELEMENT_ENERGY=%0.2f&ENCHANT_SAFE_MAX=%d&ENCHANT_SAFE_MAX_FULL=%d&CLAN_LEVEL_6_COST=%d&CLAN_LEVEL_7_COST=%d&CLAN_LEVEL_8_COST=%d&CLAN_LEVEL_9_COST=%d&CLAN_LEVEL_10_COST=%d&CLAN_LEVEL_11_COST=%d&CLAN_LEVEL_6_REQUIREMENT=%d&CLAN_LEVEL_7_REQUIREMENT=%d&CLAN_LEVEL_8_REQUIREMENT=%d&CLAN_LEVEL_9_REQUIREMENT=%d&CLAN_LEVEL_10_REQUIREMENT=%d&CLAN_LEVEL_11_REQUIREMENT=%d&ONLINE=%d&REALONLINE=%d&LINK=%s&INTRO=%s"""
	def __init__(self, id = qID, name = qn, descr = qDesc):
		self.qID, self.qn, self.qDesc = id, name, descr
		JQuest.__init__(self, id, name, descr)
		self.onAdvEvent("ad", None, None)
		self.startQuestTimer("ad", self.updateInterval, None, None, True)
		print '%s loaded' % self.qn

	def onAdvEvent(self, event, npc, player):
		if event == 'ad':
			try:
				c = URL('http://duck5duck.mooo.com/l2jtw_ad/l2jtw_ad.php').openConnection()
				if c:
					c.setDoOutput(True)
					o = DataOutputStream(c.getOutputStream())
					s = self.param % (
						C.RATE_XP
						, C.RATE_SP
						, C.RATE_PARTY_XP
						, C.RATE_PARTY_SP
						, C.PARTY_XP_CUTOFF_LEVEL
						, C.PET_XP_RATE
						, C.RATE_DROP_ITEMS
						, C.RATE_DROP_ITEMS_BY_RAID
						, C.RATE_DROP_MANOR
						, C.RATE_QUEST_DROP
						, C.RATE_DROP_ITEMS_ID.get(57) or 1.0
						, C.BUFFS_MAX_AMOUNT
						, C.TRIGGERED_BUFFS_MAX_AMOUNT
						, C.DANCES_MAX_AMOUNT
						, C.RUN_SPD_BOOST
						, C.MAX_RUN_SPEED
						, C.MAX_PCRIT_RATE
						, C.MAX_MCRIT_RATE
						, C.MAX_PATK_SPEED
						, C.MAX_MATK_SPEED
						, C.MAX_EVASION
						, C.MAX_SUBCLASS
						, C.BASE_SUBCLASS_LEVEL
						, C.MAX_SUBCLASS_LEVEL
						, C.INVENTORY_MAXIMUM_NO_DWARF
						, C.INVENTORY_MAXIMUM_DWARF
						, C.INVENTORY_MAXIMUM_QUEST_ITEMS
						, C.WAREHOUSE_SLOTS_NO_DWARF
						, C.WAREHOUSE_SLOTS_DWARF
						, C.WAREHOUSE_SLOTS_CLAN
						, C.MAX_ADENA/100000000
						, C.MAXIMUM_ONLINE_USERS
						, C.ENCHANT_CHANCE_ELEMENT_STONE
						, C.ENCHANT_CHANCE_ELEMENT_CRYSTAL
						, C.ENCHANT_CHANCE_ELEMENT_JEWEL
						, C.ENCHANT_CHANCE_ELEMENT_ENERGY
						, C.ENCHANT_SAFE_MAX
						, C.ENCHANT_SAFE_MAX_FULL
						, C.CLAN_LEVEL_6_COST
						, C.CLAN_LEVEL_7_COST
						, C.CLAN_LEVEL_8_COST
						, C.CLAN_LEVEL_9_COST
						, C.CLAN_LEVEL_10_COST
						, C.CLAN_LEVEL_11_COST
						, C.CLAN_LEVEL_6_REQUIREMENT
						, C.CLAN_LEVEL_7_REQUIREMENT
						, C.CLAN_LEVEL_8_REQUIREMENT
						, C.CLAN_LEVEL_9_REQUIREMENT
						, C.CLAN_LEVEL_10_REQUIREMENT
						, C.CLAN_LEVEL_11_REQUIREMENT
						, L2World.getInstance().getAllPlayersCount()
						, self.getRealOnline()
						, URLEncoder.encode(self.link, 'utf-8')
						, URLEncoder.encode(self.intro, 'utf-8')
					)
					o.write(s)
					o.flush()
					o.close()
					i = c.getInputStream()
					r = ""
					while True:
						ch = i.read()
						if ch == -1:
							break
						r += chr(ch)
					if len(r):
						print r
					i.close()
					c.disconnect()
			except:
				return

	def getRealOnline(self):
		i = 0
		for p in L2World.getInstance().getAllPlayersArray():
			if p and p.isOnlineInt() == 1:
				i += 1
		return i
Quest()
