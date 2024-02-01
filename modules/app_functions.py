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

# MAIN FILE
# ///////////////////////////////////////////////////////////////
import threading
import cv2
from main import *
from modules.utils.AppUtils import TEMP_FOLDER_PATH, createFolder, deleteFolder
from modules.utils.LiveCompute import LiveCompute
from modules.utils.WebcamThread import WebcamThread

from PySide6.QtMultimedia import QMediaDevices

# WITH ACCESS TO MAIN WINDOW WIDGETS
# ///////////////////////////////////////////////////////////////
class AppFunctions(MainWindow):
    def setThemeHack(self):
        Settings.BTN_LEFT_BOX_COLOR = "background-color: #495474;"
        Settings.BTN_RIGHT_BOX_COLOR = "background-color: #495474;"
        Settings.MENU_SELECTED_STYLESHEET = MENU_SELECTED_STYLESHEET = """
        border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgba(255, 121, 198, 255), stop:0.5 rgba(85, 170, 255, 0));
        background-color: #566388;
        """

        # SET MANUAL STYLES
        self.ui.lineEdit.setStyleSheet("background-color: #6272a4;")
        self.ui.pushButton.setStyleSheet("background-color: #6272a4;")
        self.ui.plainTextEdit.setStyleSheet("background-color: #6272a4;")
        self.ui.scrollArea.setStyleSheet("QScrollBar:vertical { background: #6272a4; } QScrollBar:horizontal { background: #6272a4; }")
        self.ui.comboBox.setStyleSheet("background-color: #6272a4;")
        self.ui.horizontalScrollBar.setStyleSheet("background-color: #6272a4;")
        self.ui.verticalScrollBar.setStyleSheet("background-color: #6272a4;")
        self.ui.commandLinkButton.setStyleSheet("color: #8de4ee;")
    
    def appStartUp(self) :
        # Create the temp folder (erase the old one if it exists)
        deleteFolder(TEMP_FOLDER_PATH)
        createFolder(TEMP_FOLDER_PATH)

        self.live_compute = LiveCompute("live_config.csv", running_info=self.ui.runningInfo)

        label_live_file = self.ui.label_live_file
        label_markers = self.ui.label_markers
        label_rep = self.ui.label_rep
        label_commands = self.ui.label_commands
        
        self.webcam_thread = WebcamThread(label_live_file, label_markers, label_rep, label_commands, live_compute=self.live_compute, frame_rate=30, frame_skip=2)

        # Set to home page
        self.ui.stackedWidget.setCurrentWidget(self.ui.home_page)