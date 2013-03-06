import sys
from com.l2jserver.gameserver.model.quest import State
from com.l2jserver.gameserver.model.quest import QuestState
from com.l2jserver.gameserver.model.quest.jython import QuestJython as JQuest

from com.l2jserver.gameserver import Announcements

from javax.swing import *
from java.awt import *

class Quest(JQuest):
    qID = -1
    qn = "AnnoGUI"
    qDesc = "custom"

    jmessage = None
        
    def __init__(self, id = qID, name = qn, desc = qDesc):
        JQuest.__init__(self, id, name, desc)
        self.buildGUI()
        print "Init:" + self.qn + " loaded"

    def buildGUI(self):
        frame = JFrame()
        self.jmessage = JTextField('��J�Y�ɤ��i',25)
        container = frame.getContentPane()
        container.setLayout(FlowLayout());
        container.add(self.jmessage)
        container.add(JButton('�e�X���i',actionPerformed = self.send_jmessage))
        frame.pack()
        frame.setVisible(True)
        
    def send_jmessage(self, event):
        Announcements.getInstance().announceToAll(self.jmessage.getText())
        print self.jmessage.getText()
        
Quest()
