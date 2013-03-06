import sys
from com.l2jserver.gameserver.model.quest		import State
from com.l2jserver.gameserver.model.quest		import QuestState
from com.l2jserver.gameserver.model.quest.jython	import QuestJython as JQuest

from com.l2jserver.gameserver.handler import VoicedCommandHandler
from com.l2jserver.gameserver.handler import IVoicedCommandHandler

from com.l2jserver.gameserver.model import L2World
from com.l2jserver.gameserver.model.actor import L2Character
from com.l2jserver.gameserver.model.actor.instance import L2PcInstance
from com.l2jserver.gameserver.network.serverpackets import ExShowScreenMessage
from com.l2jserver.gameserver.ai import CtrlIntention
from com.l2jserver.gameserver.instancemanager import TownManager
from java.util.logging import Logger
from com.l2jserver.gameserver.network.serverpackets import NpcHtmlMessage
import time

class VCAntiBot(JQuest, IVoicedCommandHandler):
	qID = -1
	qn = "AntiBot"
	qDesc = "custom"

	isShowHtml = True #�O�_��ܹ�ܮ�
	
	interval = 1000 * 60 * 5 #5���� �H����d�@�Ӫ��a
	interval_random_delay_sec = 180 #�H����d���� �w�] 0 - 180 ��

	timepass_check = True #�O�_�O�����˴��ӧO���a�ϥ~���ˬd��, �ݭn�h�[�~�|�A�����|�Q�d
	timepass = 60 * 20 #�ӧO���a�˴��᪺�K���ɶ�, ��� ��, �w�] 20����

	question_duration = 1000 * 60 * 5 #���D��ܦh�[ 1��=1000 �w�] 5����
	jail_duration = 0 #���h�[��۰�����, ��� ����,  0 = ���۰�����, �n GM �������
	
	max_retry = 5 #�i�����h�֦� �~�Q��
	
	title = "�ϥ~���˴��t��"
	desc = "�ХH�@���r�W�D��J .ab �Ů� �M�ᵪ��"
	#�i�ۭq�h���D�� ["���D", "����"],["���D", "����"],["���D", "����"],["���D", "����"] �p������
	#���������o ���a���S����O��J ���D���Τӧx��, �Ҽ{���a��_��J���� �ɶq���n�ίS�O�r �`���r
	#�Цۦ�ק�μW�[ �ۭq���D�P����
	qa = [ 
		["�п�J���A�P���w�w��","3"]
		,["�п�J�����AGM�W��","XXX"]
		,["�@�P�����h�֤�","7"]
		]
		
	#�����e§ [���~ID, �̤�, �̦h, ���v], [���~ID, �̤�, �̦h, ���v], [���~ID, �̤�, �̦h, ���v]
	#���v 100 = 100% ���e
	#�i�ۦ�W�[ ���
	gifts = [
		[57,10000,99999,100]
		,[57,10,100,100]
		,[57,1,1,100]
	]

	#gifts = [] #�p���e§
	
	commands = ["�ϥ~��", "ab", "AB", "abq"] #.abq �O GM ���հ��D ���ץ�
	
	def useVoicedCommand(self, command, player, params):
		if command == "abq" and player.isGM():
			self.showQuestion(player)
			return
		
		st = player.getQuestState(self.qn)
		if not st:
			st = self.newQuestState(player)
			st.setState(State.STARTED)
		if st.get("answer") == None or len(st.get("answer")) == 0:
			self.info("%s %s %s %s %s" % (self.qn, command, player, params, "�S�����פU�@��"))
			player.sendMessage("�ثe���ݭn�^���ϥ~���t��")
			return
		if params == None:
			self.showQuestion(player)
			return
		if st.get("answer") == params:
			self.info("%s %s %s %s %s" % (self.qn, command, player, params, "���ץ��T"))
			self.cancelQuestTimer("timeout_%d" % player.getObjectId(), None, player)
			self.showScreenMessage(player, "%s\n���ץ��T ���Z�F" % self.title)
			st.set("try", "0")
			st.set("answer", "")
			for i in self.gifts:
				item_id, min_c, max_c, c = i
				if c >= self.getRandom(100):
					player.addItem(self.qn, item_id, min_c + self.getRandom(max_c - min_c), None, True)
		else:
			tried = str(st.getInt("try") + 1)
			st.set("try", tried)
			self.info("%s %s %s %s %s" % (self.qn, command, player, params, "���׿��~ ���Ѧ���%s" % tried))
			player.sendMessage("���׿��~ ���Ѧ��� %s" % tried)
			if int(tried) >= self.max_retry:
				st.set("answer", "")
				self.info("%s %s %s %s %s" % (self.qn, command, player, params, "���� %d �� ���_��" % tried))
				self.cancelQuestTimer("timeout_%d" % player.getObjectId(), None, player)
				self.showScreenMessage(player, "%s\n���׿��~���ƹL�h" % self.title)
				self.jail(player)
				return
			self.showQuestion(player)
			
	def getVoicedCommandList(self):
		return self.commands
		
	def __init__(self, id = qID, name = qn, descr = qDesc):
		self.qID, self.qn, self.qDesc = id, name, descr
		JQuest.__init__(self, id, name, descr)
		self.setOnEnterWorld(True)
		VoicedCommandHandler.getInstance().registerHandler(self)
		self.startQuestTimer("check", self.interval + (1000 * self.getRandom(self.interval_random_delay_sec)), None, None, False)
		print "���a�i�� .%s" % " .".join(self.commands)
		print "%s loaded" % self.qn
	
	def info(self, message):
		Logger.getLogger(self.qn).info(message)
		
	def jail(self, player):
		player.setPunishLevel(L2PcInstance.PunishLevel.JAIL, self.jail_duration)
		
	def showScreenMessage(self, player, message, duration = 10000):
		player.sendPacket(ExShowScreenMessage(message, duration))

	def genMathAddQuestion(self):
		q1, q2 = self.getRandom(100), self.getRandom(100) #2��� �[�k
		return ["�Эp�� %d + %d = ?" % (q1, q2), str(q1+q2)]

	def genNumberConvertQuestion(self):
		t = ["","�@","�G","�T","�|","��","��","�C","�K","�E"]
		o = ["","�Q","��","�d","�U","�Q","��","�d","��","�Q","��","�d"]
		q = a = ""
		m = 5 #5��Ʀr, �̦h 12 ��
		for x in xrange(m-1, -1, -1):
			r = self.getRandom(9)+1
			q += t[r] + o[x]
			a += str(r)
		return ["�ХH�Ʀr�^�� %s" % q, a]
		
	def getQuestion(self):
		r = self.getRandom(100)
		if r in xrange(0,33): #33% �X�{ �[�k�D
			return self.genMathAddQuestion()
		elif r in xrange(33,66): #33% �X�{ �Ʀr�ഫ�D
			return self.genNumberConvertQuestion()
		return self.qa[self.getRandom(len(self.qa))] #��l���v �X�{�ۭq�D
	
	def showQuestion(self, player):
		st = player.getQuestState(self.qn)
		if not st:
			st = self.newQuestState(player)
			st.setState(State.STARTED)
		q = self.getQuestion()
		self.info("%s %s %s %s" % (self.qn, player, q[0], q[1]))
		st.set('answer', str(q[1]))
		self.showScreenMessage(player, "%s\n%s\n%s" % (self.title, self.desc, q[0]), self.question_duration)
		if self.isShowHtml:
			player.sendPacket(NpcHtmlMessage(player.getObjectId(), "<html><body>%s<br>%s<br>%s</body></html>" % (self.title, self.desc, q[0])))
		
	def checkCondition(self, player):
		if player.isGM(): return False #GM ����, �`�N �p�GGM�Q���ݭn�ѥt�@��GM����
		if player.isInOlympiadMode(): return False #��P ����
		if not TownManager.getTown(player.getX(), player.getY(), player.getZ()) == None: return False #�b���� ����
		if player.isInsideZone(L2Character.ZONE_PEACE): return False #�w���a�� ����
		if player.getAI().getIntention() == CtrlIntention.AI_INTENTION_IDLE: return False #�o�b ����
		#if player.getAI().getIntention() == CtrlIntention.AI_INTENTION_FOLLOW: return False #���H ����
		#if player.getAI().getIntention() == CtrlIntention.AI_INTENTION_MOVE_TO: return False #�]�� ����
		#if player.getAI().getIntention() == CtrlIntention.AI_INTENTION_REST: return False #���U�� ����		
		if player.isInJail(): return False #�ʸT�� ����
		st = player.getQuestState(self.qn)
		if not st:
			st = self.newQuestState(player)
			st.setState(State.STARTED)
		if self.timepass_check:
			last = st.get('last_time')
			if last and time.time() - float(last) < self.timepass: return False #�K���ɶ��� ����
		if st.getQuestTimer("timeout_%d" % player.getObjectId()): return False #�w�b�˴��� ����
		return True

	def doCheck(self):
		l2world = L2World.getInstance()
		pl = [x for x in l2world.getAllPlayers().values() if self.checkCondition(x)]
		pc = len(pl)
		if pc < 1: return
		lucky_player = pl[self.getRandom(pc)]
		self.showQuestion(lucky_player)
		self.startQuestTimer("timeout_%d" % lucky_player.getObjectId(), self.question_duration, None, lucky_player, False)
		if self.timepass_check:
			st = lucky_player.getQuestState(self.qn)
			if not st:
				st = self.newQuestState(lucky_player)
				st.setState(State.STARTED)
			st.set('last_time', str(time.time()))
		
	def onAdvEvent(self, event, npc, player):
		if event == "check":
			self.startQuestTimer("check", self.interval + (1000 * self.getRandom(self.interval_random_delay_sec)), None, None, False)
			self.doCheck()
		elif event.startswith("timeout"):
			self.info("%s �ϥ~���˴��W��" % player.getName())
			self.jail(player)
			
	def onEnterWorld(self, player):
		st = player.getQuestState(self.qn)
		if not st:
			st = self.newQuestState(player)
			st.setState(State.STARTED)
		if st.getQuestTimer("timeout_%d" % player.getObjectId()):
			self.showQuestion(player)

VCAntiBot()