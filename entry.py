from main import shorten_path
from stylesheets import *


class Entry(QGroupBox):
    clicked_signal = pyqtSignal(list, list, str)
    send_id = pyqtSignal(int)
    send_id2 = pyqtSignal(int)
    id = 0

    def __init__(self, s, t, k, b=True):
        self.my_id = self.__class__.id
        self.__class__.id += 1

        super(Entry, self).__init__()

        self.script = Folder(s, t, k)
        self.setFixedHeight(27)

        self.src = QLabel()
        self.dst = QLabel()
        self.keywords = QLineEdit()

        short_src_path = shorten_path(s, 29)
        short_dst_path = shorten_path(t, 29)

        self.src.setText(short_src_path)
        self.dst.setText(short_dst_path)
        self.keywords.insert(k)

        self.move_btn = QtWidgets.QPushButton()
        self.edit_btn = QtWidgets.QPushButton("Edit")
        self.delete_btn = QtWidgets.QPushButton()

        self.check_box = QCheckBox()
        self.check_box.setChecked(b)

        self.entry_list = []

        self.entry_list.append(self.check_box)
        self.entry_list.append(self.src)
        self.entry_list.append(self.move_btn)
        self.entry_list.append(self.dst)
        self.entry_list.append(self.keywords)
        self.entry_list.append(self.edit_btn)
        self.entry_list.append(self.delete_btn)

        self.initUI()
        self.button_handler()

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

        self.move_btn.setIcon(QtGui.QIcon("./data/arrow2.png"))
        self.delete_btn.setIcon(QtGui.QIcon("./data/error.png"))

        self.createBoxLayout()
        self.setStyleSheet(entry_layout + "color: black;")
        
    def button_handler(self):
        self.move_btn.clicked.connect(self.run_task)
        self.edit_btn.clicked.connect(self.editKeywords)
        self.delete_btn.clicked.connect(self.__del__)

    def run_task(self):
        self.script.move()
        self.mousePressEvent(self.clicked)

    def createBoxLayout(self):
        layout = QHBoxLayout()

        for x in self.entry_list:
            layout.addWidget(x)

        layout.setContentsMargins(7, 7, 7, 7)
        self.setLayout(layout)

    def editKeywords(self):
        self.keywords.setReadOnly(False)
        self.edit_btn.setText("Apply")
        self.keywords.setStyleSheet("background-color: rgba(0,0,0,0.0);")
        self.script.set_keywords(self.keywords.text())
        self.edit_btn.clicked.connect(self.applyKeywords)
        print(self.script.dst_dir)

    def applyKeywords(self):
        self.keywords.setReadOnly(True)
        self.edit_btn.setText("Edit")
        self.keywords.setStyleSheet(entry_layout + "color: black;")
        self.script.set_keywords(self.keywords.text())
        self.edit_btn.clicked.connect(self.editKeywords)
        self.mousePressEvent(self.clicked)
        print(self.script.src_dir)

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        self.clicked_signal.emit(self.script.get_src_content(),
                                 self.script.get_dst_content(),
                                 self.script.keywords)

        self.send_id2.emit(self.my_id)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.HoverEnter:
            obj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        return super(Entry, self).eventFilter(obj, event)