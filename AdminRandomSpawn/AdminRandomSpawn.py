import sys
from com.l2jserver.gameserver.handler import AdminCommandHandler
from com.l2jserver.gameserver.handler import IAdminCommandHandler
from java.util import Random
from com.l2jserver.gameserver.datatables import NpcTable
from com.l2jserver.gameserver.datatables import SpawnTable
from com.l2jserver.gameserver.model import L2Spawn
from com.l2jserver import Config
from com.l2jserver import L2DatabaseFactory

class AdminRandomSpawn(IAdminCommandHandler):
	"""
	//random_spawn ��ID �ƶq �d�� �ä[��
	�ƶq �d�� �ä[�� �p����J �|�ϥιw�]��
	�ƶq �w�]�Ȭ� 1-4 �H����
	�d�� �w�]�Ȭ� 400
	�ä[�� �w�]�Ȭ� �Ȯ� �i��J 1 �� true
	�Ҧp //random_spawn 20003 10 500 1 ���� ���� �����L 10�� �d�� 500 �ä[��
	�Ҧp //random_spawn 20481 ���� ���� ���� 1-4�� �d�� 400 �Ȯɩ�
	"""

	commands = ["admin_random_spawn"]

	def db_exec(self, sql):
		con, statement = None, None
		try:
			con = L2DatabaseFactory.getInstance().getConnection()
			statement = con.prepareStatement(sql)
			statement.execute()
		except:
			pass
		if statement:
			statement.close()
		if con:
			L2DatabaseFactory.close(con)

	
	def useAdminCommand(self, command, player):
		mobid = 0
		max_mob = Random().nextInt(3) + 1
		dist = 400
		perm = False
		param = command.split()

		try:
			mobid = int(param[1])
			max_mob = int(param[2])
			dist = int(param[3])
			perm = param[4].lower() == "true" or param[4] == "1"
		except:
			pass

		def my_spawn(player, mobid, dist, perm):
			mobt = NpcTable.getInstance().getTemplate(mobid)
			if not mobt: return
			spawn = L2Spawn(mobt)
			spawn.setInstanceId(0)
			if Config.SAVE_GMSPAWN_ON_CUSTOM:
				spawn.setCustom(True)
			spawn.setLocx(player.getX()-dist+Random().nextInt(dist*2))
			spawn.setLocy(player.getY()-dist+Random().nextInt(dist*2))
			spawn.setLocz(player.getZ())
			spawn.setHeading(player.getHeading())
			spawn.setAmount(1);
			spawn.setRespawnDelay(0)
			if perm:
				SpawnTable.getInstance().addNewSpawn(spawn, True)
				spawn.init()
			else:
				spawn.stopRespawn()
				spawn.doSpawn()
		if mobid:
			for mob in xrange(max_mob):
				my_spawn(player, mobid, dist, perm)
			
	def getAdminCommandList(self):
		return self.commands
		
	def __init__(self):
		self.db_exec("INSERT INTO `admin_command_access_rights` (`adminCommand`) VALUES ('admin_random_spawn');")
		AdminCommandHandler.getInstance().registerHandler(self)
		print "AdminRandomSpawn registered"

AdminRandomSpawn()