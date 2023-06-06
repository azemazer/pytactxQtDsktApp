import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget, 
    QHBoxLayout
)
from PyQt5.QtGui import QPalette, QColor

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HEAVY WEAPONS GUY")

        layoutH = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()

        widgets1 = [
            QCheckBox,
            QPushButton,
            QLabel
        ]
        widgets2 = [
            QPushButton,
            QProgressBar,
            QProgressBar,
            QPushButton
        ]

        for w in widgets1:
            layout1.addWidget(w())

        layoutH.addLayout( layout1 )

        for w in widgets2:
            layout2.addWidget(w())

        layoutH.addLayout( layout2 )

        layoutH.setContentsMargins(20,20,20,20)
        layoutH.setSpacing(40)

        layout1.setSpacing(40)
        layout2.setSpacing(40)

        widget = QWidget()
        widget.setLayout(layoutH)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()