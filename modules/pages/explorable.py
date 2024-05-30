from argparse import ArgumentParser
import base64

import numpy as np
from main import *
import threading

import modules.utils.HandDetection as hd
import modules.utils.DesignManagement as dm
import modules.utils.AppUtils as u
from lxml import etree
from PySide6.QtGui import QPixmap,QImage
from modules.utils.AppUtils import get_config, svg_to_pixmap
from microrep.core.export import export
from microrep.create_representations.create_representations import CreateRepresentations
from modules.utils.MicroRepThread import resize_tree
import microglyph.micro_glyph_detector as mgd

from microrep.create_representations.create_representations.configuration_file import get_combination_from_row
from PySide6.QtCore import Slot

from microrep.core.utils import get_fmc_combination, get_combination_name

HandPose = mgd.MicroGlyphDetector.Detection.HandPose
WristOrientation = mgd.MicroGlyphDetector.Detection.WristOrientation


class Explorable(QWidget) :
    prefix="export_"
    
    dic = hd.get_microgest_xml()

    def __init__(self, parent=None) :
        super().__init__(parent)

        with open(u.get_config("default_config.csv"), "r") as config_file :
            self.list_config = config_file.read().split("\n")

        self.families = ["AandB", "MaS"]

        self.page_is_active = False
        self.filename = None
        self.hand_pose_img = None

    def configure(self, ui, microrep_thread, webcam_thread) :
        self.ui = ui
        self.mgc = microrep_thread
        self.wt = webcam_thread

        self.ui.comboBox_explorable_family.addItems(self.families)
        self.ui.comboBox_explorable_config.addItems(self.list_config)

        webcam_thread.image_data.connect(self.update_image)

    def recompute_config(self) :
        config = self.ui.comboBox_explorable_config.currentText()
        with open(get_config("live_config.csv"), "w") as config_file :
            config_file.write(config)
        self.mgc.set_config("live_config.csv")

    def start(self) :
        self.page_is_active = True
    
    def stop(self) :
        self.page_is_active = False

    ################################################################
    #################### SLOT FUNCTIONS ############################
    ################################################################
        
    def selectFamily(self) :
        self.selectActive()
    
    def selectMapping(self) :
        self.recompute_config()
        self.selectActive()

    def selectActive(self) :
        selected_family = self.ui.comboBox_explorable_family.currentText()
        selected_mapping = self.ui.comboBox_explorable_config.currentText()

        if selected_family and selected_mapping :
            selected_mapping = selected_mapping.split(",")
            combinations = get_combination_from_row(selected_mapping)
            mapping_name = get_combination_name(combinations)

            self.active = f"{self.prefix}{selected_family}_{mapping_name}.svg"
            
            self.mgc.set_active(self.active)
            self.wt.resetComputing()
            
    ################################################################
    ####################  VIDEO FUNCTIONS  #########################
    ################################################################

    @Slot(np.ndarray)
    def update_image(self, triplet):
        """Updates the image_label with a new opencv image"""
        hand_landmarks, hand_pose, wrist_orientation = triplet

        if self.page_is_active :
            # qt_img = self.convert_cv_qt(image)
            # self.ui.label_explorable_live_file.setPixmap(qt_img)
            
            back_thread = threading.Thread(target=self.update_hand_pose, args=(hand_landmarks, hand_pose, wrist_orientation,))
            back_thread.start()

            labels_thread = threading.Thread(target=self.update_labels)
            labels_thread.start()
            
            self.mgc.update_running_info()

    def update_hand_pose(self, hand_landmarks, hand_pose, wrist_orientation):
        """
        Compute the hand pose and update the hand_pose_img attribute
        """
        if hand_landmarks != []:
            # hand_pose = HandPose(hand_landmarks)
            # wrist_orientation = WristOrientation(hand_landmarks)

            filename = hd.get_hand_pose_file_name(wrist_orientation, hand_pose)
            if filename != self.filename:
                self.filename = filename
                image = QImage("resources/images/hand_poses/" + self.filename)
                print(f"filename: {filename} | image: {image}")
                self.hand_pose_img = QPixmap(image)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        if cv_img is None:
            return None
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        # p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        # return QPixmap.fromImage(p)
        return QPixmap.fromImage(convert_to_Qt_format)
    
    
    def update_labels(self):
        # hand_pose_pixmap = self.convert_cv_qt(image)
        if self.hand_pose_img is not None:
            self.ui.label_explorable_live_file.setPixmap(self.hand_pose_img)