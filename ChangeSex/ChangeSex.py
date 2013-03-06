from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

class ChangeSex(JQuest):
	qID = -1
	qn = "ChangeSex"
	qDesc = "custom"
	NPC = 100

	def __init__(self, id = qID, name = qn, descr = qDesc):
		self.qID, self.qn, self.qDesc = id, name, descr
		JQuest.__init__(self, id, name, descr)
		self.addFirstTalkId(self.NPC)
		self.addStartNpc(self.NPC)
		self.addTalkId(self.NPC)

	def onAdvEvent(self, event, npc, player):
		pa = player.getAppearance()
		qs = player.getQuestState(self.qn)
		if qs.getQuestItemsCount(3470) >= 1000 and qs.getQuestItemsCount(57) >= 1000:
			qs.takeItems(3470, 1000)
			qs.takeItems(57, 1000)
			pa.setSex(not pa.getSex())
			player.broadcastUserInfo()
			player.sendMessage("�ܩʦ��\�I")
		else:
			player.sendMessage("�D�㤣���I")
		return ""

	def onFirstTalk(self, npc, player):
		return '<html><title>�ܩ�</title><body>�ܩʻݭn���� 1000 �� ���� 1000<BR><a action="bypass -h Quest %s 1">�I���ܩ�</a></body></html>' % self.qn

ChangeSex(-1, "ChangeSex", "custom")
print "�۩w�q�ܩʮv�Ұ�."