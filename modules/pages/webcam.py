from argparse import ArgumentParser
import base64

import numpy as np
from main import *
import threading

import modules.utils.HandDetection as hd
from PySide6.QtGui import QPixmap,QImage
import modules.utils.DesignManagement as dm
import modules.utils.AppUtils as u
from lxml import etree
from modules.utils.AppUtils import get_config, svg_to_pixmap
from microrep.core.export import export
from microrep.create_representations.create_representations import CreateRepresentations
from modules.utils.MicroRepThread import resize_tree

from microrep.create_representations.create_representations.configuration_file import get_combination_from_row
from PySide6.QtCore import Slot

from microrep.core.utils import get_fmc_combination, get_combination_name

TREE = "tree"
PIXMAP = "pixmap"
NAME = "name"

class Webcam(QWidget) :
    prefix="export_"
    
    dic = hd.get_microgest_xml()

    def __init__(self, parent=None) :
        super().__init__(parent)

        with open(u.get_config("default_config.csv"), "r") as config_file :
            self.list_config = config_file.read().split("\n")

        self.families = ["AandB", "MaS"]


        # Webcam variables
        self.page_is_active = False
        self.first_computed = False

        self.back_image_cv = None
        self.markers_svg_tree = None
        self.rep_svg_tree = None
        self.command_svg_tree = None
        
        self.tree = None
        self.frame_count = 0
        self.markers_tree = None
        
        self.mp_result_list = []
        self.mp_result_max_size = 3

    def configure(self, ui, microrep_thread, webcam_thread) :
        self.ui = ui
        self.mgc = microrep_thread
        self.wt = webcam_thread

        self.ui.comboBox_family.addItems(self.families)
        self.ui.comboBox_config.addItems(self.list_config)

        # webcam_thread.image_data.connect(self.update_image)

    def recompute_config(self) :
        config = self.ui.comboBox_config.currentText()
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
        selected_family = self.ui.comboBox_family.currentText()
        selected_mapping = self.ui.comboBox_config.currentText()

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

    # @Slot(np.ndarray)
    # def update_image(self, cv_img):
    #     """Updates the image_label with a new opencv image"""
    #     qt_img = self.convert_cv_qt(cv_img)
    #     self.ui.label_live_file.setPixmap(qt_img)
    
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
    

    ################################################################


    # Fonction gerant la mise a jour de l'affichage
    @Slot(np.ndarray)
    def update_image(self, image):
        if self.page_is_active :
            back_thread = threading.Thread(target=self.update_background, args=(image,))
            back_thread.start()

            if self.frame_count % 2 == 0 :
                thread = threading.Thread(target=self.update_all, args=(image, 0.1))
                thread.start()        

            labels_thread = threading.Thread(target=self.update_labels)
            labels_thread.start()

            self.mgc.update_running_info()

            self.frame_count += 1

    def update_background(self, image):
        # time.sleep(0.2) # Makes the background update coincide with the markers update
        if not self.first_computed :
            self.mgc.update_frame_size(image)
            self.first_computed = True

        self.back_image_cv = image

    def update_all(self, image, ratio=0.1):

        # reduced_image = cv2.resize(image, (0, 0), fx=ratio, fy=ratio)

        hand_landmarks = self.mgc.process_stream(image)

        if hand_landmarks != [] :
            self.markers_svg_tree = self.mgc.update_markers(hand_landmarks, self.dic, self.mgc.img_height, self.mgc.img_width)

            rep_tree = self.mgc.copy_design()
            self.rep_svg_tree = self.mgc.update_representation(rep_tree, self.markers_svg_tree, self.mgc.fmc_combinations, self.mgc.img_height, self.mgc.img_width)
            # self.update_commands(rep_tree, combi)
        else :
            self.markers_svg_tree = None
            self.rep_svg_tree = None

    def update_labels(self):
        
        # back_canva = self.convert_cv_qt(self.back_image_cv)
        # markers_canva = self.convert_cv_qt(self.markers_svg)
        # rep_canva = self.convert_cv_qt(self.rep_svg)

        # self.ui.label_live_file.setPixmap(back_canva)
        # self.ui.label_markers.setPixmap(markers_canva)
        # self.ui.label_rep.setPixmap(rep_canva)

        # thread = threading.Thread(target=self.convert_to_qt, args=([self.back_image_cv, self.markers_svg, self.rep_svg], [self.ui.label_live_file, self.ui.label_markers, self.ui.label_rep]))
        # thread.start()


        back_pixmap = self.convert_cv_qt(self.back_image_cv)
        self.ui.label_live_file.setPixmap(back_pixmap)
        
        if self.rep_svg_tree != None :
            markers_pixmap = svg_to_pixmap(self.markers_svg_tree, self.mgc.img_height, self.mgc.img_width)
            self.ui.label_markers.setPixmap(markers_pixmap)
        
        if self.rep_svg_tree != None :
            rep_pixmap = svg_to_pixmap(self.rep_svg_tree, self.mgc.img_height, self.mgc.img_width)
            self.ui.label_rep.setPixmap(rep_pixmap)

        # cv2.imshow("rep_image", self.rep_svg)
