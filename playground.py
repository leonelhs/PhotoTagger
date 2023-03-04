import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QLabel
)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        picture = QLabel()
        picture.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(picture)


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()


main()
