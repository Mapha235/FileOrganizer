import sys
from lib.folder import Folder
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QSize, QPropertyAnimation, QRect, Qt
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QApplication, QGridLayout, QSizePolicy, QWidget, QTextBrowser, QStackedWidget, \
    QStackedLayout, QGroupBox, QVBoxLayout, QHBoxLayout, QScrollArea, QLineEdit

from entry import EntryWindow
from settings import Settings
from stylesheets import *


class TheWindow(QWidget):
    def __init__(self):
        super(TheWindow, self).__init__()
        self.scroll = QScrollArea()
        self.x = 160
        self.y = 200
        self.my_width = 800
        self.my_height = 500

        self.entry_window = None
        self.settings_page = None

        self.entries = []

        # set Background Image
        self.bg = QImage("./data/bg4.jpg")

        self.settings_button = QtWidgets.QPushButton(self)
        self.create_entry_button = QtWidgets.QPushButton("Create New Entry", self)
        self.run_script_button = QtWidgets.QPushButton(self)

        # list of all buttons
        self.buttons = []

        self.buttons.append(self.settings_button)
        self.buttons.append(self.create_entry_button)
        self.buttons.append(self.run_script_button)

        self.source_text_browser = QTextBrowser(self)
        self.target_text_browser = QTextBrowser(self)
        self.entry_box = QGroupBox(self)
        self.entry_box.setStyleSheet("font-size: 14pt; color: rgb(225,225,225); background-color: rgba(255,255,255,0.0); ")



        self.initUI()

    def initUI(self):
        self.setWindowTitle("File Organizer")
        self.setGeometry(self.x, self.y, self.my_width, self.my_height)
        self.setFixedSize(800, 500)

        # Design of the settings button
        self.settings_button.setFixedSize(70, 70)
        self.settings_button.setIcon(
            QtGui.QIcon("./data/Settings.png"))

        self.settings_button.setIconSize(QtCore.QSize(60, 60))

        self.run_script_button.setFixedWidth(70)
        self.run_script_button.setIcon(
            QtGui.QIcon("./data/arrow.png"))
        self.run_script_button.setIconSize(QtCore.QSize(60, 60))

        self.create_entry_button.setFixedHeight(70)

        for button in self.buttons:
            # used for mouse hover event
            button.installEventFilter(self)

        self.buttons.clear()

        # self.settings_button.clicked.connect(self.rotate)

        # assign design layout to all widgets
        self.setStyleSheet(light)
        self.createGridLayout()
        self.createBoxLayout()
        self.makeScrollable(self.entry_box)
        self.show()

    def createBoxLayout(self):
        trash_box = QVBoxLayout()

        trash_box.setAlignment(Qt.AlignTop)
        trash_box.setContentsMargins(0, 0, 0, 0)

        #trash_box.setSpacing(10)
        for i in range(0, 10):
            entry = Entry((((self.height() - 110) / 2) - 60) / 5)
            self.entries.append(entry)
            trash_box.addWidget(entry)

        self.entry_box.setLayout(trash_box)

    def parse(self, *data):
        if len(data) != 3:
            print("Error!")

        # entriesEntry((self.height()-110)/2) - 30) / 5)

    def makeScrollable(self, widget):
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(widget)

    def createGridLayout(self):
        layout_grid = QGridLayout()

        layout_grid.setSpacing(10)

        layout_grid.addWidget(self.settings_button, 0, 0, 1, 1)
        layout_grid.addWidget(self.create_entry_button, 0, 1, 1, 8)

        layout_grid.addWidget(self.scroll, 1, 0, 1, 9)

        layout_grid.addWidget(self.source_text_browser, 2, 0, 1, 4)
        layout_grid.addWidget(self.run_script_button, 2, 4, 1, 1)
        layout_grid.addWidget(self.target_text_browser, 2, 5, 1, 4)
        self.setLayout(layout_grid)

    def openEntry(self):
        self.entry_window = EntryWindow(self.pos().x() + (self.width() / 4), self.pos().y() + 50)
        self.entry_window.show()

    def doAnimation(self):
        self.settings_page = Settings(self.pos().x() - 400, self.pos().y() + 60)
        self.anim = QPropertyAnimation(self.settings_page, b"geometry")
        self.anim.setDuration(1000)
        self.anim.setStartValue(QRect(-1000, 100, 500, 400))
        self.anim.setEndValue(QRect(0, 100, 500, 400))
        self.anim.start()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.HoverEnter:
            obj.setStyleSheet(mouse_hover)
        elif event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
            obj.setStyleSheet(mouse_hover + mouse_click)
        elif event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton:
            obj.setStyleSheet(mouse_hover)
            if obj == self.create_entry_button:
                self.openEntry()
            elif obj == self.settings_button:
                self.doAnimation()
        elif event.type() == QtCore.QEvent.HoverLeave:
            obj.setStyleSheet(light)
        return super(TheWindow, self).eventFilter(obj, event)

    def resizeUI(self):
        self.my_width = self.width()
        self.my_height = self.height()

        self.scroll.setFixedHeight(int(self.height() / 2))

        for entry in self.entries:
            entry.setFixedHeight((((self.height() - 110) / 2) - 30) / 5)

        # set background image
        scaled_bg = self.bg.scaled(QSize(self.my_width, self.my_height))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(scaled_bg))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.resizeUI()


class Entry(QGroupBox):
    def __init__(self, h):
        super(Entry, self).__init__()

        self.script = Folder("C:/", "C:/", ".txt")
        self.setFixedHeight(h)

        self.source = QLineEdit()
        self.target = QLineEdit()
        self.keyword = QLineEdit()

        self.edit_button = QtWidgets.QPushButton("Edit")
        self.trash_button = QtWidgets.QPushButton()

        self.initUI()

    def initUI(self):
        self.source.setReadOnly(True)
        self.target.setReadOnly(True)
        self.keyword.setReadOnly(True)

        self.setFixedHeight(50)

        #self.source.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
       # self.target.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.keyword.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.trash_button.setIcon(
            QtGui.QIcon("C:/Users/willi/Desktop/pythonProjects/FileOrganizer/data/error.png"))

        self.createBoxLayout()
        self.setStyleSheet(entry_layout + "color: black;")

    def createBoxLayout(self):
        layout = QHBoxLayout()

        layout.addWidget(self.source)
        layout.addWidget(self.target)
        layout.addWidget(self.keyword)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.trash_button)

        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)



def window():
    app = QApplication(sys.argv)
    win = TheWindow()

    sys.exit(app.exec_())
