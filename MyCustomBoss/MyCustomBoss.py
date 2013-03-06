import math
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

from com.l2jserver.gameserver.instancemanager import InstanceManager
from com.l2jserver.gameserver.instancemanager.InstanceManager import InstanceWorld
from com.l2jserver.gameserver.ai import CtrlIntention
from com.l2jserver.gameserver.util import Util 
from com.l2jserver.gameserver.util import Broadcast
from com.l2jserver.gameserver.network.serverpackets import ExSendUIEvent
from com.l2jserver.gameserver.model import L2World
from com.l2jserver.gameserver.datatables import NpcTable
from com.l2jserver.gameserver.model import L2Spawn
from com.l2jserver.gameserver.datatables import SpawnTable
from com.l2jserver.gameserver.datatables import SkillTable
from com.l2jserver.util import Rnd
from com.l2jserver.gameserver.network.serverpackets import SystemMessage
from com.l2jserver.gameserver.model.actor.instance import L2PcInstance
from com.l2jserver.gameserver.model import L2Object
from java.lang import System
from com.l2jserver.gameserver.datatables import ItemTable
from com.l2jserver.gameserver.network.serverpackets import ExShowScreenMessage
from com.l2jserver.gameserver.model import L2CharPosition

class MyInstanceWorld(InstanceWorld):
	def __init__(self):
		InstanceWorld.__init__(self)
		self.stage = 0
		self.step = 0
		self.wave1killed = 0
		self.flagInstance = []
		self.bossInstance = None
		self.runningInstance = None
		self.runningIndex = 0

