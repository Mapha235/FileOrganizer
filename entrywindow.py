from main import shorten_path
from stylesheets import *


class EntryWindow(QWidget):
    send_signal = pyqtSignal(list)

    def __init__(self, x, y, color_mode: int, bg_path: str):
        super(EntryWindow, self).__init__()
        self.data = [None] * 3
        self.data[2] = ""
        self.x = x
        self.y = y


        self.theme = ""
        if color_mode == 0:
            self.theme = default
        elif color_mode == 1:
            self.theme = dark
        elif color_mode == 2:
            self.theme = light

        self.bg = QImage(bg_path)

        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

        # set Background Image
        self.bg = QImage(bg_path)

        self.src_btn = QtWidgets.QPushButton("Browse Source Folder", self)
        self.src_btn.setObjectName("0")
        self.dst_btn = QtWidgets.QPushButton("Browse Destination Folder", self)
        self.dst_btn.setObjectName("1")

        self.add_btn = QtWidgets.QPushButton("Add", self)
        self.add_btn.clicked.connect(self.send_data)
        self.cancel_btn = QtWidgets.QPushButton("Cancel", self)

        self.btns = []
        self.btns.append(self.dst_btn)
        self.btns.append(self.src_btn)
        self.btns.append(self.add_btn)
        self.btns.append(self.cancel_btn)

        self.label = QtWidgets.QLabel("Example: urlaub//.pdf//5e-43c5")

        self.keyword_text_field = QtWidgets.QLineEdit(self)
        self.keyword_text_field.setPlaceholderText("Enter keyword(s)")
        self.keyword_text_field.returnPressed.connect(self.send_data)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Add New Entry")
        self.setGeometry(self.x, self.y, self.frameGeometry().width(), self.frameGeometry().height())
        self.setMaximumSize(500, 100)


        for btn in self.btns:
            btn.installEventFilter(self)
            #btn.setFixedHeight(18)
        self.btns.clear()
        #button_width = (self.frameGeometry().width() / 2) - 12
        #button_height = 18
        #self.src_btn.setFixedSize(button_width, button_height)
        #self.dst_btn.setFixedSize(button_width, button_height)

        self.setStyleSheet(self.theme + "font-size: 10pt;")

        if self.theme is default:
            self.label.setStyleSheet(examples + "color: black;")
        else:
            self.label.setStyleSheet(examples + "color: white;")

        self.createGridLayout()

    def createGridLayout(self):
        layout_grid = QGridLayout()

        self.setLayout(layout_grid)
        layout_grid.setSpacing(3)

        layout_grid.addWidget(self.src_btn, 0, 0, 1, 4)
        layout_grid.addWidget(self.dst_btn, 0, 4, 1, 4)
        layout_grid.addWidget(self.keyword_text_field, 1, 0, 1, 8)

        layout_grid.addWidget(self.label, 2, 0, 1, 4)
        layout_grid.addWidget(self.add_btn, 2, 4, 1, 2)
        layout_grid.addWidget(self.cancel_btn, 2, 6, 1, 2)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.HoverEnter:
            obj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        elif event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton:
            if obj is self.src_btn or obj is self.dst_btn:
                self.open_dialog_box(obj)
            elif obj is self.cancel_btn:
                self.close()
            elif obj is self.add_btn:
                self.send_data()
        return super(EntryWindow, self).eventFilter(obj, event)

    def correct_canceled(self, btn: QtWidgets.QPushButton):
        index = int(btn.objectName())
        name = "Destination"
        if index == 0:
            name = "Source"
        if self.data[index] is "":
            self.data[index] = None
        temp = btn.text()
        btn.setText(f"Browse {name} Folder")
        return temp

    def open_dialog_box(self, btn: QtWidgets.QPushButton):
        path_name = QFileDialog.getExistingDirectory(self)

        # TODO: regular expressions
        # shortened_path_name = re.search(r'/(.*)/', path_name)
        # shortens the path to the last two folders

        # saves the selected path to the respective place in data
        index = int(btn.objectName())
        self.data[index] = path_name
        self.correct_canceled(btn)

        if path_name != "":
            shortened_path_name = shorten_path(path_name, 27)
            if shortened_path_name != "...":
                btn.setText(shortened_path_name)

    def send_data(self):
        if self.keyword_text_field.text() != "":
            self.data[2] = self.keyword_text_field.text()

        if self.check_integrity():
            self.send_signal.emit(self.data)
            self.close()

    # checks whether src and dst folder are the same
    def is_equal(self):
        if self.src_btn.text() == self.dst_btn.text():
            return True
        return False

    def check_integrity(self):
        msg = QMessageBox()
        msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        if not any(x is None for x in self.data):
            if self.is_equal():
                msg.setWindowTitle("Error")
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error: Source and Destination Folder cannot be the same.")
                msg.exec()
                return False
            elif self.data[2] == "":
                msg.setWindowTitle("Note!")
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Note:\nUsing no keywords will move all files."
                            + "\nClick \"Edit\" to add keywords.")
                msg.exec()
            return True
        else:
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Critical)
            if self.data[0] is None and self.data[1] is None:
                msg.setText("Error: Source-Folder not selected.\n"
                            + "Error: Destination-Folder not selected.\n")
            elif self.data[0] is None:
                msg.setText("Error: Source-Folder not selected.")
            elif self.data[1] is None:
                msg.setText("Error: Destination-Folder not selected.")

            msg.exec()

        return False

    def resizeEvent(self, event):
        if self.theme is not default:
            scaled_bg = self.bg.scaled(QSize(self.width(), self.height()))
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(scaled_bg))
            self.setPalette(palette)
