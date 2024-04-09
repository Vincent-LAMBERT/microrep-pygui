
import threading
import time
import os
from PySide6.QtCore import Signal, Qt, QBuffer, QThread
from PySide6.QtGui import QPixmap,QImage
import cv2
from microrep.core.utils import TRAJ_END, TRAJ_START, get_fmc_combination
from microrep.create_representations.create_representations.configuration_file import get_combinations_from_file
import PIL as pix

from lxml import etree
import numpy as np

from widgets.image_viewer.ImageViewer import ImageViewer

from .HandDetection import get_microgest_xml
from .DesignManagement import get_markers_tree, move_rep_markers, move_rep, stroke_to_path
from .AppUtils import *
import time, numpy,cv2, subprocess, copy
import threading

from PySide6.QtCore import QLibraryInfo

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.path(QLibraryInfo.PluginsPath)
os.environ["QT_LOGGING_RULES"] = '*.debug=false;qt.accessibility.cache.warning=false;qt.qpa.events.warning=false;qt.qpa.fonts.warning=false;qt.qpa.gl.warning=false;qt.qpa.input.devices.warning=false;qt.qpa.screen.warning=false;qt.qpa.xcb.warning=false;qt.text.font.db.warning=false;qt.xkb.compose.warning=false'

class WebcamThread(QThread):
    image_data = Signal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.cap = None
        
        self.fps = 0
        
    def set_fps(self, fps):
        self.fps = fps

    def run(self):        
        while self._run_flag:
            fps_list = []
            if self.cap != None and self.cap.isOpened():
                ret, cv_img = self.cap.read()
                if ret:
                    
                    # cv_img.flags.writeable = False
                    # cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
                    # # Upscale the image by 450%
                    # cv_img = cv2.resize(cv_img, None, fx=2.28, fy=2.28, interpolation=cv2.INTER_LANCZOS4)
                    # Flip the image horizontally
                    # cv_img = cv2.flip(cv_img, 1)

                    # # font which we will be using to display FPS 
                    # font = cv2.FONT_HERSHEY_SIMPLEX 
                
                    # # putting the FPS count on the frame 
                    # cv2.putText(cv_img, str(int(self.fps)), (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA) 

                    self.image_data.emit(cv_img)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.stopWebcam()
        self.wait()

    def stopWebcam(self):
        if self.cap!=None and self.cap.isOpened():
            self.cap.release()
        # else:
        #     raise Exception("Cannot stop webcam, it is not running")

    def startWebcam(self):
        self.cap = cv2.VideoCapture(0)

    def resetComputing(self):
        pass


    