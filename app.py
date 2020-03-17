from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import sys

class TheWindow(QMainWindow):
    def __init__(self):
        super(TheWindow, self).__init__()
        self.x = 960
        self.y = 200
        self.width = 800
        self.height = 500

        self.setGeometry(self.x, self.y, self.width, self.height)

        self.setWindowTitle("File Organizer")
        self.initUI()

    def initUI(self):
        self.source_button = QtWidgets.QPushButton(self)
        self.source_button.setGeometry(10, 10, 50, 205)
        #self.source_button.setText("THE Click me")
        self.source_button.clicked.connect(self.open_dialog_box)

        self.target_button = QtWidgets.QPushButton(self)
        self.target_button.setGeometry(10, 225, 50, 205)
        #self.target_button.setText("THE Click me")
        self.target_button.clicked.connect(self.open_dialog_box)

        self.settings_button = QtWidgets.QPushButton(self)
        self.settings_button.setGeometry(10, 440, 50, 50)
        # self.settings_button.setText("THE Click me")
        self.settings_button.clicked.connect(self.open_dialog_box)

    def clicked(self):
        self.label.setText("you pressed THE button")

    def open_dialog_box(self):
        filename = QFileDialog.getOpenFileName(self)
        print(filename)


# QTextEdit

def window():
    app = QApplication(sys.argv)
    win = TheWindow()

    win.show()
    sys.exit(app.exec_())
