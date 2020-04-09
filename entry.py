from main import shorten_path
from stylesheets import *


class Entry(QGroupBox):
    clicked_signal = pyqtSignal(list, list, str)
    send_id = pyqtSignal(int)
    id = 0

    def __init__(self, s, t, k, b=True):
        self.my_id = self.__class__.id
        self.__class__.id += 1

        super(Entry, self).__init__()

        self.script = Folder(s, t, k)
        self.setFixedHeight(27)

        self.source = QLabel()
        self.target = QLabel()
        self.keywords = QLineEdit()

        short_source_path = shorten_path(s, 30)
        short_target_path = shorten_path(t, 30)

        self.source.setText(short_source_path)
        self.target.setText(short_target_path)
        self.keywords.insert(k)

        self.edit_button = QtWidgets.QPushButton("Edit")
        self.edit_button.clicked.connect(self.editKeywords)
        self.delete_button = QtWidgets.QPushButton()

        self.check_box = QCheckBox()
        self.check_box.setChecked(b)

        self.entry_list = []

        self.entry_list.append(self.check_box)
        self.entry_list.append(self.source)
        self.entry_list.append(self.target)
        self.entry_list.append(self.keywords)
        self.entry_list.append(self.edit_button)
        self.entry_list.append(self.delete_button)

        self.initUI()

    def __del__(self):
        self.close()
        self.__class__.id -= 1
        self.send_id.emit(self.my_id)

    def adjustID(self):
        self.my_id -= 1

    def get_check_box(self):
        return self.check_box.isChecked()

    def initUI(self):

        for x in self.entry_list:
            if type(x) is QLineEdit:
                x.setReadOnly(True)
                x.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            elif type(x) is QtWidgets.QPushButton:
                x.installEventFilter(self)
            elif type(x) is QLabel:
                x.setFixedWidth(205)

        self.setFixedHeight(35)

        os.chdir("C:/Dev/python/FileOrganizer")
        self.delete_button.setIcon(QtGui.QIcon("./data/error.png"))
        self.delete_button.clicked.connect(self.__del__)

        self.createBoxLayout()
        self.setStyleSheet(entry_layout + "color: black;")

    def createBoxLayout(self):
        layout = QHBoxLayout()

        for x in self.entry_list:
            layout.addWidget(x)

        layout.setContentsMargins(7, 7, 7, 7)
        self.setLayout(layout)

    def editKeywords(self):
        self.keywords.setReadOnly(False)
        self.edit_button.setText("Apply")
        self.keywords.setStyleSheet("background-color: rgba(0,0,0,0.0);")
        self.script.set_keywords(self.keywords.text())
        self.edit_button.clicked.connect(self.applyKeywords)

    def applyKeywords(self):
        self.keywords.setReadOnly(True)
        self.edit_button.setText("Edit")
        self.keywords.setStyleSheet(entry_layout + "color: black;")
        self.script.set_keywords(self.keywords.text())
        self.edit_button.clicked.connect(self.editKeywords)
        self.mousePressEvent(self.clicked)

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        self.clicked_signal.emit(self.script.get_source_content(), self.script.get_target_content(),
                                 self.script.keywords)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.HoverEnter:
            obj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        return super(Entry, self).eventFilter(obj, event)
