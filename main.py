import re

from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QHBoxLayout

from app import *
from test import *

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Window"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500

        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.button = QPushButton("Start", self)
        self.button.move(30, 30)
        self.button.clicked.connect(self.doAnimation)

        self.frame = QtWidgets.QPushButton("Donate", self)
        #self.frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.frame.setGeometry(150, 30, 500, 400)

        self.show()

    def doAnimation(self):
        self.anim = QPropertyAnimation(self.frame, b"geometry")
        self.anim.setDuration(1000)
        self.anim.setStartValue(QRect(-1000, 100, 500, 400))
        self.anim.setEndValue(QRect(0, 100, 500, 400))
        self.anim.start()

def donate():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())

def test_loop():
    path = "X:/Dev/python/FileOrganizer/venv/Include"
    found = re.search(r'\A.:/', path).group(0)
    direcories = re.search(r'/(.*?)/', path).group(1)

    print(found)

def test2():
    s = "ABC12DEF3G56HIJ7"
    pattern = re.compile(r'([A-Z]+)([0-9]+)')

    for (letters, numbers) in re.findall(pattern, s):
        print(numbers, '*', letters)

#test2()
#test_loop()
window()
#testSignal()

