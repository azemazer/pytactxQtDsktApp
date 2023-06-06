import sys
from PyQt5 import QtWidgets, uic

from ui_AgentControllerTF2_Homepage import Ui_MainWindow


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
        print("GOING TO ARENA: ", self.arena, " WITH NICKNAME: ", self.nickname, "AND PASSWORD: ", self.password)
        self.close()


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()