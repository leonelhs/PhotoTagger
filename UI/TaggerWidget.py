import qtawesome as qta
from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt, Signal)
from PySide6.QtWidgets import (QHBoxLayout, QLineEdit,
                               QPushButton, QVBoxLayout, QWidget, QMessageBox, QGraphicsScene)

from UI.widgets.ImageGraphicsView import ImageGraphicsView


class TaggerWidget(QWidget):
    taggerHandler = Signal(object)

    def __init__(self, parent=None):
        super(TaggerWidget, self).__init__(parent)
        self.__photo = None
        self.__tagEdit = None
        self.__photoViewer = None
        self.__photoLayout = None
        self.__layout = None
        self.buttonCancel = None
        self.buttonOK = None
        self.buttonsLayout = None
        self.__setupUi()

    def __setupUi(self):
        self.__layout = QVBoxLayout(self)
        self.__photoLayout = QVBoxLayout()
        self.__photoViewer = ImageGraphicsView(self)
        self.__photoViewer.setAlignment(Qt.AlignCenter)
        self.__photoLayout.addWidget(self.__photoViewer)

        self.__tagEdit = QLineEdit(self)
        self.__photoLayout.addWidget(self.__tagEdit)

        self.buttonsLayout = QHBoxLayout()
        self.buttonOK = QPushButton(self)

        icon_ok = qta.icon('mdi.check')
        self.buttonOK.setIcon(icon_ok)
        self.buttonsLayout.addWidget(self.buttonOK)

        self.buttonCancel = QPushButton(self)
        icon_close = qta.icon('mdi.close')
        self.buttonCancel.setIcon(icon_close)
        self.buttonsLayout.addWidget(self.buttonCancel)

        self.__photoLayout.addLayout(self.buttonsLayout)

        self.__layout.addLayout(self.__photoLayout)

        self.buttonOK.clicked.connect(self.onClickOK)
        self.buttonCancel.clicked.connect(self.onClickCancel)

        self.retranslateUi(self)

        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Tagging Face ", None))
        self.buttonOK.setText(QCoreApplication.translate("Form", u"OK", None))
        self.buttonCancel.setText(QCoreApplication.translate("Form", u"Cancel", None))

    def showDialog(self, message):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Tagging Person")
        dialog.setText(message)
        dialog.exec()

    def onClickOK(self):
        tagName = self.__tagEdit.text()
        if tagName:
            self.__photo.setTags(tagName)
            self.taggerHandler.emit(self.__photo)
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
        self.resize(image.width(), image.height())
