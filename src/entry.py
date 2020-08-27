from main import shortenPath
from stylesheets import *


class Entry(QGroupBox):
    is_applied = False
    clicked_signal = pyqtSignal(list, list, list, list, str)
    send_id = pyqtSignal(int)
    send_id2 = pyqtSignal(int)
    files_moved_signal = pyqtSignal(int)
    run_task_signal = pyqtSignal()
    id = 0

    def __init__(self, root: str, src, dst, keyw, isChecked=True):
        self.my_id = self.__class__.id
        self.__class__.id += 1

        self.root = root

        super(Entry, self).__init__()

        self.script = Folder(src, dst, keyw)
        # self.setFixedHeight(27)

        self.src = QLabel()
        self.dst = QLabel()
        self.keywords_line_edit = QLineEdit()

        short_src_path = shortenPath(src, 29)
        short_dst_path = shortenPath(dst, 29)

        self.src.setText(short_src_path)
        self.dst.setText(short_dst_path)
        self.keywords_line_edit.insert(keyw)

        self.move_btn = QtWidgets.QPushButton()
        self.edit_btn = QtWidgets.QPushButton("Edit")
        self.delete_btn = QtWidgets.QPushButton()

        self.check_box = QCheckBox()
        self.check_box.setChecked(isChecked)

        self.entry_list = []

        self.entry_list.append(self.check_box)
        self.entry_list.append(self.src)
        self.entry_list.append(self.move_btn)
        self.entry_list.append(self.dst)
        self.entry_list.append(self.keywords_line_edit)
        self.entry_list.append(self.edit_btn)
        self.entry_list.append(self.delete_btn)

        self.observer = QtCore.QFileSystemWatcher([self.script.getSrcDir()])

        self.initUI()
        self.signalHandler()
        
    def delete(self):
        self.__class__.id -= 1
        self.send_id.emit(self.my_id)
        self.close()

    def adjustID(self):
        self.my_id -= 1

    def getCheckBox(self):
        return self.check_box.isChecked()

    def initUI(self):

        for x in self.entry_list:
            if type(x) is QLineEdit:
                x.setReadOnly(True)
                x.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            elif type(x) is QtWidgets.QPushButton:
                x.installEventFilter(self)
            elif type(x) is QLabel:
                x.setFixedWidth(270)

        self.setFixedHeight(40)

        os.chdir(self.root)
        self.delete_btn.setIcon(QtGui.QIcon("./data/error.png"))
        self.move_btn.setIcon(QtGui.QIcon("./data/arrow2.png"))

        self.createBoxLayout()
        self.setStyleSheet(entry_layout + "color: black;")

    def signalHandler(self):
        self.move_btn.clicked.connect(self.runTask)
        self.edit_btn.clicked.connect(self.editKeywords)
        # self.keywords_line_edit.returnPressed.connect(self.editKeywords)
        self.delete_btn.clicked.connect(self.delete)
        self.observer.directoryChanged.connect(lambda: self.run_task_signal.emit())

    def runTask(self):
        files_moved = self.script.move()
        self.script.remove()
        self.files_moved_signal.emit(files_moved)
        self.mousePressEvent(self.clicked)

    def createBoxLayout(self):
        layout = QHBoxLayout()

        for x in self.entry_list:
            layout.addWidget(x)

        layout.setContentsMargins(7, 7, 7, 7)
        self.setLayout(layout)

    def editKeywords(self):
        self.is_applied = not self.is_applied
        if self.is_applied == True:
            self.keywords_line_edit.setFocus(QtCore.Qt.MouseFocusReason)
            self.keywords_line_edit.setReadOnly(False)
            self.edit_btn.setText("Apply")
            self.keywords_line_edit.setStyleSheet(
                "background-color: rgba(0,0,0,0.0);")
        else:
            self.keywords_line_edit.setReadOnly(True)
            self.edit_btn.setText("Edit")
            self.script.setKeywords(self.keywords_line_edit.text())
            self.keywords_line_edit.setStyleSheet(
                entry_layout + "color: black;")
            self.mousePressEvent(self.clicked)

    def sendRunSignal(self):
        if self.check_box.isChecked():
            self.run_task_signal.emit()
        

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        src_data = self.script.getSrcContent()
        dst_data = self.script.getDstContent()
        self.clicked_signal.emit(src_data[0], src_data[1],
                                 dst_data[0], dst_data[1],
                                 self.script.keywords)

        self.send_id2.emit(self.my_id)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.HoverEnter:
            obj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        return super(Entry, self).eventFilter(obj, event)
