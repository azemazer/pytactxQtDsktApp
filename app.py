import sys, copy, couleurs, melodies
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import pyqtSlot, QTimer, Qt
import j2l.pytactx.agent as pytactx
import auto

from ui_AgentControllerTF2_Fullapp import Ui_MainWindow


"""


---------------------
|                   |
|   HERE STARTS     |
|   LE CODE         |
|   OF LE UI        |
|                   |
|-------------------|



"""
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow): #Main window of the app
    

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Timer defragmenting the loop to simulate a While True condition
        self.timer = QTimer()
        self.timer.setTimerType(Qt.PreciseTimer)
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.onTimerUpdate)


        self.ui = uic.loadUi("AgentControllerTF2_FullApp.ui", self) # Loads the UI
        self.ui.ControlUI.setCurrentIndex(0) # Selects the correct tab on startup
        self.automode = False # Activates or deactivates autopilt

        # UI Sprite rotations
        self.imageRight = None
        self.imageLeft = None
        self.imageUp = None
        self.imageDown = None
        
        # Parameters saved in order to compare old info to new info to detect changes
        self.vieuxvie = None
        self.vieuxscore = None
        self.vieuxtirer = None

        # Connection informations
        self.arena = ""
        self.nickname = ""
        self.password = ""

        # Agent
        self.agent = None
        
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

    def onButtonRelease(self): # When "GO" is pressed
        

        print("GOING TO ARENA: ", self.arena, " WITH NICKNAME: ", self.nickname, "AND PASSWORD: ", self.password, "...")

        self.timer.start() # Starts the timer for the while True loop simulation

        # Creates the agent
        self.agent = pytactx.AgentFr(nom=self.nickname,
                        arene=self.arena,
                        username="demo",
                        password=self.password,
                        url="mqtt.jusdeliens.com",
                        verbosite=3)
        
        auto.setAgent(self.agent) # Mandatory for the autopilot to work
        
        # UI Sprite setting
        self.imageRight = QPixmap("imageResource/heavy.png")
        self.ui.agentView.setPixmap(self.imageRight)
        self.imageDown = self.imageRight.transformed(QTransform().rotate(90))
        self.imageLeft = self.imageRight.transformed(QTransform().rotate(180))
        self.imageUp = self.imageRight.transformed(QTransform().rotate(270))

        self.ui.ControlUI.setCurrentIndex(1)

        
    # TAB 2: AGENT CONTROL

    def onUpArrowPressed(self):
        

        self.agent.deplacer(0,-1)
        self.agent.orienter(1)
                
    def onDownArrowPressed(self):
        

        self.agent.deplacer(0,1)
        self.agent.orienter(3)
                
    def onRightArrowPressed(self):
        

        self.agent.deplacer(1,0)
        self.agent.orienter(0)
                
    def onLeftArrowPressed(self):
        

        self.agent.deplacer(-1,0)
        self.agent.orienter(2)

    def onShootToggled(self, shooting):
        

        if shooting == True:
            self.agent.tirer(True)
        else:
            self.agent.tirer(False)

    def onAutoToggled(self, auto):
        if auto == 1:
            print("AUTO MODE ACTIVATED.")
            self.automode = True
        else:
            print("AUTO MODE DEACTIVATED.")
            self.automode = False
                
    def onTimerUpdate(self):

        if ( self.agent != None ):

            self.vieuxvie = self.agent.vie
            self.vieuxscore = self.agent.score
            self.agent.actualiser()

            # Melodies and colours for IRL robots. Note: for now, the colours are not working.

            if self.agent.vie != self.vieuxvie:
                if self.vieuxvie == 0: #Spawn
                    self.agent.robot.playMelody(melodies.onSpawn)
                    # self.agent.robot.setLedAnimation(couleurs.vert)
                    print("Spawn")
                elif self.agent.vie == 0: #Mort
                    self.agent.robot.playMelody(melodies.onDie)
                    # self.agent.robot.setLedAnimation(couleurs.noir)
                    print("Mort")
                else: #Touche
                    self.agent.robot.playMelody(melodies.onHurt)
                    # self.agent.robot.setLedAnimation(couleurs.orange)
                    print("Touche")

            if self.agent.score != self.vieuxscore: #Frag
               self.agent.robot.playMelody(melodies.onKill)
            #    self.agent.robot.setLedAnimation(couleurs.bleu)
               print("Frag")
                   

            # --- UI ---

            # Progress bars live visualization

            # Life
            if (self.agent.vie > self.ui.healthProgressBar.maximum() ):
                self.ui.healthProgressBar.setMaximum(self.agent.vie)
            self.ui.healthProgressBar.setValue(self.agent.vie)

            # Ammo
            if (self.agent.munitions > self.ui.ammoProgressBar.maximum() ):
                self.ui.ammoProgressBar.setMaximum(self.agent.munitions)
            self.ui.ammoProgressBar.setValue(self.agent.munitions)

            # Score
            scoreStr = "Score: " + str(self.agent.score)
            self.ui.label_5.setText(scoreStr)

            # Agent visualization

            match self.agent.orientation:
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
