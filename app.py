import sys, copy, couleurs, melodies
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import pyqtSlot, QTimer, Qt
import j2l.pytactx.agent as pytactx
import auto

from ui_AgentControllerTF2_Fullapp import Ui_MainWindow

agent = None
"""


---------------------
|                   |
|   HERE STARTS     |
|   LE CODE         |
|   OF THE UI       |
|                   |
|-------------------|



"""
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    global agent

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.timer = QTimer()
        self.timer.setTimerType(Qt.PreciseTimer)
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.onTimerUpdate)
        self.ui = uic.loadUi("AgentControllerTF2_FullApp.ui", self)
        self.automode = False
        self.imageRight = None
        self.imageLeft = None
        self.imageUp = None
        self.imageDown = None
        
        self.vieuxvie = None
        self.vieuxscore = None
        self.vieuxtirer = None

        self.arena = ""
        self.nickname = ""
        self.password = ""
        
        # TAB 1: CONNECTION
    def onArenaTextChanged(self, text):
        print("Arena: ", text)
        self.arena = text
    def onNicknameTextChanged(self, text):
        print("Nickname: ", text)
        self.nickname = text
    def onPasswordTextChanged(self, text):
        print("Password: ", text)
        self.password = text

    def onButtonRelease(self):
        global agent

        print("GOING TO ARENA: ", self.arena, " WITH NICKNAME: ", self.nickname, "AND PASSWORD: ", self.password, "...")

        self.timer.start()
        agent = pytactx.AgentFr(nom=self.nickname,
                        arene=self.arena,
                        username="demo",
                        password=self.password,
                        url="mqtt.jusdeliens.com",
                        verbosite=3)
        
        auto.setAgent(agent)
        
        self.imageRight = QPixmap("imageResource/heavy.png")
        self.ui.agentView.setPixmap(self.imageRight)
        self.imageDown = self.imageRight.transformed(QTransform().rotate(90))
        self.imageLeft = self.imageRight.transformed(QTransform().rotate(180))
        self.imageUp = self.imageRight.transformed(QTransform().rotate(270))

        
    # TAB 2: AGENT CONTROL

    def onUpArrowPressed(self):
        global agent

        agent.deplacer(0,-1)
        agent.orienter(1)
                
    def onDownArrowPressed(self):
        global agent

        agent.deplacer(0,1)
        agent.orienter(3)
                
    def onRightArrowPressed(self):
        global agent

        agent.deplacer(1,0)
        agent.orienter(0)
                
    def onLeftArrowPressed(self):
        global agent

        agent.deplacer(-1,0)
        agent.orienter(2)

    def onShootToggled(self, shooting):
        global agent

        if shooting == True:
            agent.tirer(True)
        else:
            agent.tirer(False)

    def onAutoToggled(self, auto):
        if auto == 1:
            print("AUTO MODE ACTIVATED.")
            self.automode = True
        else:
            print("AUTO MODE DEACTIVATED.")
            self.automode = False
                
    def onTimerUpdate(self):
        global agent
        global agentVoisinsVieux

        if ( agent != None ):

            self.vieuxvie = agent.vie
            self.vieuxscore = agent.score
            agent.actualiser()

            # Melodies et Couleurs

            if agent.vie != self.vieuxvie:
                if self.vieuxvie == 0: #Spawn
                    agent.robot.playMelody(melodies.onSpawn)
                    # agent.robot.setLedAnimation(couleurs.vert)
                    print("Spawn")
                elif agent.vie == 0: #Mort
                    agent.robot.playMelody(melodies.onDie)
                    # agent.robot.setLedAnimation(couleurs.noir)
                    print("Mort")
                else: #Touche
                    agent.robot.playMelody(melodies.onHurt)
                    # agent.robot.setLedAnimation(couleurs.orange)
                    print("Touche")

            if agent.score != self.vieuxscore: #Frag
               agent.robot.playMelody(melodies.onKill)
            #    agent.robot.setLedAnimation(couleurs.bleu)
               print("Frag")
                   

            # --- UI ---

            # Progress bars
            if (agent.vie > self.ui.healthProgressBar.maximum() ):
                self.ui.healthProgressBar.setMaximum(agent.vie)
            self.ui.healthProgressBar.setValue(agent.vie)
            if (agent.munitions > self.ui.ammoProgressBar.maximum() ):
                self.ui.ammoProgressBar.setMaximum(agent.munitions)
            self.ui.ammoProgressBar.setValue(agent.munitions)
            scoreStr = "Score: " + str(agent.score)
            self.ui.label_5.setText(scoreStr)

            # Agent visualization

            match agent.orientation:
               case 0:
                  self.ui.agentView.setPixmap(self.imageRight)
               case 1:
                  self.ui.agentView.setPixmap(self.imageUp)
               case 2:
                  self.ui.agentView.setPixmap(self.imageLeft)
               case 3:
                  self.ui.agentView.setPixmap(self.imageDown)


            # Auto mode
            if self.automode:
                auto.automode()


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
