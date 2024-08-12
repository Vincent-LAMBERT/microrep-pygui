from argparse import ArgumentParser
import base64

import numpy as np
from main import *
import threading

import modules.utils.HandDetection as hd
import modules.utils.DesignManagement as dm
import modules.utils.AppUtils as u
from lxml import etree
import microrep.core.utils as mrep
from PySide6.QtGui import QPixmap,QImage
from modules.utils.AppUtils import HAND_POSES_FOLDER_PATH, get_config, svg_to_pixmap
from microrep.core.export import export
from microrep.create_representations.create_representations import CreateRepresentations
from modules.utils.MicroRepThread import resize_tree
import microglyph.micro_glyph_detector as mgd

from microrep.create_representations.create_representations.configuration_file import get_combination_from_row
from PySide6.QtCore import Slot

from microrep.core.utils import get_fmc_combination, get_combination_name

from modules.utils.microgesture_detector.microglyph.micro_glyph import MicroGlyphEvent
from modules.utils.microgesture_detector.microglyph.micro_glyph_detector import FINGERS, THUMB

HandPose = mgd.MicroGlyphDetector.Detection.HandPose
WristOrientation = mgd.MicroGlyphDetector.Detection.WristOrientation


class Explorable(QWidget) :
    prefix="export_"
    FRAMES_DELAY=15
    dic = hd.get_microgest_xml()

    def __init__(self, parent=None) :
        super().__init__(parent)

        with open(u.get_config("default_config.csv"), "r") as config_file :
            self.list_config = config_file.read().split("\n")

        self.families = ["AandB", "MaS"]

        self.page_is_active = False
        self.filename = None
        self.hand_pose_img = None

    def configure(self, ui, microrep_thread, main_thread, second_thread, watch_server=None) :
        self.ui = ui
        self.mgc = microrep_thread

        self.ui.comboBox_explorable_family.addItems(self.families)
        self.ui.comboBox_explorable_config.addItems(self.list_config)

        self.main_thread = main_thread
        self.second_thread = second_thread
        self.watch_server = watch_server
        
        resultThread = threading.Thread(target=self.update_image, args=(main_thread, second_thread))
        resultThread.start()

    def recompute_config(self) :
        config = self.ui.comboBox_explorable_config.currentText()
        with open(get_config("live_config.csv"), "w") as config_file :
            config_file.write(config)
        self.mgc.set_config("live_config.csv")

    def start(self) :
        self.page_is_active = True
        self.main_thread.start_webcam()
        if self.second_thread!=None :
            self.second_thread.start_webcam()
    
    def stop(self) :
        self.page_is_active = False
        self.main_thread.stop_webcam()
        if self.second_thread!=None :
            self.second_thread.stop_webcam()

    ################################################################
    #################### SLOT FUNCTIONS ############################
    ################################################################
        
    def selectFamily(self) :
        # self.selectActive()
        pass
    
    def selectMapping(self) :
        # self.recompute_config()
        # self.selectActive()
        pass

    def selectActive(self) :
        selected_family = self.ui.comboBox_explorable_family.currentText()
        selected_mapping = self.ui.comboBox_explorable_config.currentText()

        if selected_family and selected_mapping :
            selected_mapping = selected_mapping.split(",")
            combinations = get_combination_from_row(selected_mapping)
            mapping_name = get_combination_name(combinations)

            self.active = f"{self.prefix}{selected_family}_{mapping_name}.svg"
            
            # self.mgc.set_active(self.active)
            # self.wt.resetComputing()
            
    ################################################################
    ####################  VIDEO FUNCTIONS  #########################
    ################################################################

    def update_image(self, thread1, thread2):
        """Updates the image_label with a new opencv image"""
        old_filename = None
        previous_frame_wo_hp = None
        count_frames_with_result = 0
        
        if thread2 == None:
            while thread1.is_alive():
                result1 = thread1.results
                if result1 != None:
                    wo1, co1, hp1 = result1
                    wo_hp = (wo1, hp1)
                    old_filename = self.load_image(wo_hp, previous_frame_wo_hp, count_frames_with_result, old_filename)
        else :
            while thread1.is_alive() and thread2.is_alive():
                result1, result2 = thread1.results, thread2.results
                if result1 != None and result2 != None:
                    wo_hp = mergeResults(result1, result2)
                    old_filename = self.load_image(wo_hp, previous_frame_wo_hp, count_frames_with_result, old_filename)
    
    def load_image(self, result):
        # Handle thumb too close to fingers cases:
        if result[1].finger_states[THUMB] == mrep.CLOSE:
            result = previous_frame_result
            count_frames_with_result = 0
        
        if previous_frame_result != result:
            count_frames_with_result = 0
        else:
            count_frames_with_result += 1
        
        if count_frames_with_result > self.FRAMES_DELAY:
            # Corrected orientation gives the orient for the filename
            filename = hd.get_hand_pose_file_name(*result)
            
            if filename!=None and (old_filename==None or old_filename!=filename):
                old_filename = filename
                if self.watch_server != None:
                    self.watch_server.send_data(f"[FILENAME] {filename}")
                
                # print(f"Filename: {filename}")
                # Loads the image
                svg_data = etree.parse(HAND_POSES_FOLDER_PATH+filename)
                svg_tree_as_string = etree.tostring(svg_data)
                
                self.ui.widget_svg.load(svg_tree_as_string)
                
        previous_frame_result = result
        time.sleep(0.01)
        return old_filename
    
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
                
