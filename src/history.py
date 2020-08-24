from stylesheets import *


class History(QWidget):
    def __init__(self, x: int, y: int,  colormode: int, bg_path: str):
        super(History, self).__init__()
        self.x = x
        self.y = y
        self.my_width = self.frameGeometry().width()
        self.my_height = self.frameGeometry().height()

        self.history_table = QGroupBox(self)
        self.date_label = QLabel("2020-07-17  14:58")

        self.initUI()

    def add(self, src, dst, file):
        return

    def initUI(self):
        self.setWindowTitle("History")
        self.setGeometry(self.x, self.y, self.my_width, self.my_height)

        font = QtGui.QFont()
        font.setBold(True)
        self.date_label.setFont(font)
        # self.date_label.setStyleSheet("font-size: 12pt;")
        self.date_label.setAlignment(Qt.AlignCenter)

        self.createGridLayout()

    def createGridLayout(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.date_label)
        main_layout.addWidget(self.history_table)

        self.setLayout(main_layout)

    def tableLayout(self):
        self.history_table.setColumnCount(3)

    def eventFilter(self, obj, event):
        return

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.close()
