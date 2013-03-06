import sys
from com.l2jserver.gameserver.model.quest		import State
from com.l2jserver.gameserver.model.quest		import QuestState
from com.l2jserver.gameserver.model.quest.jython	import QuestJython as JQuest

from com.l2jserver.gameserver.handler import ChatHandler
from com.l2jserver import Config
from com.l2jserver.gameserver.handler import IChatHandler;
from com.l2jserver.gameserver.instancemanager import MapRegionManager;
from com.l2jserver.gameserver.model import BlockList;
from com.l2jserver.gameserver.model import L2World;
from com.l2jserver.gameserver.model.actor.instance import L2PcInstance;
from com.l2jserver.gameserver.network import SystemMessageId;
from com.l2jserver.gameserver.network.serverpackets import CreatureSay;
from com.l2jserver.gameserver.util import Util;

from com.l2jserver.gameserver import Announcements

class CQA(JQuest, IChatHandler):
	qID = -1
	qn = "cQA"
	qDesc = "custom"

	NPCID = 100
	isCritical = True #�O�_�����n���i�Φ����
	
	command_split_char = " _#_ "
	
	htm_header = "<html><body><title>�m������</title>"
	htm_footer = "</body></html>"

	gifts = {
		"����":57
		,"�j��":5575
		,"�y��":6673
		,"���m":6393
		,"�ť�":4355
		,"����":4356
		,"�Ȯu":4357
		,"�婬":4358
		,"�ڤ�":13067
	}
	
	item = qty = question = answer = None
	
	htm_input_reward = '���~<combobox width=140 var="item" list=' + reduce(lambda a, b: str(a) + ";" + str(b), gifts.keys()) + '>'
	htm_input_qty = '�ƶq<edit var="qty" width=140 height=12>'
	htm_input_question = '�D��<multiedit var="question" width=200 height=50>'
	htm_input_answer = '����<edit var="answer" width=140 height=12>'
	htm_input_submit = '<button value="�o�X���D" width=80 height=20 action="bypass -h Quest ' + qn + ' showQuestion $item%(s)s$qty%(s)s$question%(s)s$answer">' % {"s":command_split_char}
	
	htm_input_question = htm_input_reward + htm_input_qty + htm_input_question + htm_input_answer + htm_input_submit
	
	commands = [1]
	
	def handleChat(self, type, activeChar, target, text):
		if activeChar.isChatBanned() and Util.contains(Config.BAN_CHAT_CHANNELS, type):
			activeChar.sendPacket(SystemMessageId.CHATTING_IS_CURRENTLY_PROHIBITED)
			return
		cs = CreatureSay(activeChar.getObjectId(), type, activeChar.getName(), text)
		pls = L2World.getInstance().getAllPlayersArray()
		if Config.DEFAULT_GLOBAL_CHAT.lower() == "on" or (Config.DEFAULT_GLOBAL_CHAT.lower() == "gm" and activeChar.isGM()):
			region = MapRegionManager.getInstance().getMapRegionLocId(activeChar)
			for player in pls:
				if region == MapRegionManager.getInstance().getMapRegionLocId(player) and not BlockList.isBlocked(player, activeChar) and player.getInstanceId() == activeChar.getInstanceId():
					player.sendPacket(cs)
		elif Config.DEFAULT_GLOBAL_CHAT.lower() == "global":
			if not activeChar.isGM() and not activeChar.getFloodProtectors().getGlobalChat().tryPerformAction("global chat"):
				activeChar.sendMessage(1101)
				return
			for player in pls:
				if not BlockList.isBlocked(player, activeChar):
					player.sendPacket(cs)
		if not self.answer == None:
			if text == self.answer:
				self.answer = None
				Announcements.getInstance().announceToAll("���� %s ��o %s �ƶq %s ����:%s" % (activeChar.getName(), self.item, self.qty, text), self.isCritical)
				activeChar.addItem(self.qn, self.gifts[self.item], int(self.qty), None, True)
			
	def getChatTypeList(self):
		return self.commands
	
	def __init__(self, id = qID, name = qn, descr = qDesc):
		self.qID, self.qn, self.qDesc = id, name, descr
		JQuest.__init__(self, id, name, descr)
		self.addStartNpc(self.NPCID)
		self.addFirstTalkId(self.NPCID)
		self.addTalkId(self.NPCID)
		ChatHandler.getInstance().registerHandler(self)
		print "%s loaded" % self.qn
	
	def onAdvEvent(self, event, npc, player):
		if event.startswith("showQuestion "):
			params = event[len("showQuestion "):]
			self.item, self.qty, self.question, self.answer = params.split(self.command_split_char)
			Announcements.getInstance().announceToAll("�m������ �ШϥΤj���W�@�� �Ĥ@�쵪�����D�����a �N�|�o�� %s �ƶq %s" % (self.item, self.qty), self.isCritical)
			Announcements.getInstance().announceToAll("���D:%s" % (self.question), self.isCritical)
			return
		print self.qn, "�����n�D", npc, player, event
		return self.htm_header + "�����n�D" + self.htm_footer
			
	def onFirstTalk(self, npc, player):
		if not player.isGM():
			return self.htm_header + "GM �o���D�M��, �ФŰ��ݰ�" + self.htm_footer
		return self.htm_header + self.htm_input_question + self.htm_footer

CQA()