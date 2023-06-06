import sys
from PyQt5 import QtWidgets, uic
import j2l.pytactx.agent as pytactx

from ui_AgentControllerTF2_Homepage import Ui_MainWindow

agent = None


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.arena = ""
        self.nickname = ""
        self.password = ""
        
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
        agent = pytactx.AgentFrCibleAleatoire(nom=self.nickname,
                        arene=self.arena,
                        username="demo",
                        password=self.password,
                        url="mqtt.jusdeliens.com",
                        verbosite=3)
        while True:
	        agent.actualiser()


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
