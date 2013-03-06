import sys
from com.l2jserver.gameserver.model.quest		import State
from com.l2jserver.gameserver.model.quest		import QuestState
from com.l2jserver.gameserver.model.quest.jython	import QuestJython as JQuest

from com.l2jserver.gameserver.datatables import ClanTable
from com.l2jserver.gameserver.network.serverpackets import JoinPledge
from com.l2jserver.gameserver.network.serverpackets import SystemMessage
from com.l2jserver.gameserver.model import L2Clan
from com.l2jserver.gameserver.network import SystemMessageId
from com.l2jserver.gameserver.instancemanager import CastleManager
from com.l2jserver.gameserver.instancemanager import FortManager
from com.l2jserver.gameserver.network.serverpackets import PledgeShowMemberListAdd
from com.l2jserver.gameserver.network.serverpackets import PledgeShowInfoUpdate
from com.l2jserver.gameserver.network.serverpackets import PledgeShowMemberListAll

from java.lang import System

class Quest(JQuest):
	qID = -1
	qn = "AutoJoinClan"
	qDesc = "custom"

	NPCID = [103]
	
	show_can_self_join_only = True #�O�_�u��� �w�]���i�ۦ�[�J�����
	
	htm_header = "<html><title>�ۧU�[�J����t��</title><body>"
	htm_footer = "</body></html>"
	htm_first_into = "²��<BR>.............<BR>"
	htm_first_clanlist = "<a action=\"bypass -h Quest " + qn + " list\">����C��</a><BR>"
	htm_first_leader_setting = "<a action=\"bypass -h Quest " + qn + " leader_setting\">���D�]�w</a><BR>"
	htm_first = htm_first_into + htm_first_clanlist + htm_first_leader_setting
	
	htm_leader_auto_on = "<a action=\"bypass -h Quest " + qn + " auto_on\">�]�w�۰ʥ[�J����\��}</a><BR>"
	htm_leader_auto_off = "<a action=\"bypass -h Quest " + qn + " auto_off\">�]�w�۰ʥ[�J����\����</a><BR>"
	htm_leader = htm_leader_auto_on + htm_leader_auto_off
	
	htm_not_leader = "�A���O������D �S���v���]�w"
	htm_cannot_join = "����[�J. ���󤣦X"
	
	#�[�J�� �N�|�Q�[�J���������@��, ���Ҽ{�� �i�����٨S���˽ö�, �M�h�� �ҥH�Ȯɳ]�w���[�J���ݦ��
	#pledgeType = 0 #0=����, 100=�˽ö�1, 200=�˽ö�2, 1001=�M�h��1, 1002=�M�h��2, 2001=�M�h��3, 2002=�M�h��4
	
	# // Sub-unit types
	# /** Clan subunit type of Academy */
	# public static final int SUBUNIT_ACADEMY = -1;
	# /** Clan subunit type of Royal Guard A */
	# public static final int SUBUNIT_ROYAL1 = 100;
	# /** Clan subunit type of Royal Guard B */
	# public static final int SUBUNIT_ROYAL2 = 200;
	# /** Clan subunit type of Order of Knights A-1 */
	# public static final int SUBUNIT_KNIGHT1 = 1001;
	# /** Clan subunit type of Order of Knights A-2 */
	# public static final int SUBUNIT_KNIGHT2 = 1002;
	# /** Clan subunit type of Order of Knights B-1 */
	# public static final int SUBUNIT_KNIGHT3 = 2001;
	# /** Clan subunit type of Order of Knights B-2 */
	# public static final int SUBUNIT_KNIGHT4 = 2002;

	
	def __init__(self, id = qID, name = qn, descr = qDesc):
		JQuest.__init__(self, id, name, descr)
		for id in self.NPCID:
			self.addStartNpc(id)
			self.addFirstTalkId(id)
			self.addTalkId(id)
		print "Init:" + self.qn + " loaded"

	def isLeader(self, player):
		clan = player.getClan()
		if not clan: return False
		if clan.getLeaderId() != player.getObjectId(): return False
		return True
		
	def showClanList(self, player):
		r = "<table><tr><td width=150>����W��</td><td width=150>���D</td><td width=100></td><td width=10></td></tr>"
		for clan in ClanTable.getInstance().getClans():
			link = ""
			auto_join = clan.getNotice() == "auto_join"
			if self.show_can_self_join_only and auto_join == False:
				continue
			if auto_join:
				link = '<a action="bypass -h Quest %s select_pt %d">�I���[�J</a>' % (self.qn, clan.getClanId())
				if player.isGM():
					delete = '<a action="bypass -h Quest %s unset_pt %d">X</a>' % (self.qn, clan.getClanId())
				else:
					delete = ""
			r += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (clan.getName(), clan.getLeaderName(), link, delete)
		r += "</table>"
		return self.htm_header + r + self.htm_footer
		
	def showSelectPledgeType(self, clanid):
		clan = ClanTable.getInstance().getClan(clanid)
		r = "�п�ܥ[�J���@��<BR>"
		r += "�[�J��� %s<BR>" % clan.getName()
		r += '<a action="bypass -h Quest %s apply %d %d">%s</a><br1>' % (self.qn, clan.getClanId(), 0, "���ݦ��")
		for sp in clan.getAllSubPledges():
			r += '<a action="bypass -h Quest %s apply %d %d">%s</a><br1>' % (self.qn, clan.getClanId(), sp.getId(), sp.getName())
		return self.htm_header + r + self.htm_footer
		
		
	def showLeaderSetting(self):
		return self.htm_header + self.htm_leader + self.htm_footer

	def canMeJoin(self, player, clanid, pledgeType):
		clan = ClanTable.getInstance().getClan(clanid)
		if not clan: return False
		if clan.getCharPenaltyExpiryTime() > System.currentTimeMillis():
			player.sendPacket(SystemMessageId.YOU_MUST_WAIT_BEFORE_ACCEPTING_A_NEW_MEMBER)
			return False
		if player.getClanId() != 0:
			sm = SystemMessage.getSystemMessage(SystemMessageId.S1_WORKING_WITH_ANOTHER_CLAN)
			sm.addString(player.getName())
			player.sendPacket(sm)
			return False
		if player.getClanJoinExpiryTime() > System.currentTimeMillis():
			sm = SystemMessage.getSystemMessage(SystemMessageId.C1_MUST_WAIT_BEFORE_JOINING_ANOTHER_CLAN)
			sm.addString(player.getName())
			player.sendPacket(sm)
			return False
		if player.getLevel() > 40 or player.getClassId().level() >= 2:
			if pledgeType == -1:
				sm = SystemMessage.getSystemMessage(SystemMessageId.S1_DOESNOT_MEET_REQUIREMENTS_TO_JOIN_ACADEMY)
				sm.addString(player.getName())
				player.sendPacket(sm)
				player.sendPacket(SystemMessageId.ACADEMY_REQUIREMENTS)
				return False
		if clan.getSubPledgeMembersCount(pledgeType) >= clan.getMaxNrOfMembers(pledgeType):
			if pledgeType == 0:
				sm = SystemMessage.getSystemMessage(SystemMessageId.S1_CLAN_IS_FULL)
				sm.addString(clan.getName())
				player.sendPacket(sm)
			else:
				player.sendPacket(SystemMessageId.SUBCLAN_IS_FULL)
			return False
		return True
		
	def myJoinClan(self, player, clanid, pledgeType):
		clan = ClanTable.getInstance().getClan(clanid)
		if clan:
			player.sendPacket(JoinPledge(clanid))
			# player.setPledgeType(L2Clan.SUBUNIT_ROYAL1)
			player.setPledgeType(pledgeType)
			if pledgeType == L2Clan.SUBUNIT_ACADEMY:
				player.setPowerGrade(9)
				player.setLvlJoinedAcademy(player.getLevel())
			else:
				player.setPowerGrade(5)
			clan.addClanMember(player)
			player.setClanPrivileges(clan.getRankPrivs(5))
			player.sendPacket(SystemMessageId.ENTERED_THE_CLAN)
			sm = SystemMessage.getSystemMessage(SystemMessageId.S1_HAS_JOINED_CLAN)
			sm.addString(player.getName())
			clan.broadcastToOnlineMembers(sm)
			try:
				#GS 879 �H��
				if player.getClan().getCastleId() > 0:
					CastleManager.getInstance().getCastleByOwner(player.getClan()).giveResidentialSkills(player)
				if player.getClan().getFortId() > 0:				
					FortManager.getInstance().getFortByOwner(player.getClan()).giveResidentialSkills(player)
			except:
				#GS 879 ���e
				if player.getClan().getHasCastle() > 0:
					CastleManager.getInstance().getCastleByOwner(player.getClan()).giveResidentialSkills(player)
				if player.getClan().getHasFort() > 0:				
					FortManager.getInstance().getFortByOwner(player.getClan()).giveResidentialSkills(player)
			player.sendSkillList()
			clan.broadcastToOtherOnlineMembers(PledgeShowMemberListAdd(player), player)
			clan.broadcastToOnlineMembers(PledgeShowInfoUpdate(clan))
			player.sendPacket(PledgeShowMemberListAll(clan, player))
			player.setClanJoinExpiryTime(0)
			player.broadcastUserInfo()
			
	def onAdvEvent(self, event, npc, player):
		if not event: return self.onFirstTalk()
		if event == "list":
			return self.showClanList(player)
		elif event.startswith("unset_pt "):
			try:
				clanid = int(event[9:])
			except:
				return self.htm_header + "unset_pt �Ѽƿ��~ *" + event + "*" + self.htm_footer
			if player.isGM():
				clan = ClanTable.getInstance().getClan(clanid)
				clan.setNotice("")
		elif event == "leader_setting":
			if self.isLeader(player):
				return self.showLeaderSetting()
			else:
				return self.htm_header + self.htm_not_leader + self.htm_footer
		elif event == "auto_on":
			if self.isLeader(player):
				player.getClan().setNotice("auto_join")
		elif event == "auto_off":
			if self.isLeader(player):
				player.getClan().setNotice("")
		elif event.startswith("select_pt "):
			try:
				clanid = int(event[10:])
			except:
				return self.htm_header + "select_pt �Ѽƿ��~ *" + event + "*" + self.htm_footer
			return self.showSelectPledgeType(clanid)
		elif event.startswith("apply "):
			p = event[6:].split()
			if len(p) != 2 or p[1] not in ["-1","0","100","200","1001","1002","2001","2002"]:
				return self.htm_header + "�Ѽƿ��~ *" + event + "*" + self.htm_footer
			try:
				clanid = int(p[0])
			except:
				return self.htm_header + "apply �Ѽƿ��~ *" + event + "*" + self.htm_footer
			if self.canMeJoin(player, clanid, int(p[1])):
				self.myJoinClan(player, clanid, int(p[1]))
			else:
				return self.htm_header + self.htm_cannot_join + self.htm_footer
		return self.onFirstTalk(npc, player)
		

	def onFirstTalk(self, npc, player):
		st = player.getQuestState(self.qn)
		if not st:
			st = self.newQuestState(player)
			st.setState(State.STARTED)
		return self.htm_header + self.htm_first + self.htm_footer
		
Quest()