class Quest(JQuest):
	"""
	�ƥ��`�ɶ� 60����
	�i�J�� ��1�����ɶ� �ǳ�
	1�����L�� ��ߤl.. �ܦh�ߤl
	��X�ߤl�� 1���� �ߤl�|�D�ʥ����a
	�� 20���ߤl �|�ͥX �Ⱖ �ݭn�O�@���Ǫ�. �Y�O�@�Ǫ����` �ƥ����ѵ���
	��X�O�@�ǫ� �O�@�Ƿ|�����a.. �ߤl�|���O�@��
	�Y���ߤl�h�� 20��.. �C���@���ߤl �|�b�H���I�ͥX�@���j�� �����a.. 
	���F�O�@�ǥ~ ��Ҧ��� ����.. BOSS ��X��. �O�@�Ǯ���
	�� BOSS �� �X�{ ���} NPC
	���~���� �_�u �^�� �i�A���i�J�ۦP�ƥ� �~��D�� ���t���D��
	�p�G�ƥ����� �� ���\ ����A���i�J�ۦP�ƥ�
	"""
	qID = -1
	qn = "MyCustomBoss"
	qDesc = "custom"
	
	InstanceTemplateId = 99999
	InstanceReenterTime = 1000 * 60 * 15 #�i����}�l�p��h�[ �~�i�H�A���D�Էs�ƥ� (15������)
	
	NPCID = 100 #�i�J�ƥ� NPC
	instanceTime = 1000 * 60 * 60 # �ƥ��`�ɶ�, ��� ms �ȩw 60 ����
	timetos1s0 = 1000 * 60 * 1 # �i�J�ƥ��� �� 1 �����ǳƮɶ�
	timetos1s2 = 1000 * 60 * 1 # �ͥX�ߤl��h�[ �D�ʧ������a �w�] 1 ����
	#ejectLoc = [82698, 148638, -3468] #�h�X/�^�� ��m (�_��)
	ejectLoc = [86655, -19739, -1944] #�h�X/�^�� ��m (�s�髰��~)
	entryLoc = (82995, -16210, -1750) #�ƥ��ǰe�� ��m (�s�髰��)
	bossid = 29195 #BOSS ID
	wave1mobid = 157 #�Ĥ@�i ��ߤl
	killcounttos2s0 = 20 #���h�ְ��ߤl �i�J�U�@���q
	killcountspawnstrongmob = 20 #���h�ְ��ߤl �� �C���@���ߤl �ͤ@���j��
	wave2flagid = 21182 #���a�O�@�Ǫ� ID ���঺�`
	wave2mobid = 23151 #�ĤG�i�Ǫ� ID
	#�ĤG�i ����H����m �i�W�[ ���
	wave2mobspawnloc = [
		[81499,-15130,-1830]
		,[83197,-15298,-1845]
		,[84638,-16244,-1830]
		,[84722,-17496,-1855]
		,[82931,-17144,-1842]
		,[81032,-16456,-1830]
		,[82507,-16214,-1893]
	]
	
	runningR = 800
	runningStep = 36
	
	require_item_id = 57 #�i�J�һݹD�� ���� ID 57
	require_item_name = ItemTable.getInstance().getTemplate(require_item_id).getName()
	require_item_count = 100 #�i�J�һݹD�� �ƶq 100
	
	htm_header = """<html><title>�ۭq�ƥ�</title><body>"""
	htm_footer = """</body></html>"""
	htm_go = """<a action="bypass -h Quest %s go">�D�԰ƥ�</a>""" % qn
	htm_reentry = """<a action="bypass -h Quest %s reentry">�~��D�԰ƥ�</a>""" % qn
	htm_exit = """<a action="bypass -h Quest %s exit">���}�ƥ�</a>""" % qn
	htm_not_allow = """����i�J. <BR>���ݶ���, �p���p�x �����p�x�� �I���i�J<br>�Ҧ����� ���ݦb 2000���d��"""
	htm_not_allow_member = """����i�J �H�U�������ŦX�ݨD<br>"""
	
	def __init__(self, id = qID, name = qn, descr = qDesc):
		self.qID, self.qn, self.qDesc = id, name, descr
		JQuest.__init__(self, id, name, descr)
		self.addStartNpc(self.NPCID)
		self.addFirstTalkId(self.NPCID)
		self.addTalkId(self.NPCID)
		
		self.addKillId(self.wave1mobid)
		self.addKillId(self.wave2flagid)
		self.addKillId(self.bossid)
		print "%s loaded" % self.qn
		
	def onKill(self, npc, player, isPet):
		world = self.getWorld(npc)
		if not isinstance (world, MyInstanceWorld):
			return
		if npc.getNpcId() == self.wave1mobid:
			world.wave1killed += 1
			if world.wave1killed >= self.killcountspawnstrongmob:
				x, y, z = self.wave2mobspawnloc[Rnd.get(0,len(self.wave2mobspawnloc)-1)]
				x, y, z = self.getRandomXYZ(x, y, z, 100)
				n = self.spawnNpc(self.wave2mobid, x, y, z, 0, world.instanceId)
				p = self.getRandomPlayer(world)
				self.addHate(world, n, p)
		if npc.getNpcId() == self.bossid:
			self.broadcastMessage(world.instanceId, "%s �����F %s �ƥ����\" % (player.getName(), npc.getName()))
			self.broadcastScreenMessage(world.instanceId, "�ƥ����\")
			InstanceManager.getInstance().getInstance(world.instanceId).setDuration(1000*60*5)
			x, y, z = self.entryLoc
			self.spawnNpc(self.NPCID, x, y, z, 0, world.instanceId)
			world.stage, world.step = 4, 0
		
	def onAdvEvent(self, event, npc, player):
		def getWorldFromInstanceId():
			try:
				instanceid = int(event.split()[1])
			except:
				print "invaild instance id %s" % event
				return None
			world = self.getWorld(instanceId = instanceid)
			if not world:
				print "Instance disappear %d" % instanceid
				return None
			return world

		if event.startswith("flowControl "):
			try:
				instanceid = int(event.split()[1])
			except:
				print "flowControl error %s" % event
				return
			world = self.getWorld(instanceId = instanceid)
			if not world:
				self.cancelQuestTimer("flowControl %d" % instanceid, None, None)
				print "�ƥ��w���� %d" % instanceid
				return
			i = InstanceManager.getInstance().getInstance(world.instanceId) 
			for pid in i.getPlayers().toArray():
				p = L2World.getInstance().getPlayer(pid)
				if p and p.getInstanceId() == world.instanceId:
					pass
				else:
					i.ejectPlayer(pid)
					i.removePlayer(pid)
			if i.getPlayers().isEmpty():
				print "�ƥ��S�����a %d" % world.instanceId
				self.cancelQuestTimer("flowControl %d" % instanceid, None, None)
				return
			return self.flowControl(world)
			
		if event == 'reentry':
			st = player.getQuestState(self.qn)
			instanceId = st.getInt('instanceId')
			self.teleport(player, instanceId)
			self.startQuestTimer("flowControl %d" % instanceId, 1000, None, None, True)
			
		if event == 'go':
			members = [player]
			if player.getParty():
				if player.getParty().getCommandChannel():
					if player.getParty().getCommandChannel().getLeader().getObjectId() != player.getObjectId():
						return self.htm_header + self.htm_not_allow + self.htm_footer
					members = player.getParty().getCommandChannel().getMembers()
				else:
					if player.getParty().getLeader().getObjectId() != player.getObjectId():
						return self.htm_header + self.htm_not_allow + self.htm_footer
					members = player.getParty().getMembers()
			#�˴��Ҧ������i�J�ݨD
			r = ""
			for m in [x for x in members if not self.checkAllow(player, x)]:
				r += "%s<br1>" % m.getName()
			if len(r):
				return self.htm_header + self.htm_not_allow_member + r + self.htm_footer
			#�Ыذƥ�
			im = InstanceManager.getInstance()
			instanceid = im.createDynamicInstance(None)
			if instanceid:
				instance = im.getInstance(instanceid)
				world = MyInstanceWorld()
				world.instanceId = instanceid
				im.addWorld(world)
				instance.setDuration(self.instanceTime)
				instance.setEmptyDestroyTime(1000 * 60 * 1)
				instance.setSpawnLoc(self.ejectLoc)
				instance.setName("%s %s" % (self.qn, player.getName()))
				for p in members:
					self.takeItems(p, self.require_item_id, self.require_item_count)
					pid = p.getObjectId()
					world.allowed.add(pid)
					InstanceManager.getInstance().setInstanceTime(pid, self.InstanceTemplateId, System.currentTimeMillis() + self.InstanceReenterTime)
					self.teleport(p, instanceid)
				self.broadcastScreenMessage(world.instanceId, "�ǳ�")
				world.stage, world.step = 0, 1
				#world.stage, world.step = 3, 0
				self.startQuestTimer("flowControl %d" % world.instanceId, 1000, None, None, True)
				self.broadcastTimer(world.instanceId, self.timetos1s0 / 1000, "�ǳƮɶ�")
				self.startQuestTimer("s1s0 %d" % world.instanceId, self.timetos1s0, None, None, False)
				print "%s �Ыذƥ� ID %d" % (player.getName(), world.instanceId)
			else:
				print "%s Error:can not create dynamic instance" % self.qn
			return
			
		#��ߤl
		if event.startswith('s1s0 '):
			world = getWorldFromInstanceId()
			if not world:
				return
			if world.stage == 0 and world.step == 1:
				world.stage, world.step = 1, 0
				self.broadcastScreenMessage(world.instanceId, "�Ĥ@���q")
				cx, cy, cz = self.entryLoc
				for r,s in [(500,10), (900,20), (1300,30)]:
					for x, y in self.plotCircle(cx, cy, r, s):
						npc = self.spawnNpc(self.wave1mobid, x, y, -1700, 0, world.instanceId)
				self.startQuestTimer("s1s2 %d" % world.instanceId, self.timetos1s2, None, None, False)
			return
			
		#�ߤl�D�ʧ���
		if event.startswith('s1s2 '):
			world = getWorldFromInstanceId()
			if not world:
				return
			if world.stage == 1 and world.step == 0:
				world.stage, world.step = 1, 2
				self.broadcastScreenMessage(world.instanceId, "�S�̭� �W��")
			return

		#��O�@��
		#if event.startswith('s2s0 '):
		#	world = getWorldFromInstanceId()
		#	if not world:
		#		return
		#	if world.stage == 1 and world.step == 3:
		#		world.stage, world.step = 2, 0
		#		world.flagInstance += [self.spawnNpc(self.wave2flagid, 84516, -16753, -1829, 0, world.instanceId)]
		#		world.flagInstance += [self.spawnNpc(self.wave2flagid, 81651, -15373, -1832, 0, world.instanceId)]
		#	return
		if event == 'exit':
			world = self.getWorld(player)
			if world:
				self.playerExit(world.instanceId, player.getObjectId())
				
	def onFirstTalk(self, npc, player):
		st = player.getQuestState(self.qn)
		if not st:
			st = self.newQuestState(player)
			st.setState(State.STARTED)
		lastInstanceId = st.getInt('instanceId') or None
		world = self.getWorld(player)
		if world:
			return self.htm_header + self.htm_exit + self.htm_footer
		if lastInstanceId:
			world = InstanceManager.getInstance().getWorld(lastInstanceId)
			if world and world.stage in [0,1,2,3] and world.allowed.contains(player.getObjectId()):
				return self.htm_header + self.htm_reentry + self.htm_footer
		return self.htm_header + self.htm_go + self.htm_footer

	def checkAllow(self, player, target):
		message = ""
		if not Util.checkIfInRange(2000, player, target, False):
			message = "%s ���b�����d�� 2000 ��줺" % target.getName()
		if not target.getLevel() >= 80: 
			message = "%s ���Ť���" % target.getName()
		if self.getQuestItemsCount(target, self.require_item_id) < self.require_item_count:
			message = "%s �һݹD�㤣�� �ݭn %s %d ��" % (target.getName(), self.require_item_name, self.require_item_count)
		l, c = InstanceManager.getInstance().getInstanceTime(target.getObjectId(), self.InstanceTemplateId), System.currentTimeMillis()
		if l > c:
			message = "%s �ƥ��ɶ����� %d ���i��" % (target.getName(), (l - c)/1000)
		if len(message) > 0:
			player.sendMessage(message)
			if player.getObjectId() != target.getObjectId():
				target.sendMessage(message)
			return False
		return True
		
	def plotCircle(self, x, y, r, steps):
		ret = []
		anginc = math.pi * 2 / steps
		ang = 0
		for step in xrange(steps):
			ang += anginc
			xx = r * math.cos(ang)
			yy = r * math.sin(ang)
			ret += [(int(xx + x), int(yy + y))]
		return ret

	def getRandomXYZ(self, x, y, z, offset):
		return x+Rnd.get(-offset, offset), y+Rnd.get(-offset, offset), z
		
	def getRandomPlayer(self, world):
		allplayers = self.getAllInstancePlayers(world.instanceId)
		if len(allplayers):
			return allplayers[Rnd.get(0, len(allplayers)-1)]
		return None
		#return L2World.getInstance().getPlayer(world.allowed.get(Rnd.get(0, world.allowed.size()-1)))

	def getRandomFlag(self, world):
		return world.flagInstance[Rnd.get(0,len(world.flagInstance)-1)]

	def getWorld(self, player = None, instanceId = None):
		if player and isinstance(player, L2Object):
			return InstanceManager.getInstance().getWorld(player.getInstanceId())
			#return InstanceManager.getInstance().getPlayerWorld(player)
		if instanceId:
			return InstanceManager.getInstance().getWorld(instanceId)
		return None
	
	def teleport(self, player, instanceId):
		st = player.getQuestState(self.qn)
		if not st:
			st = self.newQuestState(player)
			st.setState(State.STARTED)
		st.set('instanceId', str(instanceId))
		player.getAI().setIntention(CtrlIntention.AI_INTENTION_IDLE)
		player.setInstanceId(instanceId);
		player.teleToLocation(*self.entryLoc);
		if player.getPet():
			self.teleport(player.getPet(), instanceId)

	def broadcastScreenMessage(self, instanceId, message, duration = 10000):
		Broadcast.toPlayersInInstance(ExShowScreenMessage(message, duration), instanceId)
			
	def showScreenMessage(self, player, message, duration = 10000):
		player.sendPacket(ExShowScreenMessage(message, duration))
			
	def broadcastMessage(self, instanceId, text):
		Broadcast.toPlayersInInstance(SystemMessage.sendString(text), instanceId)
	
	def broadcastTimer(self, instanceId, time, text):
		for objId in InstanceManager.getInstance().getWorld(instanceId).allowed:
			p = L2World.getInstance().getPlayer(objId)
			p.sendPacket(ExSendUIEvent(p, False, False, time, 0, text))
			#Broadcast.toPlayersInInstance(ExSendUIEvent(), instanceId)
			
	def spawnNpc(self, npcId, x, y, z, heading, instId):
		npcTemplate = NpcTable.getInstance().getTemplate(npcId)
		inst = InstanceManager.getInstance().getInstance(instId)
		try:
			npcSpawn = L2Spawn(npcTemplate)
			npcSpawn.setLocx(x)
			npcSpawn.setLocy(y)
			npcSpawn.setLocz(z)
			#npcSpawn.setHeading(heading)
			npcSpawn.setAmount(1)
			npcSpawn.setInstanceId(instId)
			SpawnTable.getInstance().addNewSpawn(npcSpawn, False)
			npc = npcSpawn.doSpawn()
			#npc.setOnKillDelay(0)
			#npc.setRunning()
			return npc
		except:
			print "spawnNPC error"
			
	def getAllVisibleNpcs(self, world):
		npcs = []
		if not isinstance (world, MyInstanceWorld):
			return npcs
		i = InstanceManager.getInstance().getInstance(world.instanceId)
		if not i:
			return npcs
		for n in i.getNpcs():
			if L2World.getInstance().findObject(n.getObjectId()):
				npcs += [n]
		return npcs
		
	def addHate(self, world, npc, target):
		try:
			if target and L2World.getInstance().findObject(target.getObjectId()):
				npc.setTarget(target)
				#npc.getKnownList().addKnownObject(target)
				npc.addDamageHate(target, 0, Rnd.get(100,999))
				npc.getAI().setIntention(CtrlIntention.AI_INTENTION_ATTACK)
		except:
			pass

	def getAllInstancePlayers(self, instanceId):
		p = []
		i = InstanceManager.getInstance().getInstance(instanceId) 
		if i:
			for pid in i.getPlayers().toArray():
				player = L2World.getInstance().getPlayer(pid)
				if player:
					p += [player]
		return p

	def playerExit(self, instanceId, playerId):
		i = InstanceManager.getInstance().getInstance(instanceId) 
		if i:
			i.ejectPlayer(playerId)
			i.removePlayer(playerId)
		
	def removeAllPlayers(self, instanceId):
		i = InstanceManager.getInstance().getInstance(instanceId) 
		if i:
			for pid in i.getPlayers().toArray():
				i.ejectPlayer(pid)
				i.removePlayer(pid)
					
	def flowControl(self, world):
		if not isinstance (world, MyInstanceWorld):
			return
		if world.stage == 1:
			if world.step == 2:
				allnpc = self.getAllVisibleNpcs(world)
				for n in allnpc:
					p = self.getRandomPlayer(world)
					self.addHate(world, n, p)
			if world.wave1killed >= self.killcounttos2s0:
				world.stage, world.step = 2, 0
				world.flagInstance += [self.spawnNpc(self.wave2flagid, 84516, -16753, -1829, 0, world.instanceId)]
				world.flagInstance += [self.spawnNpc(self.wave2flagid, 81651, -15373, -1832, 0, world.instanceId)]
				#self.startQuestTimer("s2s0 %d" % world.instanceId, 1000 * 5, None, None, False)
				self.broadcastScreenMessage(world.instanceId, "�ЫO�@ %s ���n�Q��" % world.flagInstance[0].getName())

			return

		if world.stage == 2:
			if world.step == 0:
				allnpc = self.getAllVisibleNpcs(world)
				for n in allnpc:
					p = None
					if n.getNpcId() == self.wave1mobid:
						p = self.getRandomFlag(world)
					if n.getNpcId() in [self.wave2mobid, self.wave2flagid]:
						p = self.getRandomPlayer(world)
					if p:
						self.addHate(world, n, p)
				for n in world.flagInstance:
					if not L2World.getInstance().findObject(n.getObjectId()):
						self.broadcastMessage(world.instanceId, "%s ���` �ƥ�����" % n.getName())
						self.broadcastScreenMessage(world.instanceId, "%s ���` �ƥ�����" % n.getName())
						world.allowed.clear()
						self.removeAllPlayers(world.instanceId)
				if len(allnpc) == 2:
					world.stage, world.step = 3, 0
			return
		
		if world.stage == 3:
			if world.step == 0:
				for n in world.flagInstance:
					if n:
						i = InstanceManager.getInstance().getInstance(world.instanceId)
						if i:
							i.removeNpc(n)
							n.deleteMe()
				x, y, z = self.entryLoc
				world.bossInstance = self.spawnNpc(self.bossid, x, y, z, 0, world.instanceId)
				self.broadcastScreenMessage(world.instanceId, "�̫ᶥ�q")
				world.stage, world.step = 3, 1
			if world.step == 1:
				b = world.bossInstance
				if b.getCurrentHp() / b.getMaxHp() < 0.9:
					world.stage, world.step = 3, 2
					x, y, z = self.entryLoc
					world.runningInstance = self.spawnNpc(29191, x, y, z, 0, world.instanceId)
					world.runningInstance.setRunning()
					world.runningInstance.setIsInvul(True)
			if world.step == 2:
				x, y, z = world.bossInstance.getX(), world.bossInstance.getY(), world.bossInstance.getZ()
				r = self.plotCircle(x, y, self.runningR, self.runningStep)
				if r and len(r):
					world.runningIndex += 1
					if world.runningIndex >= self.runningStep:
						world.runningIndex = 0
					x, y = r[world.runningIndex]
					world.runningInstance.getAI().setIntention(CtrlIntention.AI_INTENTION_MOVE_TO, L2CharPosition(x, y, z, 0))

		if world.stage == 4:
			if world.step == 0:
				i = InstanceManager.getInstance().getInstance(world.instanceId)
				if i:
					i.removeNpc(world.runningInstance)
					world.runningInstance.deleteMe()
					
Quest()	

