from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

class Quest(JQuest):
	qID = -1
	qn = "DeLevel"
	qDesc = "custom"
	NPCID = 100 #�]�wĲ�o�� NPC ID
	
	min_level = 20 #�]�w. �̧C�i���ܦh�֯�. 
	max_level = 80 #�]�w. �̰��i���ܦh�֯�. 

	htm_header = """<html><title>�����}��</title><body>"""
	htm_footer = """</body></html>"""
	
	htm_intro = """��J�����C���Ŧܦh�֯�<br>��J�d�� �̰� %d �̧C %d <BR>�M����U ���� �s��/���s �T�{ """ % (min_level, max_level)
	htm_input = """<edit var="value"><a action="bypass -h Quest %s show_confirm $value">�n�D������</a>""" % qn
	htm_confirm = """<a action="bypass -h Quest %s confirm %d">�T�{������ %d ��</a>"""
	htm_level_error = """��J���ſ��~.<BR> �п�J��ۤv���Ÿ��C�����Ũӭ���. """
	htm_delevel_done = """��������"""
	htm_level_outOfRange = """�����ſ�J�ƭ� �W�X�d�� �̰� %d �̧C %d """ % (min_level, max_level)
	
	def __init__(self, id = qID, name = qn, descr = qDesc):
		self.qID, self.qn, self.qDesc = id, name, descr
		JQuest.__init__(self, id, name, descr)
		self.addStartNpc(self.NPCID)
		self.addFirstTalkId(self.NPCID)
		self.addTalkId(self.NPCID)
		print "%s loaded" % self.qn

	def onAdvEvent(self, event, npc, player):
		if event.startswith("show_confirm "):
			wantedLevel = int(event[len("show_confirm "):]) or 999
			if player.getLevel() > wantedLevel:
				if self.min_level <= wantedLevel <= self.max_level:
					return self.returnHTML(self.htm_confirm % (self.qn, wantedLevel, wantedLevel))
				else:
					return self.returnHTML(self.htm_level_outOfRange)
			else:
				return self.returnHTML(self.htm_level_error)
		elif event.startswith("confirm "):
			wantedLevel = int(event[len("confirm "):]) or 999
			self.delevel(player, wantedLevel)
			return self.returnHTML(self.htm_delevel_done)

	def onFirstTalk(self, npc, player):
		return self.returnHTML(self.htm_intro + self.htm_input)
		
	def returnHTML(self, s):
		return self.htm_header + s + self.htm_footer
		
	def delevel(self, player, level):
		if player.getLevel() > level:
			player.getStat().addLevel(level - player.getLevel())
		
Quest()	
