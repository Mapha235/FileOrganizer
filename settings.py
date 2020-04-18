from stylesheets import *


class Settings(QWidget):
    toggle = 0
    signal = pyqtSignal(bool)

    def __init__(self, x, y, language_mode: int, color_mode: int):
        super(Settings, self).__init__()
        self.__class__.toggle %= 2
        self.__class__.toggle += 1

        self.x = x
        self.y = y
        self.my_width = 270
        self.my_height = 400
        self.setFixedSize(self.my_width, self.my_height)

        # self.bg = QImage("./data/bg4.jpg")
        # scaled_bg = self.bg.scaled(QSize(self.my_width, self.my_height))
        # palette = QPalette()
        # palette.setBrush(QPalette.Background, QBrush(scaled_bg))
        # self.setPalette(palette)

        self.languages = QtWidgets.QGroupBox("Language")
        self.de = QtWidgets.QRadioButton("Deutsch")
        self.eng = QtWidgets.QRadioButton("Englisch")
        self.apply_btn = QtWidgets.QPushButton("Apply")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

        self.customization = QtWidgets.QGroupBox("Design")
        self.default = QtWidgets.QRadioButton("Default")
        self.dark = QtWidgets.QRadioButton("Dark")
        self.light = QtWidgets.QRadioButton("Light")

        self.bgs = QtWidgets.QGroupBox("Background")
        self.bg_dark = QLabel()
        self.bg_light = QLabel()
        self.radio_dark = QtWidgets.QRadioButton()
        self.radio_light = QtWidgets.QRadioButton()

        self.options = QtWidgets.QGroupBox("Options")
        self.run_in_background = QCheckBox("Run in Background.")
        self.enable_shortcut = QCheckBox("Enable Shortcut. (Ctrl+M)")
        self.auto_replace = QCheckBox("Enable replace existing file in destination\ndirectory.")

        if color_mode == 1:
            self.dark.setChecked(True)
        elif color_mode == 2:
            self.light.setChecked(True)

        if language_mode == 1:
            self.eng.setChecked(True)
        else:
            self.de.setChecked(True)

        self.initUI()
        self.button_handler()

    def initUI(self):
        self.setWindowTitle("Settings")
        self.setWindowIcon(QtGui.QIcon("./data/Settings.png"))
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setGeometry(self.x, self.y, self.my_width, self.my_height)

        # self.languages.setFixedHeight(40)
        # self.customization.setFixedHeight(40)
        # self.bgs.setFixedHeight(120)

        pix_dark = QtGui.QPixmap("./data/tile2.png")
        pix_light = QtGui.QPixmap("./data/tile.png")

        self.bg_dark.setPixmap(pix_dark)
        self.bg_dark.setFixedSize(100, 60)
        self.bg_dark.setScaledContents(True)

        self.bg_light.setPixmap(pix_light)
        self.bg_light.setFixedSize(100, 60)
        self.bg_light.setScaledContents(True)

        self.createLayout()

    def button_handler(self):
        self.cancel_btn.clicked.connect(self.close)
        self.apply_btn.clicked.connect(self.apply)

    def createLayout(self):
        main_layout = QGridLayout()
        main_layout.addWidget(self.languages, 0, 0, 1, 2)
        main_layout.addWidget(self.customization, 1, 0, 1, 2)
        main_layout.addWidget(self.bgs, 2, 0, 1, 2)
        main_layout.addWidget(self.options, 3, 0, 1, 2)
        main_layout.addWidget(self.apply_btn, 4, 0, 1, 1)
        main_layout.addWidget(self.cancel_btn, 4, 1, 1, 1)

        languages_layout = QHBoxLayout()
        languages_layout.setAlignment(Qt.AlignCenter)
        languages_layout.setSpacing(40)
        languages_layout.addWidget(self.de)
        languages_layout.addWidget(self.eng)

        customization_layout = QHBoxLayout()
        customization_layout.setAlignment(Qt.AlignCenter)
        customization_layout.setSpacing(20)
        customization_layout.addWidget(self.default)
        customization_layout.addWidget(self.dark)
        customization_layout.addWidget(self.light)

        bgs_layout = QGridLayout()
        bgs_layout.addWidget(self.bg_dark, 0, 0, 1, 3)
        bgs_layout.addWidget(self.bg_light, 0, 3, 1, 3)
        bgs_layout.addWidget(self.radio_dark, 1, 1, 1, 1)
        bgs_layout.addWidget(self.radio_light, 1, 4, 1, 1)
        bgs_layout.setAlignment((Qt.AlignCenter))

        options_layout = QGridLayout()
        options_layout.addWidget(self.run_in_background, 0, 0)
        options_layout.addWidget(self.enable_shortcut, 1, 0)
        options_layout.addWidget(self.auto_replace, 2, 0)

        self.customization.setLayout(customization_layout)
        self.languages.setLayout(languages_layout)
        self.bgs.setLayout(bgs_layout)
        self.options.setLayout(options_layout)
        self.setLayout(main_layout)

    def apply(self):
        self.signal.emit(self.dark.isChecked())
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.__class__.toggle += 1
        self.close()
