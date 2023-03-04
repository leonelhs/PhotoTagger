import qtawesome as qta
from PySide6.QtCore import (QMetaObject, Qt, Signal)
from PySide6.QtWidgets import (QHBoxLayout, QLineEdit,
                               QPushButton, QVBoxLayout, QWidget, QMessageBox, QGraphicsScene)

from UI.widgets.image_graphics_wiew import ImageGraphicsView


class TaggerWidget(QWidget):
    taggerMessageHandler = Signal(object)

    def __init__(self, parent=None):
        super(TaggerWidget, self).__init__(parent)
        self.__photo = None
        self.__tagEdit = None
        self.__photoViewer = None
        self.__photoLayout = None
        self.__layout = None
        self.__buttonCancel = None
        self.__buttonOK = None
        self.__buttonsLayout = None
        self.__setupUi()

    def __setupUi(self):
        self.setWindowTitle("Tagging Person")
        self.__layout = QVBoxLayout(self)
        self.__photoLayout = QVBoxLayout()
        self.__photoViewer = ImageGraphicsView(self)
        self.__photoViewer.setAlignment(Qt.AlignCenter)
        self.__photoLayout.addWidget(self.__photoViewer)

        self.__tagEdit = QLineEdit(self)
        self.__photoLayout.addWidget(self.__tagEdit)

        self.__buttonsLayout = QHBoxLayout()
        self.__buttonOK = QPushButton(self)

        icon_ok = qta.icon('mdi.check')
        self.__buttonOK.setIcon(icon_ok)
        self.__buttonsLayout.addWidget(self.__buttonOK)

        self.__buttonCancel = QPushButton(self)
        icon_close = qta.icon('mdi.close')
        self.__buttonCancel.setIcon(icon_close)
        self.__buttonsLayout.addWidget(self.__buttonCancel)

        self.__layout.addLayout(self.__photoLayout)
        self.__layout.addLayout(self.__buttonsLayout)

        self.__buttonOK.clicked.connect(self.onClickOK)
        self.__buttonCancel.clicked.connect(self.onClickCancel)

        QMetaObject.connectSlotsByName(self)

    def showDialog(self, message):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Tagging Person")
        dialog.setText(message)
        dialog.exec()

    def onClickOK(self):
        tagName = self.__tagEdit.text()
        if tagName:
            self.__photo.setTags(tagName)
            self.taggerMessageHandler.emit(self.__photo)
            self.close()
        else:
            self.showDialog("Please enter a name for this person!")

    def onClickCancel(self):
        self.close()

    def onFaceTaggerRequest(self, photo):
        self.__photo = photo
        self.__tagEdit.setText(photo.tags())
        image = photo.pixmap()
        scene = QGraphicsScene()
        scene.addPixmap(image)
        self.__photoViewer.setScene(scene)
