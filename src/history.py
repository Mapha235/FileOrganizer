from stylesheets import *

class History(QWidget):
    def __init__(self, x : int, y : int,  colormode : int, bg_path : str):
        super(History, self).__init__()
        self.x = x
        self.y = y
        self.my_width = self.frameGeometry().width()
        self.my_height = self.frameGeometry().height()

    def add(self, src, dst, file):
        return

    def initUI(self):
        self.setWindowTitle("Settings")
        self.setWindowIcon(QtGui.QIcon("./data/Settings.png"))
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setGeometry(self.x, self.y, self.my_width, self.my_height)

    def createLayout(self):
        return
        
    def eventFilter(self, obj, event):
        return
        
    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.close()