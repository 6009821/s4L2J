import sys
from com.l2jserver.gameserver.model.quest		import State
from com.l2jserver.gameserver.model.quest		import QuestState
from com.l2jserver.gameserver.model.quest.jython	import QuestJython as JQuest

from com.l2jserver.gameserver.datatables import SkillTable #�ޯत��W����
from com.l2jserver.gameserver.datatables import SkillTreesData #�ǲߧޯ����
from com.l2jserver.gameserver.model import L2SkillLearn #�ǲߧޯ����
from com.l2jserver.gameserver.model.skills import L2Skill #�ޯ����

import math

qID = -1
qn = "easySkillRemove"
qDesc = "custom"

class EasySkillRemove(JQuest):
	NPCID = [103] #Ĳ�o���Ȫ� NPC �i�ק�.. �i�H�h ID �Ҧp [100,102,103]
	htm_header = "<html><body><title>²���ޯ�R���t��</title>"
	htm_search = "<table><tr><td><edit var=\"value\" width=140 height=12></td><td><button value=\"�j�M\" width=50 height=20  action=\"bypass -h Quest " + qn + " search $value\"></td></tr></table>"
	htm_footer = "</body></html>"

	def __init__(self, id, name, descr):
		JQuest.__init__(self, id, name, descr)
		for id in self.NPCID:
			self.addStartNpc(id)
			self.addFirstTalkId(id)
			self.addTalkId(id)
		print "Init:" + qn + " loaded"

	def makeRemoveLink(self, skill):
		return "<a action=\"bypass -h Quest " + qn + " remove " + str(skill.getId()) + " " + str(skill.getLevel()) + "\">" + SkillTable.getInstance().getInfo(skill.getId(), skill.getLevel()).getName() + " Lv " + str(skill.getLevel()) + "</a><BR1>"
		
	def listSkills(self, player, page):
		#sl = player.getAllSkills() #GS 890 �ΥH�e
		sl = player.getAllSkills().toArray() #GS 891 �ΥH��
		rpp = 13

		total_page = int(math.ceil(len(sl) / (rpp + 0.0)))
		r = "�w�ǲߪ��ޯ�M�� (�`�N!�I���R��)<br1>"
		r += "��&nbsp;"
		for i in xrange(1,total_page + 1):
			r += "<a action=\"bypass -h Quest " + qn + " page " + str(i) + "\">" + str(i) + "</a>&nbsp;"
		r += "��<BR1>"

		start = rpp * (page - 1)
		stop = rpp * page
		for s in sl[start:stop]:
			r += self.makeRemoveLink(s)
		return r

	def onAdvEvent(self, event, npc, player):
		if event.startswith('page '):
			page = event[5:]
			return self.htm_header + self.htm_search + self.listSkills(player, int(page)) + self.htm_footer
		elif event.startswith('remove '):
			sid, slv = event[7:].split()
			sid = int(sid)
			slv = int(slv)
			player.removeSkill(SkillTable.getInstance().getInfo(sid, slv))
			player.sendSkillList()
		elif event.startswith('search '):
			kw = event[7:]
			r = ""
			skillTable = SkillTable.getInstance()
			for s in player.getAllSkills():
				if kw in skillTable.getInfo(s.getId(), s.getLevel()).getName():
					r += self.makeRemoveLink(s)
			return self.htm_header + self.htm_search + r + self.htm_footer
		return self.onFirstTalk(npc, player)
		
	def onFirstTalk(self, npc, player):
		st = player.getQuestState(qn)
		if not st:
			st = self.newQuestState(player)
			st.setState(State.STARTED)
		return self.htm_header + self.htm_search + self.listSkills(player, 1) + self.htm_footer
		
EasySkillRemove(qID, qn, qDesc)
