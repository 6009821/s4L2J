import sys
from com.l2jserver.gameserver.model.quest		import State
from com.l2jserver.gameserver.model.quest		import QuestState
from com.l2jserver.gameserver.model.quest.jython	import QuestJython as JQuest

from com.l2jserver.util					import Rnd
from com.l2jserver.gameserver.datatables		import NpcTable
from com.l2jserver.gameserver.model			import L2DropData
from com.l2jserver.gameserver.ai			import CtrlIntention
from com.l2jserver.gameserver.model			import L2World
from com.l2jserver.gameserver.network.serverpackets	import NpcSay
from com.l2jserver.gameserver				import GameTimeController
from com.l2jserver.gameserver.datatables		import SkillTable
from com.l2jserver.gameserver				import Announcements
from com.l2jserver.gameserver.instancemanager		import TownManager

class NewYearEvent(JQuest):
	qID = -1
	qn = "NewYear_2011"
	qDesc = "custom"

	#�������~ ID, ��, ���̤�, ���̦h, ���v 1 * 10000 = 1%
	#itemID, category, minD, maxD, chance
	event_droplist = [
		[10304, 15, 1, 1, 5 * 10000],	#�ܨ���L��-�C����
		[20876, 1, 1, 1, 5 * 10000],	#�ʦ~�n�X
		[20877, 2, 1, 1, 5 * 10000],	#�~�~���l
		[20878, 3, 1, 1, 5 * 10000],	#�꺡�p�N
		[20879, 4, 1, 1, 5 * 10000],	#���ߵo�]
		[20880, 5, 1, 1, 5 * 10000],	#���ɺ���
		[20881, 6, 1, 1, 5 * 10000],	#��}�I�Q
		[20882, 7, 1, 1, 5 * 10000],	#�����
		[20870, 8, 1, 1, 1 * 10000],	#�����@��
		[20871, 9, 1, 1, 1 * 10000],	#�����@��
		[20872, 10, 1, 1, 1 * 10000],	#�Ŧ��@��
		[20873, 11, 1, 1, 1 * 10000],	#�������@��
		[20874, 12, 1, 1, 1 * 10000],	#�զ��@��
		[20875, 13, 1, 1, 1 * 10000],	#�Ȧ��@��
		[20788, 14, 1, 2, 50 * 10000]	#�Ϥ��c
	]

	boss_droplist = event_droplist + [
		[57, 20, 100000, 1000000, 100 * 10000],	#���� 10-100�U 100%
		[57, 21, 100000, 1000000, 100 * 10000],	#���� 10-100�U 100%
		[57, 22, 100000, 1000000, 100 * 10000],	#���� 10-100�U 100%
		[57, 23, 100000, 1000000, 100 * 10000],	#���� 10-100�U 100%
		[57, 24, 100000, 1000000, 100 * 10000],	#���� 10-100�U 100%
		[57, 25, 100000, 1000000, 100 * 10000],	#���� 10-100�U 100%
	]

	npc_droplist = event_droplist + [
		[57, 0, 10000, 50000, 90 * 10000],	#���� 1-5�U 90%
		[20870, -1, 1, 1, 10 * 10000],	#�����@�� �^��
		[20871, -1, 1, 1, 10 * 10000],	#�����@�� �^��
		[20872, -1, 1, 1, 10 * 10000],	#�Ŧ��@�� �^��
		[20873, -1, 1, 1, 10 * 10000],	#�������@�� �^��
		[20874, -1, 1, 1, 10 * 10000],	#�զ��@�� �^��
		[20875, -1, 1, 1, 10 * 10000]	#�Ȧ��@�� �^��
	]

	Boss = [29118] #BOSS �گP��
	#�p�ǲM��
	NPCs = [22272, 22273, 22274, 22393, 22394, 22395, 22411, 22412, 22413, 22414, 22415, 22439, 22440, 22441, 22442, 18371, 18372, 18373, 18374, 18375, 18376, 18377, 18490, 27278]

	spawn_rate = 20 #�S�ܼC���ꥴ Boss �|�ͤp�Ǫ����v, 1 = 1%

	npc_town_spawn_time = 1000 * 60 * 1  # 1 ���� �b���� �䪱�a �ͤ@��
	npc_town_spawn_chance = 33	# ���̥ͩǾ��v
	npc_town_spawn_min = 1		# �̤֥ͦh�ְ���
	npc_town_spawn_max = 5		# �̦h�ͦh�ְ���

	isGM_join_event = True	# �p�G False, GM �������ʱ���v�T

	npc_spawn_say = [
		'%player_name% �����a',
		'�~��~�� %player_name%���ܦh�~�� �m!',
		'���ߵo�] �~�殳�� %player_name% ���I�~��ӦY',
		'�ܭ��ܭ� �ڶ��F �O�~�檺���D �N�b %player_name% ���W, �S�̭� �W��!!',
		'%player_name% ���O�C����, ��..',
		'�W�m�Q�~ �N�O���F�� %player_name% ���U',
		'%player_name% ��U�~��, �d�A����',
		'ť�D %player_name% �N�b�o�ӫ���, ���A�F'
	]

	#BOSS_spawn_info ���]�w �|�C���ɶ� 1�� (�{�� 4�p��) ���ͤ@��
	# ID, [�C���ɶ�, BOSS ID, X, Y, Z, ���V, ��m�H������, �{��ɶ��s�b�h�[] 0 = ������ (���طN 0 �p�G�S���a�h�� �|�ֿn�ܦh��)
	BOSS_spawn_info = dict([
		['boss1', ['00:00', 29118, 149494, 46727, -3413, 0, True, 59 * 60 * 1000]],	#�w�]�{��ɶ� 59���������, �j�ꫬ�v�޳����� �C���ɶ� 0��0��
		['boss2', ['06:00', 29118, 7058, -23681, -3708, 0, True, 240 * 60 * 1000]],	#�w�]�{��ɶ� 4�p�ɫ����, ��l���q
		['boss3', ['18:30', 29118, -11166, 254195, -3189, 0, True, 3300 * 1000]]	#�w�] �C���ɶ� 330��������� �N�O �C���ɶ� 00:00 ����, �F�ɥC��
	])

	ask_transform_zone = [
		300690,
		300691
	]

	main_town_id = [
		12,	#�ȤB
		9,	#�_��
		13,	#���F�S
		17,	#�ץ[�S
		14,	#�|�]
		15,	#���W����������
		5,	#�j�|�B��
		7,	#�j�|�B��
		8,	#�f��
		16,	#��ù��
		11,	#�y�H��
		10,	#�ڷ�
		2,	#���ܤ��q
		6,	#�G�H��
		3,	#���F��
		4,	#�b�~�H��
		1,	#�º��
		20,	#��Ѩϧ�
		22,	#�ڤۮq
		33	#�p�X��a
	]
	
	# 1GameTime = �{��ɶ� 10��
	# 1GameTime = �C���ɶ� 1����
	# 60GameTime = �C���ɶ� 1�p��
	# 1440GameTime = �C���ɶ� 1��
	def comming_game_time_to_real_sec(self, game_time):
		try:
			h, m = game_time.split(':')	#���X �p��, ��
			m = int(h) * 60 + int(m)	#�Τ@�� ���p��
			diff = m - GameTimeController.getInstance().getGameTime() % 1440	#�p��ɶ��t --�C���ɶ�(��)
			if diff < 0: diff += 1440
			return diff * 10	#�����{��ɶ�(��)
		except:
			return -1	#���~�ɶǦ^ -1

	def addDrop(self, id, droplist):
		t = NpcTable.getInstance().getTemplate(id)
		for itemID, category, minD, maxD, chance in droplist:
			d = L2DropData()
			d.setItemId(itemID)
			d.setMinDrop(minD)
			d.setMaxDrop(maxD)
			d.setChance(chance) #100 * 10000 = 100%
			t.addDropData(d, category)

	def __init__(self, id = qID, name = qn, descr = qDesc):
		JQuest.__init__(self, id, name, descr)
		for id in self.Boss:
			self.addAttackId(id)
			self.addDrop(id, self.boss_droplist)
			self.addSkillSeeId(id)

		for id in self.NPCs:
			self.addDrop(id, self.npc_droplist)
			self.addSkillSeeId(id)

		for id in self.ask_transform_zone:
			self.addEnterZoneId(id)

		self.startQuestTimer('spawn_npc_in_town', self.npc_town_spawn_time, None, None, True)
		for timer_id in self.BOSS_spawn_info:
			t = self.comming_game_time_to_real_sec(self.BOSS_spawn_info[timer_id][0])
			if t >= 0:
				self.startQuestTimer(timer_id, t * 1000, None, None, False)
			else:
				print self.qn +':BPSS_spawn_info ���ɶ��榡���~'
		
	def onEnterZone(self, character, zone):
		try:
			if character.getTransformationId(): return
			if not isGM_join_event and player.isGM(): return
		except:
			return
		skillId, skillLevel = [672, 1]
		skill = SkillTable.getInstance().getInfo(skillId, skillLevel)
		if skill:
			skill.getEffects(character, character)

	def onSkillSee(self, npc, caster, skill, targets, isPet):
		try:
			if not isGM_join_event and caster.isGM(): return
		except:
			pass
		npc.addDamageHate(caster, 0, len(targets)*1000)
		npc.getAI().setIntention(CtrlIntention.AI_INTENTION_ATTACK, caster)

	def onAttack(self, npc, player, damage, isPet, skill):
		try:
			if player and player.getTransformationId() != 5: # �C�����ܨ� ID 5
				if Rnd.get(100) < spawn_rate:
					self.myAddSpawn(npc, player, damage)
		except:
			pass

	def myAddSpawn(self, npc, player, damage): # npc �Χ@�l���m, player �Q���몺���a
		n = self.addSpawn(self.NPCs[Rnd.get(len(self.NPCs))], npc, False)
		n.addDamageHate(player, 0, damage * 1000 / (player.getLevel() + 7))
		n.getAI().setIntention(CtrlIntention.AI_INTENTION_ATTACK, player)
		npc.broadcastPacket(NpcSay(n.getObjectId(), 0, n.getNpcId(), self.npc_spawn_say[Rnd.get(len(self.npc_spawn_say))].replace('%player_name%', player.getName()) ))

	def canSpawn(self, player):
		if not player: return False
		if not self.isGM_join_event and player.isGM(): return False
		if player.isSilentMoving(): return False
		if player.getTransformationId() == 5: return False
		if player.getAI().getIntention() == CtrlIntention.AI_INTENTION_IDLE: return False
		if player.getAI().getIntention() == CtrlIntention.AI_INTENTION_REST: return False
		if not player.isInsideZone(player.ZONE_TOWN): return False
		if TownManager.getTown(player.getX(), player.getY(), player.getZ()).getTownId() not in self.main_town_id: return False
		if Rnd.get(100) > self.npc_town_spawn_chance: return False
		return True

	def onAdvEvent(self, event, npc, player):
		print event, npc, player
		if event == 'spawn_npc_in_town':
			for player in L2World.getInstance().getAllPlayers().values():
				print player
				if self.canSpawn(player):
					print "canspawn"
					c = Rnd.get(self.npc_town_spawn_max - self.npc_town_spawn_min) + self.npc_town_spawn_min
					for i in range(c):
						self.myAddSpawn(player, player, 1000)
		elif event in self.BOSS_spawn_info:
			t, boss_id, x, y, z, heading, random_offset, despawn_delay = self.BOSS_spawn_info[event]
			n = self.addSpawn(boss_id, x, y, z, heading, random_offset, despawn_delay)
			Announcements.getInstance().announceToAll('���� BOSS �X�{�b�u' + n.getCastle().getCName() + '�v�a�� ' + str(x) + ',' + str(y) + ',' + str(z))
			self.startQuestTimer(event, 14400*1000, None, None, False)	#�C���ɶ��@�ѫ�A����

NewYearEvent()

