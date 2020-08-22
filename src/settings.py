from stylesheets import *


class Settings(QWidget):
    toggle = False
    design_signal = pyqtSignal(int, str)
    bg_dark_clicked = pyqtSignal()
    bg_light_clicked = pyqtSignal()

    def __init__(self, x, y, language_mode: int, color_mode: int, is_bg4: bool, groot: str):
        super(Settings, self).__init__()
        self.__class__.toggle = not self.__class__.toggle
        self.x = x
        self.y = y
        self.my_width = self.frameGeometry().width()
        self.my_height = self.frameGeometry().height()
        self.setFixedSize(self.my_width, self.my_height)
        self.bg_path = ""

        self.root = groot

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

        if color_mode == 0:
            self.default.setChecked(True)
        elif color_mode == 1:
            self.dark.setChecked(True)
        elif color_mode == 2:
            self.light.setChecked(True)

        if language_mode == 0:
            self.de.setChecked(True)
        else:
            self.eng.setChecked(True)

        if is_bg4:
            self.radio_light.setChecked(True)
        else:
            self.radio_dark.setChecked(True)

        self.initUI()
        self.handle_signals()

    def initUI(self):
        self.setWindowTitle("Settings")
        self.setWindowIcon(QtGui.QIcon("./data/Settings.png"))
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setGeometry(self.x, self.y, self.my_width, self.my_height)

        pix_dark = QtGui.QPixmap("./data/tile2.png")
        pix_light = QtGui.QPixmap("./data/tile.png")

        self.languages.setEnabled(False)

        self.bg_dark.setPixmap(pix_dark)
        self.bg_dark.setFixedSize(100, 60)
        self.bg_dark.setScaledContents(True)
        #self.bg_dark.installEventFilter(self)

        self.bg_light.setPixmap(pix_light)
        self.bg_light.setFixedSize(100, 60)
        self.bg_light.setScaledContents(True)
        #self.bg_light.installEventFilter(self)

        if self.default.isChecked():
            self.bgs.setEnabled(False)
        self.default.toggled.connect(self.toggle_bg_box)

        self.createLayout()

    def toggle_bg_box(self):
        if self.default.isChecked():
            self.bgs.setEnabled(False)
        else:
            self.bgs.setEnabled(True)

    def updatePos(self, x, y):
        self.x = x
        self.y = y
        #self.setGeometry(x, y, self.my_width, self.my_height)
        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()
        self.setGeometry(x, y, self.width, self.height)

    def handle_signals(self):
        if self.default.isChecked():
            self.bgs.setEnabled(False)

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
        bgs_layout.setAlignment(Qt.AlignCenter)

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
        if self.radio_dark.isChecked():
            self.bg_path = f"{self.root}/data/bg.jpg"
        elif self.radio_light.isChecked():
            self.bg_path = f"{self.root}/data/bg4.jpg"

        if self.default.isChecked():
            color_mode = 0
        elif self.dark.isChecked():
            color_mode = 1
        elif self.light.isChecked():
            color_mode = 2
        self.design_signal.emit(color_mode, self.bg_path)
        self.close()

    def eventFilter(self, obj, event):
        if event.type() is QtCore.QEvent.MouseButtonPress:
            if obj is self.bg_dark:
                self.radio_dark.setChecked(True)
            elif obj is self.bg_light:
                self.radio_light.setChecked(True)
        return super(Settings, self).eventFilter(obj, event)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.__class__.toggle = not self.__class__.toggle
        self.close()
