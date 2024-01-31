import sys
from PyQt5 import QtCore, QtWidgets

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MyWindow')
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main) 
        self.button = QtWidgets.QPushButton('Do it')
        self.button.clicked.connect(self.do)

        self.contincheck = QtWidgets.QCheckBox("Continuous")
        self.contincheck.clicked.connect(self.continuous_doing)
        self.continuous = False
        layout = QtWidgets.QGridLayout(self._main)
        layout.addWidget(self.button, 0, 0)
        layout.addWidget(self.contincheck, 1, 0)

        self.mythread = MyThread(self.continuous, self)
        self.mythread.finished.connect(self.thread_finished)
        self.button.clicked.connect(self.mythread.stop)
        self.mythread.signal.connect(self.done)

    def continuous_doing(self):
        self.button.setCheckable(self.contincheck.isChecked())
        self.continuous = self.contincheck.isChecked()

    def do(self):
        if self.button.isCheckable() and not self.button.isChecked():
            self.button.setText('Do it')
            self.contincheck.setEnabled(True)
        else:
            self.mythread.continuous = self.continuous
            if self.button.isCheckable() and self.button.isChecked():
                self.button.setText('Stop doing that')
                self.contincheck.setDisabled(True)

            self.mythread.start()

    @QtCore.pyqtSlot(int)
    def done(self, i):
        print('done it', i)

    @QtCore.pyqtSlot()
    def thread_finished(self):
        print('thread finished')


class MyThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(int)

    def __init__(self, continuous=False, parent=None):
        super(MyThread, self).__init__(parent)
        self._stopped = True
        self.continuous = continuous
        self.i = 0

    def __del__(self):
        self.wait()

    def stop(self):
        self._stopped = True

    def run(self):
        self._stopped = False
        while True:
            self.signal.emit(self.i)
            if self._stopped:
                break
            if self.continuous: 
                QtCore.QThread.sleep(2)
            else: 
                break


if __name__ == '__main__':
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    mainGui = MyWindow()
    mainGui.show()
    app.aboutToQuit.connect(app.deleteLater)
    app.exec_()

