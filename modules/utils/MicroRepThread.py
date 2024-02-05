
import threading
import time
import os
from PySide6.QtCore import Signal, Qt, QBuffer, QThread
from PySide6.QtGui import QPixmap,QImage
import cv2
from microrep.core.utils import TRAJ_END, TRAJ_START, get_fmc_combination, get_combination_from_name
from microrep.create_representations.create_representations.configuration_file import get_combinations_from_file
import PIL as pix

from lxml import etree
import numpy as np

from .HandDetection import create_detector, input_treatement, update_mp_results
from .DesignManagement import family_resize, move_rep, move_rep_markers, read_file, stroke_to_path, write_file, remove_invisible_layers, get_markers_tree
from .AppUtils import *


import time, numpy,cv2, subprocess, copy
import threading

class MicroRepThread(QThread):

    resized_done = False
    detector = create_detector()
    fmc_combinations = None
    rep_tree = None

    def __init__(self, running_info=None, mp_result_max_size=3):
        super(MicroRepThread, self).__init__()
        # Creation de la liste des mp_results et de sa taille max
        # (pour fluidification de la détection)
        self.mp_result_list = []
        self.mp_result_max_size = mp_result_max_size

        self.running_info = running_info

    def set_config(self, config_file):
        # Check if absolute path
        if os.path.isabs(config_file):
            self.config_path = config_file
        else:
            self.config_path = get_config(config_file)
        combinations = get_combinations_from_file(self.config_path)
        self.fmc_combinations = get_fmc_combination(combinations)

    def update_running_info(self):
        label = f"Running threads : {threading.active_count()}"
        self.running_info.setText(label)

    def recompute_design(self):
        tree = get_markers_tree()

        # Check if the path exists
        if os.path.exists(TEMP_REP_FOLDER_PATH):
            deleteFolder(TEMP_REP_FOLDER_PATH)
        createFolder(TEMP_REP_FOLDER_PATH)

        write_file(tree, TEMP_FILE_PATH)
        # Export the representations with the dedicated module
        export_representations(self.config_path)

        base_tree = read_file(TEMP_REP_FILE_PATH)
        self.base_tree = remove_invisible_layers(base_tree)

    def update_markers(self, mp_results, dic, img_height, img_width):
        markers_tree = get_markers_tree()
        resized_tree = family_resize(markers_tree, mp_results, img_height, img_width)

        tree = move_rep_markers(mp_results, resized_tree, img_height, img_width, dic)
        pixmap = svg_to_pixmap(tree, img_height, img_width)
        return tree, pixmap

    def update_representation(self, rep_tree, markers_tree, combi, img_height, img_width):
        new_rep_tree = move_rep(rep_tree, markers_tree, combi)

        tree = stroke_to_path(new_rep_tree, markers_tree, combi)
        pixmap = svg_to_pixmap(tree, img_height, img_width)
        return tree, pixmap

    def update_commands(self):
        pass

    #####################################################
    ############## UPDATE FUNCTIONS #####################
    #####################################################

    def resize_design(self, image):
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
    
    def copy_design(self):
        # Copy the representation tree
        random_int = np.random.randint(0, 100000)
        write_file(self.base_tree, TEMP_AT_FILE_PATH+str(random_int))
        rep_tree = read_file(TEMP_AT_FILE_PATH+str(random_int))
        os.remove(TEMP_AT_FILE_PATH+str(random_int))

        return rep_tree
    
    def getRep(self, index):
        files = os.listdir(TEMP_REP_FOLDER_PATH)
        file = files[index%len(files)]
        file_path = TEMP_REP_FOLDER_PATH+file

        fmc_combination = get_combination_from_name(file)
        # fmc_combination = None

        return read_file(file_path), fmc_combination

def export_representations(config_path, export_filetype="svg", dpi=90, traces=False, show_command=False, one_family=False, four_gesture=False, debug=False, dry=False, prefix="export_") :
    path_str = f"--path={TEMP_REP_FOLDER_PATH}"
    filetype_str = f"--filetype={export_filetype}"
    dpi_str = f"--dpi={dpi}"
    traces_str = f"--traces={traces}"
    command_str = f"--command={show_command}"
    one_str = f"--one={one_family}"
    four_str = f"--four={four_gesture}"
    debug_str = f"--debug={debug}"
    dry_str = f"--dry={dry}"
    prefix_str = f"--prefix={prefix}"
    config_str = f"--config={config_path}"
    
    export_rep = CreateRepresentations()
    export_rep.run(args=[TEMP_FILE_PATH, path_str, filetype_str, dpi_str, traces_str, command_str, one_str, four_str, debug_str, dry_str, prefix_str, config_str])

    # Copy a random file in TEMP_REP_FOLDER_PATH to TEMP_REP_FILE_PATH
    index = random.randint(0, len(os.listdir(TEMP_REP_FOLDER_PATH))-1)
    random_file_name = os.listdir(TEMP_REP_FOLDER_PATH)[index]
    
    if os.path.exists(TEMP_REP_FILE_PATH) :
        os.remove(TEMP_REP_FILE_PATH)
    os.rename(TEMP_REP_FOLDER_PATH+random_file_name, TEMP_REP_FILE_PATH)
    
    # family_name = "AandB"
    # # Keep the one and only file in TEMP_REP_FOLDER_PATH with the family_name in its name
    # for file in os.listdir(TEMP_REP_FOLDER_PATH) :
    #     if not family_name in file :
    #         os.remove(TEMP_REP_FOLDER_PATH+file)
    #     else :
    #         if os.path.exists(TEMP_REP_FILE_PATH) :
    #             os.remove(TEMP_REP_FILE_PATH)
    #         os.rename(TEMP_REP_FOLDER_PATH+file, TEMP_REP_FILE_PATH)

