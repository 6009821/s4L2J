import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

from com.l2jserver import L2DatabaseFactory

import time

class Rank(JQuest):
	qID = -1
	qn = "Rank"
	qDesc = "custom"
	
	NPCID = 103 #Ĳ�o���Ȫ� NPC
	number_of_record = 15 #�̦h��ܦh�֦�O��

	blacklist = [] #����W�ٶ¦W�� ����ܳo�Ǩ��⪺�ƾ� �i�h�� ["GM","���äH��","�Ѥj","GM2��"]
	blacklist = ",".join(['"%s"' % x for x in blacklist])
	if len(blacklist) == 0:
		blacklist = '""'
	
	htm_header = "<html><body><title>�Ʀ�]</title>"
	htm_footer = "</body></html>"
	
	item_count_sql = "select sum(`count`) as c, COALESCE(`characters`.`char_name`, `clan_data`.`clan_name`) as name from `items` left join `characters` on `items`.`owner_id` = `characters`.`charId` left join `clan_data` on `items`.`owner_id` = `clan_data`.`clan_id` where `items`.`item_id` = %d group by `items`.`owner_id` having name not in (%s) order by c desc limit %d;"
	
	def item_count_cb(r):
		return (r.getRow(),r.getString("name"),r.getLong("c"))

	pages_header = "<table><tr><td width=32>�ƦW</td><td width=150>����W��</td><td width=150>%s</td></tr>"
	pages_body = "<tr><td>%d</td><td>%s</td><td>%d</td></tr>"
	pages_footer = "</table>"
	pages = [
		{
			"id":"����", 
			"sql":item_count_sql % (57, blacklist, number_of_record,), 
			"cb":item_count_cb,
			"header":pages_header % "����",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"�j��", 
			"sql":item_count_sql % (5575, blacklist, number_of_record,), 
			"cb":item_count_cb,
			"header":pages_header % "�j�N������",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"�y��", 
			"sql":item_count_sql % (6673, blacklist, number_of_record,), 
			"cb":item_count_cb,
			"header":pages_header % "�y�����",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"�Ŧ�", 
			"sql":item_count_sql % (4355, blacklist, number_of_record,), 
			"cb":item_count_cb,
			"header":pages_header % "�Ŧ�쫽",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"����", 
			"sql":item_count_sql % (4356, blacklist, number_of_record,), 
			"cb":item_count_cb,
			"header":pages_header % "��������",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"�Ȧ�", 
			"sql":item_count_sql % (4357, blacklist, number_of_record,), 
			"cb":item_count_cb,
			"header":pages_header % "�Ȧ�u�Y",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"���", 
			"sql":item_count_sql % (4358, blacklist, number_of_record,), 
			"cb":item_count_cb,
			"header":pages_header % "����⩬��߼�",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"�ڤ�", 
			"sql":item_count_sql % (13067, blacklist, number_of_record,), 
			"cb":item_count_cb,
			"header":pages_header % "�ڤۮq�N��",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"����", 
			"sql":item_count_sql % (3470, blacklist, number_of_record,), 
			"cb":item_count_cb,
			"header":pages_header % "����",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"���m", 
			"sql":item_count_sql % (6393, blacklist, number_of_record,), 
			"cb":item_count_cb,
			"header":pages_header % "����-���m������",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"����", 
			"sql":"SELECT `char_name`, count(1) as c FROM `character_quests` left join `characters` on `character_quests`.`charId` = `characters`.`charId` where `character_quests`.`var` = '<state>' and `character_quests`.`value` = 'Completed' and `char_name` not in (%s) group by `character_quests`.`charId` order by c desc limit %d;" % (blacklist, number_of_record,), 
			"cb":lambda r: (r.getRow(),r.getString("char_name"),r.getLong("c")),
			"header":pages_header % "���ȧ�����",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"PVP", 
			"sql":"SELECT `char_name`, `pvpkills` FROM `characters` where `char_name` not in (%s) order by `pvpkills` desc limit %d;" % (blacklist, number_of_record,), 
			"cb":lambda r: (r.getRow(),r.getString("char_name"),r.getLong("pvpkills")),
			"header":pages_header % "PVP����",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"PK", 
			"sql":"SELECT `char_name`, `pkkills` FROM `characters` where `char_name` not in (%s) order by `pkkills` desc limit %d;" % (blacklist, number_of_record,), 
			"cb":lambda r: (r.getRow(),r.getString("char_name"),r.getLong("pkkills")),
			"header":pages_header % "PK����",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"�ʦV", 
			"sql":"SELECT `char_name`, `karma` FROM `characters` where `char_name` not in (%s) order by `karma` desc limit %d;" % (blacklist, number_of_record,), 
			"cb":lambda r: (r.getRow(),r.getString("char_name"),r.getLong("karma")),
			"header":pages_header % "�ʦV",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"�n��", 
			"sql":"SELECT `char_name`, `fame` FROM `characters` where `char_name` not in (%s) order by `fame` desc limit %d;" % (blacklist, number_of_record,), 
			"cb":lambda r: (r.getRow(),r.getString("char_name"),r.getLong("fame")),
			"header":pages_header % "�ӤH�n��",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"�b�u", 
			"sql":"SELECT `char_name`, `onlinetime` FROM `characters` where `char_name` not in (%s) order by `onlinetime` desc limit %d;" % (blacklist, number_of_record,), 
			"cb":lambda r: (r.getRow(),r.getString("char_name"),long(r.getLong("onlinetime")/60/60/24)),
			"header":pages_header % "�֭p�b�u(��)",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"�g��", 
			"sql":"SELECT `char_name`, `exp` FROM `characters` where `char_name` not in (%s) order by `exp` desc limit %d;" % (blacklist, number_of_record,), 
			"cb":lambda r: (r.getRow(),r.getString("char_name"),r.getLong("exp")),
			"header":pages_header % "�g���",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"����", 
			"sql":"SELECT `char_name`, `level` FROM `characters` where `char_name` not in (%s) order by `exp` desc limit %d;" % (blacklist, number_of_record,), 
			"cb":lambda r: (r.getRow(),r.getString("char_name"),r.getLong("level")),
			"header":pages_header % "����",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"�T��", 
			"sql":"SELECT `char_name`, `punish_timer` FROM `characters` where `punish_level` = 1 and `char_name` not in (%s) order by `punish_timer` desc limit %d;" % (blacklist, number_of_record,), 
			"cb":lambda r: (r.getRow(),r.getString("char_name"),r.getLong("punish_timer")/60000),
			"header":pages_header % "�٭n�T�h�[(����)",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"�ʸT", 
			"sql":"SELECT `char_name`, `punish_timer` FROM `characters` where `punish_level` = 2 and `char_name` not in (%s) order by `punish_timer` desc limit %d;" % (blacklist, number_of_record,), 
			"cb":lambda r: (r.getRow(),r.getString("char_name"),r.getLong("punish_timer")/60000),
			"header":pages_header % "�٭n�T�h�[(����)",
			"footer":pages_footer,
			"body":pages_body
		}
		,{
			"id":"���v", 
			"sql":"SELECT `char_name`, `lastAccess` FROM `characters` where `accesslevel` = -1 and `char_name` not in (%s) order by `lastAccess` desc limit %d;" % (blacklist, number_of_record,), 
			"cb":lambda r: (r.getRow(),r.getString("char_name"),time.localtime(float(r.getLong("lastAccess")/1000))[1],time.localtime(float(r.getLong("lastAccess")/1000))[2]),
			"header":pages_header % "�̫�n��",
			"footer":pages_footer,
			"body":"<tr><td>%d</td><td>%s</td><td>%d��%d��</td></tr>"
		}
	]

	def __init__(self, id = qID, name = qn, descr = qDesc):
		JQuest.__init__(self, id, name, descr)
		self.addStartNpc(self.NPCID)
		self.addFirstTalkId(self.NPCID)
		self.addTalkId(self.NPCID)
		print "%s loaded" % (self.qn,)
		
	def db_query(self, sql, cb):
		r = []
		con, statement, rset = None, None, None
		try:
			con = L2DatabaseFactory.getInstance().getConnection()
			statement = con.prepareStatement(sql)
			rset = statement.executeQuery()
			while rset.next():
				try:
					r += [cb(rset)]
				except:
					pass
		finally:
			if rset:
				rset.close()
			if statement:
				statement.close()
			if con:
				L2DatabaseFactory.close(con)
		return r
				
	def showPages(self, pageid = pages[0]["id"]):
		def showTab():
			c = 0
			r = "<table border=0 cellpadding=0 cellspacing=0><tr>"
			for a in self.pages:
				r += '<td><button width=31 height=20 fore="L2UI_CT1.Tab_DF_Tab%s" value="%s" action="bypass -h Quest %s %s"></td>' % (["_Unselected","_Selected"][pageid == a["id"]], a["id"], self.qn, a["id"])
				c += 1
				if c % 9 == 0:
					r += "</tr><tr>"
			r += "</tr></table>"
			return r
		r = showTab()
		for a in self.pages:
			if pageid == a["id"]:
				r += a["header"]
				for record in self.db_query(a["sql"], a["cb"]):
					r += a["body"] % record
				r += a["footer"]
				break
		return self.htm_header + r + self.htm_footer
		
	def onAdvEvent(self, event, npc, player):
		for a in self.pages:
			if a["id"] == event:
				return self.showPages(event)
		return self.onFirstTalk(npc, player)
		
	def onFirstTalk(self, npc, player):
		st = player.getQuestState(self.qn)
		if not st:
			st = self.newQuestState(player)
			st.setState(State.STARTED)
		return self.showPages()
		
Rank()
