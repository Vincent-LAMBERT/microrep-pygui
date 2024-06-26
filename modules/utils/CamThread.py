import time
import mediapipe as mp
import cv2
from PySide6.QtCore import Signal, Qt, QBuffer, QThread
import numpy as np
import uuid
import os
import threading
from lxml import etree

import microglyph.micro_glyph_detector as mgd
# import  NormalizedLandmark
from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark

from modules.utils.HandDetection import get_hand_pose_file_name

HandPose = mgd.MicroGlyphDetector.Detection.HandPose
WristOrientation = mgd.MicroGlyphDetector.Detection.WristOrientation

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_detector1 = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.5)
mp_detector2 = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.5)


class CamThread(QThread):
    image_data = Signal(np.ndarray)
    SVG_FOLDER_PATH="C:\\Users\\sasuk\\Other\\microrep-pygui\\resources\\images\\hand_poses\\"
    FRAMES_DELAY=20

    def __init__(self, previewName, mp_detector, camID, pov=WristOrientation.FRONT, image_treatment=None, result_treatment=None):
        super().__init__()
        self._run_flag = True
        self.webcam_started = False
        
        self.previewName = previewName
        self.camID = camID
        
        if image_treatment is None:
            self.image_treatment = lambda frame: cv2.imshow(self.previewName, frame)
        else :
            self.image_treatment = image_treatment
            
        if result_treatment is None:
            self.result_treatment = lambda frame: None 
            
        self.mp_detector = mp_detector
        self.results = None
        self.pov = pov

    def run(self):
        print("Starting " + self.previewName)
        self.camPreview()

    def camPreview(self):
        cv2.namedWindow(self.previewName)
        # cam = cv2.VideoCapture(camID)
        self.cam = cv2.VideoCapture(self.camID, cv2.CAP_DSHOW)
        print(f"Camera {self.camID} is opened: {self.cam.isOpened()}")
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
        # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
        
        if self.cam.isOpened():  # try to get the first frame
            rval, frame = self.cam.read()
        else:
            rval = False

        self.start_time = time.time()
        frames = []
        
        hand_poses = []
        
        while rval:
            frame, result = self.loop_cap(hand_poses)
            # frame, result = loop_cap(self.previewName, cam, self.mp_detector, self.pov, hand_poses)
            frames.append(frame)
            
            if not None in result:
                self.results = result
            else :
                self.results = None

            self.image_treatment(frame)
            self.result_treatment(result)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyWindow(self.previewName)
        
        # # print("Starting " + self.previewName)
        # # cv2.namedWindow(self.previewName)
        
        # self.cam = cv2.VideoCapture(self.camID)
        # self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
        
        # if self.cam.isOpened():  # try to get the first frame
        #     self.rval, frame = self.cam.read()
        # else:
        #     self.rval = False

        # self.start_time = time.time()
        # frames = []
        
        # while self.rval:
        #     frame, result = self.loop_cap()
        #     frames.append(frame)
            
        #     if not None in result:
        #         self.results = result
        #     else :
        #         self.results = None

        #     if time.time() - self.start_time > self.delay:
        #         self.image_data.emit((self.other_thread, self))
        #     #     cv2.imshow(self.previewName, frames.pop(0))

        #     # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     #     break

        # # cv2.destroyWindow(self.previewName)
            
    def loop_cap(self, hand_poses):
        rval, frame = self.cam.read()
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        image.flags.writeable = False

        result = self.mp_detector.process(image)
        # Transform to make it a list of 21 landmarks
        hand_landmarks = []
        if result.multi_hand_landmarks:
            handmarks = result.multi_hand_landmarks[0]
            for handmark in handmarks.landmark:
                landmark = NormalizedLandmark(handmark.x, handmark.y, handmark.z)
                hand_landmarks.append(landmark)

        if hand_landmarks != []:
            wrist_orientation = WristOrientation(hand_landmarks)
            hand_pose = HandPose(self.previewName, hand_landmarks, wrist_orientation.orientation, hand_poses)
            hand_poses.append(hand_pose)
            if len(hand_poses) > 10 :
                hand_poses.pop(0)
            
            if self.pov!=WristOrientation.FRONT :
                corrected_orientation = WristOrientation.correct_orientation(wrist_orientation, self.pov)
            else :
                corrected_orientation = wrist_orientation.orientation
        else :
            wrist_orientation = None
            hand_pose = None
            corrected_orientation = None
        
        # Set flag to true
        image.flags.writeable = True
        
        # RGB 2 BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Rendering results
        if result.multi_hand_landmarks:
            for num, hand in enumerate(result.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                                        mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                        mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                            )
        return image, (wrist_orientation, corrected_orientation, hand_pose)
    
    @staticmethod
    def get_results(self, thread1, thread2):
        filename = None
        old_filename = None
        previous_frame_result = None
        count_frames_with_result = 0
        
        while thread1.is_alive() and thread2.is_alive():
            result1, result2 = thread1.results, thread2.results
            if result1 != None and result2 != None:
                result = CamThread.mergeResults(result1, result2)
                
                if previous_frame_result != result:
                    count_frames_with_result = 0
                else:
                    count_frames_with_result += 1
                
                if count_frames_with_result > CamThread.FRAMES_DELAY:
                    # Corrected orientation gives the orient for the filename
                    filename = get_hand_pose_file_name(*result)
                    
                    # svg_tree = dm.read_file("resources/images/hand_poses/" + filename)
                    # pixmap = svg_to_pixmap(svg_tree)
                    # show with cv2
                    # img = cv2.imread("resources/images/hand_poses/" + filename)
                    # cv2.imshow("Hand Pose", img)
                    
                    if filename!=None and (old_filename==None or old_filename!=filename):
                        old_filename = filename
                        print(f"Filename: {filename}")
                        # Loads the image
                        svg_data = etree.parse(CamThread.SVG_FOLDER_PATH+filename)
                        svg_tree_as_string = etree.tostring(svg_data)
                    #     # print("svg_tree_as_string: ", svg_tree_as_string)
                        self.widgetSvg.load(svg_tree_as_string)
            
                    #     if thread2.results[1] in [WristOrientation.BACK, WristOrientation.FRONT, WristOrientation.LEFT, WristOrientation.RIGHT] :
                    #         name = f"{thread2.results[1]} \t\t"
                    #     else :
                    #         name = f"{thread2.results[1]} \t"
                    #     # # print(f"{name} --- {thread1.previewName}: {thread1.results[0]} --- {thread2.previewName}: {thread2.results[0]}")
                    #     print(f"{name} --- {thread1.previewName}: {thread1.results[2]} \t\t| {thread2.previewName}: {thread2.results[2]} \t\t| final: {rs[1]} - {rs[0]}")
                    
                previous_frame_result = result
                time.sleep(0.01)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.stopWebcam()
        self.wait()

    def stopWebcam(self):
        if self.cam!=None and self.cam.isOpened():
            self.cam.release()

    def startWebcam(self):
        # cv2.namedWindow(self.previewName)
        # self.cam = cv2.VideoCapture(self.camID, cv2.CAP_MSMF)
        # self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
        self.webcam_started = True

    def resetComputing(self):
        pass