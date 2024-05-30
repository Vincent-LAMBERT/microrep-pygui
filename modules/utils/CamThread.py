import mediapipe as mp
import cv2
from PySide6.QtCore import Signal, Qt, QBuffer, QThread
import numpy as np
import uuid
import os
import threading

import microglyph.micro_glyph_detector as mgd
# import  NormalizedLandmark
from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark

HandPose = mgd.MicroGlyphDetector.Detection.HandPose
WristOrientation = mgd.MicroGlyphDetector.Detection.WristOrientation

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_detector1 = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.5)
mp_detector2 = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.5)


class CamThread(QThread):
    image_data = Signal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.cap = None
        self.rval = False
        self.webcam_started = False

        self.previewName = "Camera"
        self.camID = 0
        self.mp_detector = mp_detector1

    def run(self):
        while self._run_flag:
            if self.webcam_started:
                self.cap = cv2.VideoCapture(self.camID, cv2.CAP_MSMF)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
                # cv2.namedWindow(self.previewName)
                # cv2.setWindowProperty(self.previewName, cv2.WND_PROP_TOPMOST, 1)

                self.rval, self.frame = self.cap.read()
                while self.rval:
                    self.frame, hand_landmarks, hand_pose, wrist_orientation = self.loop_cap()
                    self.image_data.emit((hand_landmarks, hand_pose, wrist_orientation))
                #     cv2.imshow(self.previewName, self.frame)
                #     if cv2.waitKey(10) & 0xFF == ord('q'):
                #         break
                # cv2.destroyWindow(self.previewName)
            
    def loop_cap(self):
        self.rval, frame = self.cap.read()

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
            hand_pose = HandPose(hand_landmarks)
            wrist_orientation = WristOrientation(hand_landmarks)
            # print("CAMERA: "+str(self.previewName)+" | Hand_pose: "+str(hand_pose)+", Wrist_orientation: "+str(wrist_orientation))
        else:
            hand_pose = None
            wrist_orientation = None
        
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
        return image, hand_landmarks, hand_pose, wrist_orientation

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.stopWebcam()
        self.wait()

    def stopWebcam(self):
        if self.cap!=None and self.cap.isOpened():
            self.cap.release()

    def startWebcam(self):
        # cv2.namedWindow(self.previewName)
        # self.cap = cv2.VideoCapture(self.camID, cv2.CAP_MSMF)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
        self.webcam_started = True

    def resetComputing(self):
        pass