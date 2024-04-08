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
from modules.utils.MicroRepThread import MicroRepThread
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

        self.microrep_thread = MicroRepThread(running_info=self.ui.runningInfo)
        
        # self.webcam_thread = WebcamThread(self.ui, microrep_compute=self.microrep_thread, frame_rate=60, frame_skip=2)
        self.webcam_thread = WebcamThread()
        self.webcam_thread.image_data.connect(self.ui.webcam.update_image)
        self.webcam_thread.start()

        # Set to home page
        self.ui.stackedWidget.setCurrentWidget(self.ui.home_page)

        # Give the ui to the children widgets
        self.ui.generator.configure(self.ui, self.microrep_thread)
        self.ui.exporter.configure(self.ui, self.microrep_thread)
        self.ui.webcam.configure(self.ui, self.microrep_thread, self.webcam_thread)

        # self.setWindowTitle("Qt live label demo")
        # self.disply_width = 640
        # self.display_height = 480
        # # create the label that holds the image
        # self.image_label = QLabel(self)
        # self.image_label.resize(self.disply_width, self.display_height)
        # # create a text label
        # self.textLabel = QLabel('Webcam')

        # # create a vertical box layout and add the two labels
        # vbox = QVBoxLayout()
        # vbox.addWidget(self.image_label)
        # vbox.addWidget(self.textLabel)
        # # set the vbox layout as the widgets layout
        # # self.setLayout(vbox)

        # # create the video capture thread
        # self.thread = VideoThread()
        # # connect its signal to the update_image slot
        # self.thread.change_pixmap_signal.connect(self.update_image)
        # # start the thread
        # self.thread.start()

        # self.show()