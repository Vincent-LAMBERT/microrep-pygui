# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform
import cv2

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        
        # On windows set to true
        if platform.system() == 'Windows':
            Settings.ENABLE_CUSTOM_TITLE_BAR = True
        # On mac or linux set to false
        else : 
            Settings.ENABLE_CUSTOM_TITLE_BAR = False

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "µRep-PyGUI"
        # APPLY TEXTS
        self.setWindowTitle(title)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_generator.clicked.connect(self.buttonClick)
        widgets.btn_classic.clicked.connect(self.buttonClick)
        widgets.btn_webcam.clicked.connect(self.buttonClick)
        widgets.btn_exp.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # START CUSTOM FUNCTIONS
        # ///////////////////////////////////////////////////////////////
        AppFunctions.appStartUp(self)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home_page)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW GENERATOR PAGE
        if btnName == "btn_generator":
            widgets.stackedWidget.setCurrentWidget(widgets.generator_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        # SHOW CLASSIC DEMO PAGE
        if btnName == "btn_classic":
            widgets.stackedWidget.setCurrentWidget(widgets.classic_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WEBCAM DEMO PAGE
        if btnName == "btn_webcam":
            widgets.stackedWidget.setCurrentWidget(widgets.webcam_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
            
            self.microrep_thread.set_config("live_config.csv")
            self.microrep_thread.recompute_design()
            self.webcam_thread.restartLive()
        else :
            self.webcam_thread.stopLive()

        # SHOW EXPERIMENT PAGE
        if btnName == "btn_exp":
            widgets.stackedWidget.setCurrentWidget(widgets.experiment_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPosition().toPoint()
            
    @Slot(QImage)
    def runWebCam(self, idx):
        self.idx = idx
        combo = self.sender()
        print(f"Selected the variable {idx} from combo {combo.id_number}")
        self.th.start()

    @Slot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))
    
    def getAvailableCameras(self):
        cameras = QMediaDevices.videoInputs()
        for cameraDevice in cameras:
            self.availableCameras.append(cameraDevice.description())


class Thread(QThread):
    updateFrame = Signal(QImage)
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.status = True
        self.cap = True

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.status:
            ret, frame = self.cap.read()
            if not ret:
                continue
            h, w, ch = frame.shape
            img = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
            scaled_img = img.scaled(640, 480, Qt.KeepAspectRatio)
            # Emit signal
            self.updateFrame.emit(scaled_img)
        sys.exit(-1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("resources/images/images/microRep.png"))
    window = MainWindow()
    sys.exit(app.exec())
