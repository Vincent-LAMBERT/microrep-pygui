
import threading
import time
import os
from PyQt5.QtCore import pyqtSignal, Qt, QBuffer, QThread
from PyQt5.QtGui import QPixmap,QImage
import cv2
from microrep.core.utils import TRAJ_END, TRAJ_START, get_fmc_combination
from microrep.create_representations.create_representations.configuration_file import get_combinations_from_file
import PIL as pix
from PyQt5 import uic

from lxml import etree
import numpy as np

from widgets.image_viewer.ImageViewer import ImageViewer

from .HandDetection import create_detector, get_microgest_xml
from .DesignManagement import get_markers_tree, move_rep_markers, move_rep, stroke_to_path, family_resize
from .AppUtils import *
import time, numpy,cv2, subprocess, copy
import threading

# Classe QThread personnalisée pour la capture vidéo
class WebcamThread(QThread):
    image_data = pyqtSignal(np.ndarray)
    dic = get_microgest_xml()

    # Crating the variables
    back_pixmap = None
    markers_canva = None
    rep_canva = None
    command_canva = None
    
    tree = None
    frame_count = 0
    resize_done = False
    markers_tree = None
    
    detector = create_detector()
    dic = get_microgest_xml()
    
    def __init__(self, live_compute, frame_rate=60, frame_skip=1, mp_result_max_size=3):
        super(WebcamThread, self).__init__()
        self.is_running = True
        
        self.lc = live_compute
        self.frame_rate = frame_rate
        self.frame_skip = frame_skip
        
        # Création des labels
        self.label_live_file = ImageViewer()
        self.label_markers = ImageViewer()
        self.label_rep = ImageViewer()
        self.label_commands = ImageViewer()

        # Creation de la liste des mp_results et de sa taille max
        # (pour fluidification de la détection)
        self.mp_result_list = []
        self.mp_result_max_size = mp_result_max_size

    def run(self):
        cap = cv2.VideoCapture(0)
        prev = 0
        while cap.isOpened() and self.is_running:
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
                # print(f"Image shape : {image.shape}")
                self.image_data.emit(image)
        self.quit()
    
    def stop(self):
        self.is_running = False

    def start(self) -> None:
        self.image_data.connect(self.update_image)
        self.setTerminationEnabled(True)
        super().start()

    #####################################################
    ############## UPDATE FUNCTIONS #####################
    #####################################################

    # Fonction gerant la mise a jour de l'affichage
    def update_image(self, image):
        print("update")
        if not self.resize_done :
            self.lc.resizeDesign(image)
            self.resize_done = True

        back_thread = threading.Thread(target=self.update_background, args=(image,))
        back_thread.start()

        if self.frame_count % (self.frame_skip+1) == 0 :
            reduced_image = cv2.resize(image, (0, 0), fx=0.1, fy=0.1)
            thread = threading.Thread(target=self.update_all, args=(reduced_image,))
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

    def update_all(self, image):
        mp_results = self.lc.detect(image)

        if mp_results.hand_landmarks != [] :
            markers_tree = self.update_markers(mp_results)

            rep_tree = self.lc.copyDesign()
            new_rep_tree = self.update_representation(rep_tree, self.lc.fmc_combinations, markers_tree)
            # self.update_commands(rep_tree, combi)
        else :
            self.markers_canva = None
            self.rep_canva = None

    def update_markers(self, mp_results):
        markers_tree = get_markers_tree()
        resized_tree = family_resize(markers_tree, mp_results, self.lc.img_height, self.lc.img_width)

        tree = move_rep_markers(mp_results, resized_tree, self.lc.img_height, self.lc.img_width, self.dic)
        
        self.markers_canva = svg_to_pixmap(tree, self.lc.img_height, self.lc.img_width)
        return tree

    def update_representation(self, rep_tree, combi, markers_tree):
        new_rep_tree = move_rep(rep_tree, markers_tree, combi)
        svg_tree = stroke_to_path(new_rep_tree, markers_tree, combi)
        
        self.rep_canva = svg_to_pixmap(svg_tree, self.lc.img_height, self.lc.img_width)
        return new_rep_tree

    def update_commands(self):
        pass

    def update_labels(self):
        self.label_live_file.setPixmap(self.back_pixmap)
        self.label_markers.setPixmap(self.markers_canva)
        self.label_rep.setPixmap(self.rep_canva)