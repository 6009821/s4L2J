import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest
from com.l2jserver.gameserver import Shutdown
from com.l2jserver.gameserver import GmListTable

qn = "server_restart"

NPCS_ID = [9922350] #Ĳ�o NPC ID
allow_server_restart_player_name_list = ["�b��", "�ͯb", "�b��", "GM", "���a"] #���v�i�H���s�Ұʦ��A�������a/GM�W�r

class server_restart(JQuest):
	def __init__(self, id, name, descr):
		JQuest.__init__(self, id, name, descr)

	def c_to_l2html(self, text):
		text = text.replace("\n", "<br>")
		return "<html><body>" + text + "</body></html>"
		
	def onFirstTalk(self, npc, player):
		if GmListTable.getInstance().isGmOnline(True):
			return self.c_to_l2html("GM �b�u��\n���ҥ\��ȮɵL��\n�u�� GM ���b�u�ɤ~��ϥΦ��\��")
		return self.c_to_l2html("<a action=\"bypass -h Quest server_restart namelist\">�d�߱��v���Ҫ��a�W��</a>\n<a action=\"bypass -h Quest server_restart request\">�n�D���s�Ұ�</a>")
			
	def onAdvEvent(self, event, npc, player):
		e = event.split()
		if e[0] == "restart":
			try:
				delay = int(e[1])
			except:
				delay = 180
			if delay <= 0 or delay > 300:
				return self.c_to_l2html("��J�ȿ��~\n���Ľd�� 1-300")
			if player.getName() in allow_server_restart_player_name_list:
				Shutdown.getInstance().startShutdown(player, delay, True)
				return self.c_to_l2html("���A���N�� " + str(delay) + "�᭫�s�Ұ�")
			else:
				return self.c_to_l2html(player.getName() + " �A�S�����s�Ұʦ��A�����v��")
		if e[0] == "namelist":
			return self.c_to_l2html("�H�U���a�w���v�i�H���s�Ұʦ��A��\n" + reduce(lambda a, b: a + "\n" + b, allow_server_restart_player_name_list))
		if e[0] == "request":
			return self.c_to_l2html("�h�֬�᭫�s�Ұʦ��A��<edit var=\"value\" width=75 height=12><a action=\"bypass -h Quest server_restart restart $value\">�T�{����</a>")


QUEST = server_restart(-1, qn, "Custom")

for id in NPCS_ID:
	QUEST.addStartNpc(id)
	QUEST.addFirstTalkId(id)
	QUEST.addTalkId(id)

print "server_restart loaded"
