from stylesheets import *
from app import *

"""
TODO:
    - alle Entries organisieren in einer Datenstruktur oder Multithreading einbauen und mit thread_id's identifizieren
    - filtern nach mehreren keywords implementieren
    - duplikate erkennen in Entry
    - Ausnahme-keywords einbauen
    - savefile
    - settings
        - custom hintergrund
        - light/dark mode
        - sprachen
    - linux support(?)
    - If schleifen in eventFilter verbessern
    - regular expressions einbauen
    - wenn möglich eventFilter mit connect ersetzen
    
"""


def makeScrollable(widget):
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(widget)
    return scroll


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
        shortened_path_name = shortened_path_name[k:l - 1]

    if l >= 1 and shortened_path_name[1] == ":":
        return shortened_path_name

    return "..." + shortened_path_name


def main():
    app = QApplication(sys.argv)
    win = TheWindow()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
