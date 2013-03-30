import sys
from com.l2jserver.gameserver.model.quest.jython	import QuestJython as JQuest

from com.l2jserver.gameserver.datatables import SkillTable #�ޯत��W����
from com.l2jserver.gameserver.datatables import SkillTreesData #�ǲߧޯ����
from com.l2jserver.gameserver.model import L2SkillLearn #�ǲߧޯ����
from com.l2jserver.gameserver.model.skills import L2Skill #�ޯ����

import math

class EasySkillRemove(JQuest):
	qID = -1
	qn = "easySkillRemove"
	qDesc = "custom"
	NPCID = [100] #Ĳ�o���Ȫ� NPC �i�ק�.. �i�H�h ID �Ҧp [100,102,103]
	rpp = 10 #�C����ܦh�֭ӰO��

	htm_header = "<html><body><title>²���ޯ�R���}��</title>"
	htm_search = "��J�ޯ�W�٩�ID�@�j�M<table><tr><td><edit var=\"value\" width=150 height=12></td><td><button value=\"�j�M\" width=50 height=20  action=\"bypass -h Quest " + qn + " search $value\"></td></tr></table>"
	htm_footer = "</body></html>"
	htm_list_header = "�w�ǲߪ��ޯ�M��<br1>"
	htm_warning = "<font color=ff0000>(�`�N!�I���ޯ�s�� �Y�ɧR��)</font><BR1>"

	def __init__(self, id=qID, name=qn, descr=qDesc):
		qID, qn, qDesc = id, name, descr
		JQuest.__init__(self, id, name, descr)
		for id in self.NPCID:
			self.addStartNpc(id)
			self.addFirstTalkId(id)
			self.addTalkId(id)
		print "Init:" + self.qn + " loaded"

	def onAdvEvent(self, event, npc, player):
		if event.startswith('page '):
			page = event[len('page '):]
			return self.htm_header + self.htm_search + self.listSkills(player, int(page)) + self.htm_footer
		elif event.startswith('remove '):
			sid, slv = event[len('remove '):].split()
			sid = int(sid)
			slv = int(slv)
			player.removeSkill(SkillTable.getInstance().getInfo(sid, slv))
			player.sendSkillList()
		elif event.startswith('search '):
			kw = event[len('search '):]
			r = self.htm_warning
			skillTable = SkillTable.getInstance()
			for s in player.getAllSkills():
				if kw in skillTable.getInfo(s.getId(), s.getLevel()).getName() or kw == str(s.getId()):
					r += self.makeRemoveLink(s)
			return self.htm_header + self.htm_search + r + self.htm_footer
		return self.onFirstTalk(npc, player)
		
	def onFirstTalk(self, npc, player):
		return self.htm_header + self.htm_search + self.listSkills(player, 1) + self.htm_footer

	def makeRemoveLink(self, skill):
		return "<a action=\"bypass -h Quest " + self.qn + " remove " + str(skill.getId()) + " " + str(skill.getLevel()) + "\">" + SkillTable.getInstance().getInfo(skill.getId(), skill.getLevel()).getName() + "(%d)" % str(skill.getId()) + " Lv " + str(skill.getLevel()) + "</a><BR1>"
		
	def listSkills(self, player, page):
		#sl = player.getAllSkills() #GS 890 �ΥH�e
		sl = player.getAllSkills().toArray() #GS 891 �ΥH��

		total_page = int(math.ceil(len(sl) / (self.rpp + 0.0)))
		r = self.htm_list_header
		r += "��&nbsp;"
		for i in xrange(1,total_page + 1):
			r += "<a action=\"bypass -h Quest " + self.qn + " page " + str(i) + "\">" + str(i) + "</a>&nbsp;"
		r += "��<BR1>"
		r += self.htm_warning

		start = self.rpp * (page - 1)
		stop = self.rpp * page
		for s in sl[start:stop]:
			r += self.makeRemoveLink(s)
		return r
		
EasySkillRemove()
