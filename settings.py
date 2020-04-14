from stylesheets import *


class Settings(QWidget):
    toggle = 0

    def __init__(self, x, y):
        super(Settings, self).__init__()
        self.__class__.toggle %= 2
        self.__class__.toggle += 1

        self.x = x
        self.y = y
        self.my_width = 250
        self.my_height = 370
        self.setFixedSize(250, 370)

        self.languages = QtWidgets.QGroupBox()
        self.radio_btn1 = QtWidgets.QRadioButton("Deutsch")
        self.radio_btn2 = QtWidgets.QRadioButton("English")
        self.flag = QLabel()

        self.customization = QtWidgets.QGroupBox()
        self.btn = QtWidgets.QPushButton("Browse")

        self.miscellaneous = QtWidgets.QGroupBox()

        self.apply_btn = QtWidgets.QPushButton("Apply")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

        self.initUI()
        self.button_handler()

    def initUI(self):
        self.setWindowTitle("Settings")
        self.setWindowIcon(QtGui.QIcon("./data/Settings.png"))
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setGeometry(self.x, self.y, self.my_width, self.my_height)

        self.flag.setStyleSheet("border-radius: 25px")
        #self.flag.setFixedSize(80, 40)
        pix = QtGui.QPixmap("./data/Deutschland_flag.png")
        self.flag.setPixmap(pix)
        self.flag.setScaledContents(True)

        self.createLayout()

    def button_handler(self):
        self.cancel_btn.clicked.connect(self.close)

    def createLayout(self):
        main_layout = QGridLayout()
        main_layout.addWidget(self.languages, 0, 0, 1, 2)
        main_layout.addWidget(self.customization, 1, 0, 1, 2)
        main_layout.addWidget(self.miscellaneous, 2, 0, 1, 2)
        main_layout.addWidget(self.apply_btn, 3, 0, 1, 1)
        main_layout.addWidget(self.cancel_btn, 3, 1, 1, 1)

        languages_layout = QGridLayout()
        languages_layout.addWidget(self.flag, 0,0)
        languages_layout.addWidget(self.radio_btn1, 1, 0)
        languages_layout.addWidget(self.radio_btn2, 1, 1)

        customization_layout = QHBoxLayout()
        customization_layout.addWidget(self.btn)

        self.customization.setLayout(customization_layout)
        self.languages.setLayout(languages_layout)
        self.setLayout(main_layout)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.__class__.toggle += 1
        self.close()