CALIBRATION_EQUIVALENT = {(WristOrientation.FRONT, WristOrientation.LEFT): WristOrientation.FRONT_LEFT,
                          (WristOrientation.FRONT, WristOrientation.RIGHT): WristOrientation.FRONT_RIGHT,
                          (WristOrientation.FRONT, WristOrientation.FRONT_LEFT): WristOrientation.FRONT_LEFT,
                          (WristOrientation.FRONT, WristOrientation.FRONT_RIGHT): WristOrientation.FRONT_RIGHT,
                          (WristOrientation.BACK, WristOrientation.LEFT): WristOrientation.BACK_LEFT,
                          (WristOrientation.BACK, WristOrientation.RIGHT): WristOrientation.BACK_RIGHT,
                          (WristOrientation.BACK, WristOrientation.BACK_LEFT): WristOrientation.BACK_LEFT,
                          (WristOrientation.BACK, WristOrientation.BACK_RIGHT): WristOrientation.BACK_RIGHT,
                          (WristOrientation.LEFT, WristOrientation.FRONT): WristOrientation.FRONT_LEFT,
                          (WristOrientation.LEFT, WristOrientation.BACK): WristOrientation.BACK_LEFT,
                          (WristOrientation.LEFT, WristOrientation.FRONT_LEFT): WristOrientation.FRONT_LEFT,
                          (WristOrientation.LEFT, WristOrientation.BACK_LEFT): WristOrientation.BACK_LEFT,
                          (WristOrientation.RIGHT, WristOrientation.FRONT): WristOrientation.FRONT_RIGHT,
                          (WristOrientation.RIGHT, WristOrientation.BACK): WristOrientation.BACK_RIGHT,
                          (WristOrientation.RIGHT, WristOrientation.FRONT_RIGHT): WristOrientation.FRONT_RIGHT,
                          (WristOrientation.RIGHT, WristOrientation.BACK_RIGHT): WristOrientation.BACK_RIGHT,
                          (WristOrientation.FRONT_LEFT, WristOrientation.FRONT): WristOrientation.FRONT_LEFT,
                          (WristOrientation.FRONT_LEFT, WristOrientation.LEFT): WristOrientation.FRONT_LEFT,
                          (WristOrientation.FRONT_RIGHT, WristOrientation.FRONT): WristOrientation.FRONT_RIGHT,
                          (WristOrientation.FRONT_RIGHT, WristOrientation.RIGHT): WristOrientation.FRONT_RIGHT,
                          (WristOrientation.BACK_LEFT, WristOrientation.BACK): WristOrientation.BACK_LEFT,
                          (WristOrientation.BACK_LEFT, WristOrientation.LEFT): WristOrientation.BACK_LEFT,
                          (WristOrientation.BACK_RIGHT, WristOrientation.BACK): WristOrientation.BACK_RIGHT,
                          (WristOrientation.BACK_RIGHT, WristOrientation.RIGHT): WristOrientation.BACK_RIGHT}

def mergeResults(result1, result2):
    wo1, co1, hp1 = result1
    wo2, co2, hp2 = result2
                
    # print(f"wo1: {wo1.orientation} \t| wo2: {wo2.orientation} \t| co2: {co2} \t| hp1: {hp1} \t| hp2: {hp2}")
    
    if wo1 != None and wo2 != None and co2 != None and hp1 != None and hp2 != None :
        # Handling side/calibration issues
        # if co2 != wo1.orientation:
        #     if (co2, wo1.orientation) in CALIBRATION_EQUIVALENT:
        #         co2 = CALIBRATION_EQUIVALENT[(co2, wo1.orientation)]
        #     else :
        #         co2 = wo1.orientation
        co2 = wo1.orientation

        # Getting the hand pose from the right webcam according to the orientation
        if hp1 == hp2:
            hp = hp1
        else :
            if wo1.orientation==WristOrientation.FRONT :
                # TODO Here I must take into account the angles with the camera in front
                hp = hp1
                hp.flex_fingers(hp2.get_flexed_fingers())
            elif wo2.orientation==WristOrientation.FRONT :
                hp = hp2
                hp.flex_fingers(hp1.get_flexed_fingers())
            else :
                hp = hp2
                # if co2 == WristOrientation.FRONT_LEFT :
                #     hp = hp2
                #     # From the side camera, keep the ring and pinky
                #     hp.finger_states[RING] = hp1.finger_states[RING]
                #     hp.finger_states[PINKY] = hp1.finger_states[PINKY]
                # else : 
                #     hp = hp2
        
        # Correcting the hand pose according to the corrected orientation (removing complex joints for side views)
        if co2 in [WristOrientation.LEFT, WristOrientation.RIGHT]:
            for finger in FINGERS: 
                if hp.finger_states[finger] in [mrep.COMPLEX, mrep.ABDUCTION, mrep.ADDUCTION]:
                    hp.finger_states[finger] = mrep.UP
        # print(f"co2: {co2} \t| wo1: {wo1.orientation} \t| wo2: {wo2.orientation}")
        return co2, hp