
import threading
import time
import os
import svgutils.transform as sg
from PySide6.QtCore import Signal, Qt, QBuffer, QThread
from PySide6.QtGui import QPixmap,QImage
import cv2
from microrep.core.utils import TRAJ_END, TRAJ_START, get_fmc_combination, get_combination_from_name
from microrep.create_representations.create_representations.configuration_file import get_combinations_from_file
import PIL as pix

from lxml import etree
import numpy as np

from .HandDetection import create_detector, input_treatement, update_mp_results
from .DesignManagement import apply_transforms, flip_tree, get_resize_ratio, move_rep, move_rep_markers, read_file, scale_children, stroke_to_path, write_file, remove_invisible_layers, get_markers_tree
from .AppUtils import *


import time, numpy,cv2, subprocess, copy
import threading

class MicroRepThread(QThread):

    detections = 0
    detector = create_detector()
    fmc_combinations = None
    rep_tree = None
    resized_tree = None

    active = None

    def __init__(self, running_info=None, detections_max_size=3):
        super(MicroRepThread, self).__init__()
        # Creation de la liste des mp_results et de sa taille max
        # (pour fluidification de la détection)
        self.detected_hands_list = []
        self.detections_max_size = detections_max_size

        self.running_info = running_info
        # self.tracker = FingersTracker()

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

    def set_active(self, active):
        self.active = active
        self.recompute_design()

    def recompute_design(self):
        tree = get_markers_tree()

        # Check if the path exists
        if os.path.exists(TEMP_REP_FOLDER_PATH):
            deleteFolder(TEMP_REP_FOLDER_PATH)
        createFolder(TEMP_REP_FOLDER_PATH)

        write_file(tree, TEMP_FILE_PATH)
        # Export the representations with the dedicated module
        export_representations(self.config_path)

        # Select the first file
        if self.active not in os.listdir(TEMP_REP_FOLDER_PATH):
            self.active = os.listdir(TEMP_REP_FOLDER_PATH)[0]
    
        if os.path.exists(TEMP_REP_FILE_PATH) :
            os.remove(TEMP_REP_FILE_PATH)
        os.rename(TEMP_REP_FOLDER_PATH+self.active, TEMP_REP_FILE_PATH)

        self.detections = 0

        # self.base_tree = remove_invisible_layers(base_tree)

        self.base_tree_left = read_file(TEMP_REP_FILE_PATH)

        self.base_tree_right = read_file(TEMP_REP_FILE_PATH)
        self.base_tree_right = flip_tree(self.base_tree_right)
        self.base_tree_right = apply_transforms(self.base_tree_right)
        
        self.base_tree = self.base_tree_left

    def update_markers(self, hand_landmarks, dic, img_height, img_width):
        markers_tree = get_markers_tree()
        markers_tree = resize_tree(markers_tree, img_height, img_width)
        tree = move_rep_markers(hand_landmarks, markers_tree, img_height, img_width, dic)

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

    def update_frame_size(self, image):
        self.img_height, self.img_width, channel = image.shape
        resize_tree(self.base_tree_left, self.img_height, self.img_width)
        resize_tree(self.base_tree_right, self.img_height, self.img_width)

    def detect(self, image):

        image_numpy, mp_results = input_treatement(image, self.detector)
        
        # mp_results = self.tracker.landmark_finder(image)
        self.detections += 1

        # # Scale the image to the self.img_height and self.img_width
        # image_numpy = cv2.resize(image_numpy, (self.img_width, self.img_height), interpolation=cv2.INTER_LANCZOS4)

        hand_landmarks = self.get_hand_skeleton(mp_results)
        self.resize_design(hand_landmarks)

        return hand_landmarks

    def get_hand_skeleton(self, mp_results):
        # Ensure that a hand is detected
        if mp_results.hand_landmarks != [] :
        # if mp_results :
        #     # print(f"mp_results : {mp_results}")
        #     if mp_results.multi_hand_landmarks != [] :
            detected_hands = update_mp_results(mp_results, self.detected_hands_list, self.detections_max_size) # Ensure stability whereas the more stable the representation, the more the delay because of the multiple detections (a max size of 3 is fine)

            if detected_hands[LEFT] != [] and detected_hands[RIGHT] != [] :
                hand_landmarks = detected_hands[RIGHT]
                self.base_tree = self.base_tree_right
                write_file(self.base_tree, TEMP_DESIGN_FILE_PATH[:-4]+"right.svg")
            elif detected_hands[LEFT] == [] and detected_hands[RIGHT] != [] :
                hand_landmarks = detected_hands[RIGHT]
                self.base_tree = self.base_tree_right
                write_file(self.base_tree, TEMP_DESIGN_FILE_PATH[:-4]+"right.svg")
            elif detected_hands[LEFT] != [] and detected_hands[RIGHT] == [] :
                hand_landmarks = detected_hands[LEFT]
                self.base_tree = self.base_tree_left
                write_file(self.base_tree, TEMP_DESIGN_FILE_PATH[:-4]+"left.svg")
            else :
                hand_landmarks = []
        else :
            hand_landmarks = []
        # else :
        #     hand_landmarks = []

        return hand_landmarks
    
    def resize_design(self, hand_landmarks):
        if hand_landmarks != [] and (self.detections%5 == 0 or self.resized_tree==None):
            ratio = get_resize_ratio(self.base_tree, hand_landmarks)
            self.resized_tree = scale_children(self.base_tree, ratio)
            self.resized_tree = apply_transforms(self.resized_tree)

            write_file(self.resized_tree, TEMP_DESIGN_FILE_PATH)
    
    def copy_design(self):
        # Copy the representation tree
        random_int = np.random.randint(0, 100000)
        write_file(self.resized_tree, TEMP_COPY_FILE_PATH+str(random_int))
        rep_tree = read_file(TEMP_COPY_FILE_PATH+str(random_int))
        os.remove(TEMP_COPY_FILE_PATH+str(random_int))

        return rep_tree
    
    def getRep(self, index):
        files = os.listdir(TEMP_REP_FOLDER_PATH)
        file = files[index%len(files)]
        file_path = TEMP_REP_FOLDER_PATH+file

        tree = read_file(file_path)
        fmc_combination = get_combination_from_name(file)

        return tree, fmc_combination, file
    
#####################################################
################# UTILS FUNCTIONS ###################
#####################################################

def resize_tree(tree, img_height, img_width):
    tree.getroot().attrib["width"] = f"{img_width}"
    tree.getroot().attrib["height"] = f"{img_height}"
    tree.getroot().attrib["viewBox"] = f"0 0 {img_width} {img_height}"

    return tree

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

    # # Copy a random file in TEMP_REP_FOLDER_PATH to TEMP_REP_FILE_PATH
    # index = random.randint(0, len(os.listdir(TEMP_REP_FOLDER_PATH))-1)
    # random_file_name = os.listdir(TEMP_REP_FOLDER_PATH)[index]
    
    # family_name = "AandB"
    # # Keep the one and only file in TEMP_REP_FOLDER_PATH with the family_name in its name
    # for file in os.listdir(TEMP_REP_FOLDER_PATH) :
    #     if not family_name in file :
    #         os.remove(TEMP_REP_FOLDER_PATH+file)
    #     else :
    #         if os.path.exists(TEMP_REP_FILE_PATH) :
    #             os.remove(TEMP_REP_FILE_PATH)
    #         os.rename(TEMP_REP_FOLDER_PATH+file, TEMP_REP_FILE_PATH)

