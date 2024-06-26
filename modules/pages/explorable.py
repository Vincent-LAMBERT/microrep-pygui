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

from modules.utils.microgesture_detector.microglyph.micro_glyph import MicroGlyphEvent

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

    def configure(self, ui, microrep_thread, main_thread, second_thread) :
        self.ui = ui
        self.mgc = microrep_thread

        self.ui.comboBox_explorable_family.addItems(self.families)
        self.ui.comboBox_explorable_config.addItems(self.list_config)

        self.main_thread = main_thread
        self.second_thread = second_thread
        
        self.update_image(self.main_thread, self.second_thread)

    def recompute_config(self) :
        config = self.ui.comboBox_explorable_config.currentText()
        with open(get_config("live_config.csv"), "w") as config_file :
            config_file.write(config)
        self.mgc.set_config("live_config.csv")

    def start(self) :
        self.page_is_active = True
        self.main_thread.start_webcam()
        self.second_thread.start_webcam()
    
    def stop(self) :
        self.page_is_active = False
        self.main_thread.stop_webcam()
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
        # thread1, thread2 = threads
        # # print(f"Thread 1: {thread1.isRunning()} | Thread 2: {thread2.isRunning()}")

        results = []
        
        # while thread1.isRunning() and thread2.isRunning():
            
        #     # resultThread = threading.Thread(target=get_results, args=(thread1, thread2, results))
        #     # resultThread.start()
            
        #     # back_thread = threading.Thread(target=self.update_hand_pose, args=(hand_landmarks, hand_pose, wrist_orientation,))
        #     # back_thread.start()

        #     # labels_thread = threading.Thread(target=self.update_labels)
        #     # labels_thread.start()
            
        #     self.mgc.update_running_info()

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
                # image = QImage("resources/images/hand_poses/" + self.filename)
                # print(f"filename: {filename} | image: {image}")
                # self.hand_pose_img = QPixmap(image)

    
                print(f"filename: {filename}")
                svg_tree = dm.read_file("resources/images/hand_poses/" + self.filename)
                self.hand_pose_img = svg_to_pixmap(svg_tree)
    
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

        
def get_results(thread1, thread2, results):
    if thread1.results != None and thread2.results != None:
        result = mergeThreads(thread1, thread2)
        results.append(result)
        
        if len(results) > 15:
            results.pop(0)
        
        # Check if every result is the same
        if all(elem == results[-1] for elem in results):
            rs = results[-1]
            # Corrected orientation gives the orient for the filename
            filename = hd.get_hand_pose_file_name(*rs)
            
            if thread2.results[1] in [WristOrientation.BACK, WristOrientation.FRONT, WristOrientation.LEFT, WristOrientation.RIGHT] :
                name = f"{thread2.results[1]} \t\t"
            else :
                name = f"{thread2.results[1]} \t"
            # print(f"{name} --- {thread1.previewName}: {thread1.results[0]} --- {thread2.previewName}: {thread2.results[0]}")
            # print(f"{name} --- {thread1.previewName}: {thread1.results[2]} \t\t| {thread2.previewName}: {thread2.results[2]} \t\t| final: {rs[1]}")
                
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

def mergeThreads(thread1, thread2):
    wrist_orientation1, corrected_orientation, hand_pose1 = thread1.results
    wrist_orientation2, x, hand_pose2 = thread2.results
    
    if wrist_orientation1 != None and wrist_orientation2 != None and corrected_orientation != None and hand_pose1 != None and hand_pose2 != None :
        
        # Handling side/calibration issues
        if corrected_orientation != wrist_orientation2.orientation:
            if (corrected_orientation, wrist_orientation2.orientation) in CALIBRATION_EQUIVALENT:
                corrected_orientation = CALIBRATION_EQUIVALENT[(corrected_orientation, wrist_orientation2.orientation)]
    
        if hand_pose1 == hand_pose2:
            hand_pose = hand_pose1
        else :
            if wrist_orientation1.orientation==WristOrientation.FRONT :
                hand_pose = hand_pose1
            elif wrist_orientation2.orientation==WristOrientation.FRONT :
                hand_pose = hand_pose2
            else :
                if corrected_orientation == WristOrientation.FRONT_LEFT :
                    hand_pose = hand_pose2
                    # From the side camera, keep the ring and pinky
                    hand_pose.finger_states[MicroGlyphEvent.FINGER.RING] = hand_pose1.finger_states[MicroGlyphEvent.FINGER.RING]
                    hand_pose.finger_states[MicroGlyphEvent.FINGER.PINKY] = hand_pose1.finger_states[MicroGlyphEvent.FINGER.PINKY]
                else : 
                    hand_pose = hand_pose2

        return corrected_orientation, hand_pose