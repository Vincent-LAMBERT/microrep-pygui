# Code taken from : https://stackoverflow.com/questions/67948983/resizing-a-window-with-pyqt5-how-do-i-reduce-the-size-of-a-widget-to-allow-the/67952671#67952671

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter

class ImageViewer(QLabel):
    pixmap = None
    _sizeHint = QSize()
    ratio = Qt.KeepAspectRatio
    transformation = Qt.SmoothTransformation

    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setPixmap(None)

    def setPixmap(self, pixmap):
        if self.pixmap != pixmap:
            self.pixmap = pixmap
            if isinstance(pixmap, QPixmap):
                self._sizeHint = pixmap.size()
            else:
                self._sizeHint = QSize()
            self.updateGeometry()
            self.updateScaled()

    def setAspectRatio(self, ratio):
        if self.ratio != ratio:
            self.ratio = ratio
            self.updateScaled()

    def setTransformation(self, transformation):
        if self.transformation != transformation:
            self.transformation = transformation
            self.updateScaled()

    def updateScaled(self):
        if self.pixmap :
            self.scaled = self.pixmap.scaled(self.size(), self.ratio, self.transformation)
            self.update()

    def sizeHint(self):
        return self._sizeHint

    def resizeEvent(self, event):
        self.updateScaled()

    def paintEvent(self, event):
        if not self.pixmap:
            return
        
        qp = QPainter(self)
        r = self.scaled.rect()
        r.moveCenter(self.rect().center())
        qp.drawPixmap(r, self.scaled)
