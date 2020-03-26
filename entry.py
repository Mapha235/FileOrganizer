import re

import PyQt5
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal

from app import *

from stylesheets import *


class EntryWindow(QWidget):
    send_signal = pyqtSignal(list)

    def __init__(self, x, y):
        super(EntryWindow, self).__init__()
        self.data = [None] * 3
        self.data[2] = ""
        self.x = x
        self.y = y

        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

        # set Background Image
        self.bg = QImage("C:/Dev/python/FileOrganizer/data/bg4.jpg")

        self.source_button = QtWidgets.QPushButton("Browse Source Folder", self)
        self.source_button.setObjectName("0")
        self.target_button = QtWidgets.QPushButton("Browse Target Folder", self)
        self.target_button.setObjectName("1")

        self.add_button = QtWidgets.QPushButton("Add", self)
        self.add_button.setAutoDefault(True)

        self.cancel_button = QtWidgets.QPushButton("Cancel", self)

        self.buttons = []
        self.buttons.append(self.target_button)
        self.buttons.append(self.source_button)
        self.buttons.append(self.add_button)
        self.buttons.append(self.cancel_button)

        self.label = QtWidgets.QLabel("Example: urlaub//.pdf//5e-43c5")

        self.keyword_text_field = QtWidgets.QLineEdit(self)
        self.keyword_text_field.setPlaceholderText("Enter keyword(s)")
        self.keyword_text_field.returnPressed.connect(self.send_data)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Add New Entry")
        self.setFixedSize(400, 100)
        self.setGeometry(self.x, self.y, self.width(), self.height())

        for button in self.buttons:
            button.installEventFilter(self)
            button.setFixedHeight(18)
        self.buttons.clear()
        self.source_button.setFixedSize(int(self.width() / 2) - 6, 18)

        self.setStyleSheet(entry_layout + "color: white;")
        self.label.setStyleSheet(examples)

        self.createGridLayout()

    def createGridLayout(self):
        layout_grid = QGridLayout()

        self.setLayout(layout_grid)
        layout_grid.setSpacing(3)

        layout_grid.addWidget(self.source_button, 0, 0, 1, 4)
        layout_grid.addWidget(self.target_button, 0, 4, 1, 4)
        layout_grid.addWidget(self.keyword_text_field, 1, 0, 1, 8)

        layout_grid.addWidget(self.label, 2, 0, 1, 4)
        layout_grid.addWidget(self.add_button, 2, 4, 1, 2)
        layout_grid.addWidget(self.cancel_button, 2, 6, 1, 2)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.HoverEnter:
            obj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        elif event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton:
            if obj == self.source_button or obj == self.target_button:
                self.open_dialog_box(obj)
            elif obj == self.cancel_button:
                self.close()
            elif obj == self.add_button:
                self.send_data()

        return super(EntryWindow, self).eventFilter(obj, event)

    def correct_canceled(self, btn: QtWidgets.QPushButton):
        index = int(btn.objectName())

        if self.data[index] is "":
            self.data[index] = None
        btn.setText("?")


    def open_dialog_box(self, btn: QtWidgets.QPushButton):
        path_name = QFileDialog.getExistingDirectory(self)

        # TODO: regular expressions
        # shortened_path_name = re.search(r'/(.*)/', path_name)
        # shortens the path to the last two folders

        # saves the selected path to the respective place in data
        index = int(btn.objectName())
        self.data[index] = path_name
        self.correct_canceled(btn)

        shortened_path_name = shorten_path(path_name, 27)
        if shortened_path_name != "...":
            btn.setText(shortened_path_name)


    def send_data(self):
        if self.keyword_text_field.text() is not "":
            self.data[2] = self.keyword_text_field.text()

        self.check_integrity()
        if not any(x is None for x in self.data):
            print("sent")
            self.send_signal.emit(self.data)
            self.close()

    def check_integrity(self):
        msg = QMessageBox()

        if not any(x is None for x in self.data):
            if self.data[2] == "":
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
                            + "Error: Target-Folder not selected.\n")
            elif self.data[0] is None:
                msg.setText("Error: Source-Folder not selected.")
            elif self.data[1] is None:
                msg.setText("Error: Target-Folder not selected.")

            msg.exec()

        return False

    def resizeBG(self):
        # set background image
        scaled_bg = self.bg.scaled(QSize(self.width(), self.height()))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(scaled_bg))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.resizeBG()


def shorten_path(path_name, length):
    counter = 0
    shortened_path_name = ""

    for i in reversed(path_name):
        if counter >= 2:
            break
        elif i == '/':
            counter += 1
        shortened_path_name += i

    shortened_path_name = shortened_path_name[::-1]
    l = len(shortened_path_name)
    if l >= length:
        k = l - 1 - length
        shortened_path_name = shortened_path_name[k:(l-1)]

    if l >= 1 and shortened_path_name[1] == ":":
        return shortened_path_name

    return "..." + shortened_path_name
