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
from main import *
from modules.utils.AppUtils import TEMP_FOLDER_PATH, createFolder, deleteFolder
from modules.utils.LiveCompute import LiveCompute
from modules.utils.WebcamThread import WebcamThread

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
        self.ui.tableWidget.setStyleSheet("QScrollBar:vertical { background: #6272a4; } QScrollBar:horizontal { background: #6272a4; }")
        self.ui.scrollArea.setStyleSheet("QScrollBar:vertical { background: #6272a4; } QScrollBar:horizontal { background: #6272a4; }")
        self.ui.comboBox.setStyleSheet("background-color: #6272a4;")
        self.ui.horizontalScrollBar.setStyleSheet("background-color: #6272a4;")
        self.ui.verticalScrollBar.setStyleSheet("background-color: #6272a4;")
        self.ui.commandLinkButton.setStyleSheet("color: #8de4ee;")

    def addLiveThreads(self) :
        # # Create the temp folder (erase the old one if it exists)
        # deleteFolder(TEMP_FOLDER_PATH)
        # createFolder(TEMP_FOLDER_PATH)

        # live_compute = LiveCompute("live_config.csv")
        # self.video_thread = WebcamThread(live_compute=live_compute, frame_rate=30, frame_skip=2)
        
        # # Permet la superposition des labels/images
        # frame_layout = self.ui.webcam.layout()
        # frame_layout.addWidget(self.video_thread.label_live_file,0,0)
        # frame_layout.addWidget(self.video_thread.label_markers,0,0)
        # frame_layout.addWidget(self.video_thread.label_rep,0,0)
        # frame_layout.addWidget(self.video_thread.label_commands,0,0)

        # self.video_thread.start()

        print("Threads started")