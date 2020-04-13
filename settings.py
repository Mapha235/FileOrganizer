from stylesheets import *


class Settings(QWidget):
    def __init__(self, x, y):
        super(Settings, self).__init__()
        self.x = x
        self.y = y
        self.my_width = 250

        self.my_height = 370
        self.setFixedSize(250, 370)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)


        self.container = QtWidgets.QGroupBox()
        self.radio_button = QtWidgets.QRadioButton("")
        self.button = QtWidgets.QPushButton("Browse")
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Settings")
        self.setWindowIcon(QtGui.QIcon("./data/Settings.png"))
        #self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setGeometry(self.x, self.y, self.my_width, self.my_height)
        self.createBoxLayout()

    def createBoxLayout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.container)

        vbox = QVBoxLayout()
        vbox.addWidget(self.radio_button)
        vbox.addWidget(self.button)

        self.container.setLayout(vbox)
        self.setLayout(layout)


