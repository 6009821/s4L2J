from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest
from com.l2jserver.gameserver.util import Util 

class Quest(JQuest):
	qID = -1 #�}�� ID, �ۭq�}�� �i�� -1
	qn = "partyDrop" #�}���W��, ���୫�дN�i�H
	qDesc = "custom" #�}������ / �M��}���� HTM ��m�ɥ�

	MOBID = 29068 #�o�ӬO�a�s�� ID
	itemid = 1 #�o�ӬO �����~�� ID ���L �ȮɥΤF "hardcode" �ҥH �S�@�Ϊ�
	itemcount = 1 #�o�ӬO �����~���ƶq ���L �ȮɥΤF "hardcode" �ҥH �S�@�Ϊ�

	def __init__(self, id = qID, name = qn, descr = qDesc):
		self.qID, self.qn, self.qDesc = id, name, descr #�]�w qid, qn �� qdesc (�p�G�b�}���̤U�H  Quest(-1, "abc", "custom") �Φ�I�s)
		JQuest.__init__(self, id, name, descr) #�I�s��
		self.addKillId(self.MOBID) #�[�J ���@�өǪ��� ID �Q���|�I�s �o�̪� onKill
		print "%s loaded" % self.qn #��l�Ƨ��� GS ��ܰT��

	def onKill(self, npc, player, isPet): #��Ǫ��Q���� �|�Q�I�s.. player �O���M���Ǫ����a
		party = player.getParty() #��o���M���a������
		if party: #�p�G���ն����p
			members = [] #��l�� �����ܼ�
			cc = party.getCommandChannel() #���o �p�x (�p�G��)
			if cc: #���p�x
				members = cc.getMembers() #���o�p�x�Ҧ�����
			else: #�S���p�x
				members = party.getMembers() #���o�@�붤��Ҧ�����
			for m in members: #�b members �ܼƨ��X�C�Ӧ��� M
				if Util.checkIfInRange(2000, player, m, False): #�p�� ���� M �� ���M���a���Z�� �O�_�b 2000 ���H��
					#m.addItem(self.qn, itemid, itemcount, null, True)
					m.addItem(self.qn, 1, 1, None, True) #�����W�[���~�� M �������I�]��.. ��1�ӰѼƬO�ѵo���ѦҦW��, �ĤG�ѼƬO ���~ ID,  �ĤT �ƶq, �Ѧ�, �O�_�o�T��
					m.addItem(self.qn, 2, 1, None, True) #�C�W�[�@�� �h���@�ت��~.. �o�� �� ����
					m.addItem(self.qn, 3, 1, None, True)
					m.addItem(self.qn, 32272, 1, None, True)
					m.addItem(self.qn, 35704, 1, None, True)
					m.addItem(self.qn, 18549, 1, None, True)
				else: #�Z�����b 2000 ���H��
					player.sendMessage("���b�d�� �����S�O���y") #�V���a�o�X�T��
		else: #�p�G�S���ն����p
			player.sendMessage("�S������ �����S�O���y") #�V���a�o�X�T��

Quest() #�I�s Quest �� __init__