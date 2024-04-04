
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

# Classe QThread personnalisée pour la capture vidéo
class WebcamThread(QThread):
    is_running = True

    first_computed = False
    webcam_on = False

    image_data = Signal(np.ndarray)

    # Crating the variables
    back_pixmap = None
    markers_canva = None
    rep_canva = None
    command_canva = None
    
    tree = None
    frame_count = 0
    markers_tree = None
    
    dic = get_microgest_xml()
    
    def __init__(self, label_live_file, label_markers, label_rep, label_commands, microrep_compute, frame_rate=60, frame_skip=1, mp_result_max_size=3):
        super(WebcamThread, self).__init__()
        
        self.mgc = microrep_compute
        self.frame_rate = frame_rate
        self.frame_skip = frame_skip
        
        # Création des labels
        self.label_live_file = label_live_file
        self.label_markers = label_markers
        self.label_rep = label_rep
        self.label_commands = label_commands

        # Creation de la liste des mp_results et de sa taille max
        # (pour fluidification de la détection)
        self.mp_result_list = []
        self.mp_result_max_size = mp_result_max_size

        self.start()

    def run(self):
        cap = None
        while self.is_running :
            if self.webcam_on :
                # Turn the camera on
                cap = cv2.VideoCapture(0)
                prev = 0
                while cap.isOpened() and self.webcam_on:
                    self.mgc.update_running_info()
                    time_elapsed = time.time() - prev
                    success, image = cap.read()
                    if not success:
                        print("Ignoring empty camera frame.")
                        continue
                    if time_elapsed > 1./self.frame_rate:
                        prev = time.time()
                        image.flags.writeable = False
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        # Upscale the image by 450%
                        image = cv2.resize(image, None, fx=2.28, fy=2.28, interpolation=cv2.INTER_LANCZOS4)
                        # Flip the image horizontally
                        image = cv2.flip(image, 1)
                        self.image_data.emit(image)

                if cap.isOpened():
                    cap.release()
            else :
                self.mgc.update_running_info()
        # self.quit()

    def start(self) -> None:
        self.image_data.connect(self.update_image)
        self.setTerminationEnabled(True)
        super().start()

    def stop(self) -> None:
        self.is_running = False
    
    def stopLive(self):
        self.webcam_on = False
        print("Stopping the camera")

    def restartLive(self):
        self.webcam_on = True
        self.resetComputing()
    
    def resetComputing(self):
        self.first_computed = False

    #####################################################
    ############## UPDATE FUNCTIONS #####################
    #####################################################

    # Fonction gerant la mise a jour de l'affichage
    def update_image(self, image, ratio=0.1):
        if not self.first_computed :
            self.mgc.update_frame_size(image)
            self.first_computed = True

        back_thread = threading.Thread(target=self.update_background, args=(image,))
        back_thread.start()

        if self.frame_count % (self.frame_skip+1) == 0 :
            thread = threading.Thread(target=self.update_all, args=(image, ratio,))
            thread.start()

        self.update_labels()

        self.frame_count += 1

    def update_background(self, image):
        time.sleep(0.2) # Makes the background update coincide with the markers update
        img_height, img_width, channel = image.shape
        bytes_per_line = 3 * img_width
        q_image = QImage(image.data, img_width, img_height, bytes_per_line, QImage.Format_RGB888)
        if not q_image.isNull():
            self.back_pixmap = QPixmap.fromImage(q_image)
        else :
            self.back_pixmap = None

    def update_all(self, image, ratio=0.1):
        reduced_image = cv2.resize(image, (0, 0), fx=ratio, fy=ratio)

        hand_landmarks = self.mgc.process_stream(reduced_image)

        if hand_landmarks != [] :
            markers_tree, self.markers_canva = self.mgc.update_markers(hand_landmarks, self.dic, self.mgc.img_height, self.mgc.img_width)

            rep_tree = self.mgc.copy_design()
            new_rep_tree, self.rep_canva = self.mgc.update_representation(rep_tree, markers_tree, self.mgc.fmc_combinations, self.mgc.img_height, self.mgc.img_width)
            # self.update_commands(rep_tree, combi)
        else :
            self.markers_canva = None
            self.rep_canva = None

    def update_labels(self):
        self.label_live_file.setPixmap(self.back_pixmap)
        self.label_markers.setPixmap(self.markers_canva)
        self.label_rep.setPixmap(self.rep_canva)