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


class CamThread(threading.Thread):
    SVG_FOLDER_PATH="C:\\Users\\sasuk\\Other\\microrep-pygui\\resources\\images\\hand_poses\\"
    FRAMES_DELAY=20

    def __init__(self, previewName, mp_detector, camID, pov=WristOrientation.FRONT, image_treatment=None):
        threading.Thread.__init__(self)
        self._run_flag = True
        self.webcam_to_start = False
        self.cam_is_active = False
        
        self.previewName = previewName
        self.camID = camID
        
        if image_treatment is None:
            self.image_treatment = lambda frame: cv2.imshow(self.previewName, frame)
        else:
            self.image_treatment = image_treatment
            
        self.mp_detector = mp_detector
        self.results = None
        self.pov = pov
        
        self.cam = None

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.stop_webcam()
        self.wait()

    def stop_webcam(self):
        self.cam_is_active = False 
        self.cam.release()

    def start_webcam(self):
        self.webcam_to_start = True

    def run(self):
        while self._run_flag:
            if self.webcam_to_start and not self.cam_is_active:
                print("Starting " + self.previewName)
                self.webcam_to_start=False
                self.cam_is_active=True
                
                cv2.namedWindow(self.previewName)
                cv2.setWindowProperty(self.previewName, cv2.WND_PROP_TOPMOST, 1)
                # cam = cv2.VideoCapture(camID)
                self.cam = cv2.VideoCapture(self.camID, cv2.CAP_DSHOW)
                print(f"Camera {self.camID} is opened")
                self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
                # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
                
                # if self.cam_is_active():  # try to get the first frame
                #     self.rval, frame = self.cam.read()
                # else:
                #     self.rval = False

                self.start_time = time.time()
                self.frames = []
                self.hand_poses = []
            
            elif self.cam_is_active:
                frame, result = self.loop_cap(self.hand_poses)
                # frame, result = loop_cap(self.previewName, cam, self.mp_detector, self.pov, hand_poses)
                self.frames.append(frame)
                
                if not None in result:
                    self.results = result
                else :
                    self.results = None

                self.image_treatment(frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            elif not self.webcam_to_start and not self.cam_is_active:
                # Destroy the window if it exist
                if cv2.getWindowProperty(self.previewName, cv2.WND_PROP_VISIBLE) == 1:
                    cv2.destroyWindow(self.previewName)
        
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
            hand_pose = HandPose(hand_landmarks, wrist_orientation.orientation, hand_poses)
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
    