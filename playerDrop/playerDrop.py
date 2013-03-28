from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest
from com.l2jserver import Config
from com.l2jserver.gameserver.model.items.type import L2WeaponType
from com.l2jserver.gameserver.model.items.type import L2ArmorType
from com.l2jserver.gameserver.model.items.type import L2EtcItemType

class Quest(JQuest):
	qID = -1
	qn = "playerDrop"
	qDesc = "custom"
	
	#Ĳ�o NPC ID
	NPCID = 100
	
	#�զW�� �W�椺�����~ ID ���|����, ���|�C�X
	#�w�] ���� �j�N������ �y����� �Ŧ�쫽 �������� �Ȧ�u�Y ����⩬��߼� �ڤۮq�N�� ���� ����-���m������
	whiteList = [57, 5575, 6673, 4355, 4356, 4357, 4358, 13067, 3470, 6393]
	#�զW�� �[�J D �� R �ŵ���
	whiteList += [1458, 1459, 1460, 1461, 1462, 17371]
	
	#���\ �Z�� �C�X/����/�R��
	isAllowWeaponDrop = True
	#���\ ���� �C�X/����/�R��
	isAllowArmorDrop = True
	#���\ �j�ƨ� �C�X/����/�R��
	isAllowScrollEnchanceDrop = True
	#���\ �t�ޯ�D�� �C�X/����/�R��
	isAllowHasSkillItemDrop = True
	
	
	#�˴����~�i�_�����ݩ�
	checkDropable = True #False
	
	#�@���C�X�h�֪��~
	itemsPerPage = 10
	
	html_header = "<html><body><title>�M�ŭI�]���~</title>"
	html_footer = "</body></html>"
	html_after_drop = "�A�� 15�� �u���v �ߦ^���~<br1>"
	html_disappear = "�a�W�����~�N�� %d ������(�������~���~)<br1>" % (Config.AUTODESTROY_ITEM_AFTER,)
	html_drop_all = """<a action="bypass -h Quest %(qn)s drop">�I�������I�]���Ҧ����~</a><br1>""" % {"qn":qn}
	html_drop_quest = """<a action="bypass -h Quest %(qn)s delQuestItems">�I���R���Ҧ����ȹD��</a><br1>""" % {"qn":qn}
	html_foreach_item = """<tr><td><a action="bypass -h Quest %(qn)s dropone %(itemid)d">����</a></td><td><a action="bypass -h Quest %(qn)s delone %(itemid)d">�R��</a></td><td>%(itemname)s</td></tr><br1>"""
	html_prev_page = """<a action="bypass -h Quest %s list %d">�W�@��</a>"""
	html_next_page = """<a action="bypass -h Quest %s list %d">�U�@��</a>"""
	html_drop_one_intro = "�H�U�s�� �I������<br1>"
	
	def __init__(self, id = qID, name = qn, descr = qDesc):
		self.qID, self.qn, self.qDesc = id, name, descr
		JQuest.__init__(self, id, name, descr)
		self.addStartNpc(self.NPCID)
		self.addFirstTalkId(self.NPCID)
		self.addTalkId(self.NPCID)
		print "Init:" + self.qn + " loaded"

	def onFirstTalk(self, npc, player):
		return self.html_header + self.html_drop_all + self.html_drop_quest + self.list(player) + self.html_footer

	def onAdvEvent(self, event, npc, player):
		if event == "delQuestItems":
			return self.delQuestItems(npc, player)
		if event == "drop":
			return self.drop(player)
		if event.startswith("dropone "):
			return self.dropone(npc, player, int(event[8:]))
		if event.startswith("delone "):
			return self.delone(npc, player, int(event[7:]))
		if event.startswith("list "):
			try:
				page = int(event[len("list "):])
			except:
				return
			return self.html_header + self.html_drop_all + self.html_drop_quest + self.list(player, page) + self.html_footer

	def dropone(self, npc, player, oid):
		item = player.getInventory().getItemByObjectId(oid)
		player.dropItem(self.qn, item, None, False, True)
		return self.onFirstTalk(npc, player)

	def delone(self, npc, player, oid):
		item = player.getInventory().getItemByObjectId(oid)
		player.destroyItem(self.qn, item, None, True)
		return self.onFirstTalk(npc, player)
		
	def check(self, item):
		if item.getItemId() in self.whiteList: return False
		if item.isEquipped(): return False
		if self.checkDropable and not item.isDropable(): return False
		if not self.isAllowWeaponDrop and item.isWeapon(): return False
		if not self.isAllowArmorDrop and item.isArmor(): return False
		if not self.isAllowScrollEnchanceDrop and item.getItemType() in [L2EtcItemType.SCRL_ENCHANT_WP, L2EtcItemType.SCRL_ENCHANT_AM, L2EtcItemType.BLESS_SCRL_ENCHANT_WP, L2EtcItemType.BLESS_SCRL_ENCHANT_AM, L2EtcItemType.SCRL_INC_ENCHANT_PROP_WP, L2EtcItemType.SCRL_INC_ENCHANT_PROP_AM, L2EtcItemType.ANCIENT_CRYSTAL_ENCHANT_WP, L2EtcItemType.ANCIENT_CRYSTAL_ENCHANT_AM]: return False
		if not self.isAllowHasSkillItemDrop and item.getItem().hasSkills(): return False
		return True
		
	def drop(self, player):
		r = ""
		for item in [x for x in player.getInventory().getItems() if self.check(x)]:
			player.dropItem(self.qn, item, None, False, True)
		if Config.DESTROY_DROPPED_PLAYER_ITEM and Config.AUTODESTROY_ITEM_AFTER > 0:
			r = r + self.html_disappear
		r = r + self.html_after_drop
		return self.html_header + r + self.html_footer
		
	def delQuestItems(self, npc, player):
		for item in [x for x in player.getInventory().getItems() if x.isQuestItem()]:
			player.destroyItem(self.qn, item, None, True)
		return self.onFirstTalk(npc, player)
		
		
	def list(self, player, page=1):
		r = self.html_drop_one_intro
		if page > 1:
			r += self.html_prev_page % (self.qn, page - 1)
		r += " �� %d �� " % page
		r += self.html_next_page % (self.qn, page + 1)
		r = r + "<table>"
		index = 0
		startItemIndex = (page-1) * self.itemsPerPage
		for item in [x for x in player.getInventory().getItems() if self.check(x)]:
			if startItemIndex <= index < startItemIndex + self.itemsPerPage:
				r = r + self.html_foreach_item % {"qn":self.qn, "itemname":item.getName(), "itemid":item.getObjectId()}
			index = index + 1
		r = r + "</table>"
		return r
Quest()
