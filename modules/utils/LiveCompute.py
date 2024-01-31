
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

from .HandDetection import create_detector, input_treatement, update_mp_results
from .DesignManagement import read_file, write_file, remove_invisible_layers, export_representations, get_markers_tree
from .AppUtils import *


import time, numpy,cv2, subprocess, copy
import threading

class LiveCompute(QThread):

    resized_done = False
    detector = create_detector()
    fmc_combinations = None
    rep_tree = None

    def __init__(self, config_file_name, running_info=None, mp_result_max_size=3):
        super(LiveCompute, self).__init__()

        self.config_path = getConfig(config_file_name)
        combinations = get_combinations_from_file(self.config_path)
        self.fmc_combinations = get_fmc_combination(combinations)

        # Compute the design
        self.compute_design()

        # Creation de la liste des mp_results et de sa taille max
        # (pour fluidification de la détection)
        self.mp_result_list = []
        self.mp_result_max_size = mp_result_max_size

        self.running_info = running_info

    def update_running_info(self):
        label = f"Running threads : {threading.active_count()}"
        self.running_info.setText(label)

    def compute_design(self):
        tree = get_markers_tree()

        # Check if the path exists
        if os.path.exists(TEMP_LIVE_FOLDER_PATH):
            deleteFolder(TEMP_LIVE_FOLDER_PATH)
        createFolder(TEMP_LIVE_FOLDER_PATH)
        write_file(tree, TEMP_FILE_PATH)
        export_representations(self.config_path)

        base_tree = read_file(TEMP_REP_FILE_PATH)
        self.base_tree = remove_invisible_layers(base_tree)

    #####################################################
    ############## UPDATE FUNCTIONS #####################
    #####################################################

    def resizeDesign(self, image):
        self.img_height, self.img_width, channel = image.shape
        self.base_tree.getroot().attrib["width"] = f"{self.img_width}"
        self.base_tree.getroot().attrib["height"] = f"{self.img_height}"
        self.base_tree.getroot().attrib["viewBox"] = f"0 0 {self.img_width} {self.img_height}"

    def detect(self, image):
        image_numpy, mp_results = input_treatement(image, self.detector)

        # Scale the image to the self.img_height and self.img_width
        image_numpy = cv2.resize(image_numpy, (self.img_width, self.img_height), interpolation=cv2.INTER_LANCZOS4)
        
        # Ensure that a hand is detected
        if mp_results.hand_landmarks != [] :
            mp_results = update_mp_results(mp_results, self.mp_result_list, self.mp_result_max_size) # Ensure stability whereas the more stable the representation, the more the delay because of the multiple detections (a max size of 3 is fine)

        return mp_results
    
    def copyDesign(self):
        # Copy the representation tree
        random_int = np.random.randint(0, 100000)
        write_file(self.base_tree, TEMP_AT_FILE_PATH+str(random_int))
        rep_tree = read_file(TEMP_AT_FILE_PATH+str(random_int))
        os.remove(TEMP_AT_FILE_PATH+str(random_int))

        return rep_tree
