from stylesheets import *
from app import *


def makeScrollable(widget):
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(widget)
    scroll.setStyleSheet("")
    return scroll


def shortenPath(path_name, length):
    shortened_path_name = ""

    folders = path_name.split('/')
    # folder_num limits the number of folders that are displayed
    folder_num = int(length / 10)
    start = len(folders) - folder_num
    if folder_num > start:
        start = 0

    folders = folders[start:len(folders)]

    for f in folders:
        slash = '/'
        # this condition is only met when f equals the path-letter (such as C:). This way the
        # shortened_path_name does not have a slash as its first character
        if f[1] == ':':
            slash = ''
        shortened_path_name = shortened_path_name + slash + f

    if len(shortened_path_name) >= 1 and shortened_path_name[1] == ':':
        return shortened_path_name

    return "..." + shortened_path_name

def readFile():
    path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
    name = "save.txt"
    try:
        file = open(f"{path}/data/{name}", "r")
    except FileNotFoundError:
        file = open(f"{path}/data/{name}", "w+")

    values = []

    for i in file:
        temp = i.split('|')
        temp.pop()
        values.append(temp)

    if len(values) == 0:
        values.append([path,"0", ""])

    file.close()

    return values

def main():
    app = QApplication(sys.argv)
    win = TheWindow(readFile())
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
