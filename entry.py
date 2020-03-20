from app import *
from stylesheets import *


class Entry(QWidget):
    def __init__(self, x, y):
        super(Entry, self).__init__()
        self.x = x
        self.y = y


        # set Background Image
        self.bg = QImage("C:/Users/willi/Desktop/pythonProjects/FileOrganizer/data/bg.png")

        self.source_button = QtWidgets.QPushButton("Browse Source Folder", self)
        self.target_button = QtWidgets.QPushButton("Browse Target Folder", self)

        self.add_button = QtWidgets.QPushButton("Add", self)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)

        self.buttons = []
        self.buttons.append(self.target_button)
        self.buttons.append(self.source_button)
        self.buttons.append(self.add_button)
        self.buttons.append(self.cancel_button)

        self.keyword_text_field = QtWidgets.QLineEdit(self)
        self.keyword_text_field.setPlaceholderText("Enter keyword")
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Add New Entry")
        self.setFixedSize(400, 100)
        self.setGeometry(self.x, self.y, self.width(), self.height())

        for button in self.buttons:
            button.installEventFilter(self)
        self.buttons.clear()

        self.setStyleSheet(entry_layout)


        self.createGridLayout()

    def createGridLayout(self):
        layout_grid = QGridLayout()

        self.setLayout(layout_grid)
        layout_grid.setSpacing(3)

        layout_grid.addWidget(self.source_button, 0, 0, 1, 4)
        layout_grid.addWidget(self.target_button, 0, 4, 1, 4)
        layout_grid.addWidget(self.keyword_text_field, 1, 0, 1, 8)

        layout_grid.addWidget(self.add_button, 2, 4, 1, 2)

        layout_grid.addWidget(self.cancel_button, 2, 6, 1, 2)



    def eventFilter(self, obj, event):
        default_style_sheet = self.styleSheet()
        if event.type() == QtCore.QEvent.HoverEnter:
            obj.setStyleSheet(entry_mouse_hover)
        elif event.type() == QtCore.QEvent.HoverLeave:
            obj.setStyleSheet(entry_layout)
        return super(Entry, self).eventFilter(obj, event)


    def open_dialog_box(self):
        filename = QFileDialog.getExistingDirectory(self)
        print(filename)



    def resizeBG(self):
        # set background image
        scaled_bg = self.bg.scaled(QSize(self.width(), self.height()))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(scaled_bg))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.resizeBG()




def window2():
    app = QApplication(sys.argv)
    win = Entry()
    win.show()
    sys.exit(app.exec_())
