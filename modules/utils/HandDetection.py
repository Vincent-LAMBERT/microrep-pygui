
import math
from lxml import etree
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark
import subprocess

from .AppUtils import *


# import math
# import os
# import cv2
# import mediapipe as mp
# import numpy as np

# from colorama import init as colorama_init
# from colorama import Fore
# from colorama import Style

# import matplotlib

# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# class FingersTracker():
#     def __init__(self, mode=False, maxHands=1, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
#         self.mode = mode
#         self.maxHands = maxHands
#         self.detectionCon = detectionCon
#         self.modelComplex = modelComplexity
#         self.trackCon = trackCon
#         self.mpHands = mp.solutions.hands
#         self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
#                                         self.detectionCon, self.trackCon)
#         self.mpDraw = mp.solutions.drawing_utils

#     def landmark_finder(self, image):
#         # imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
#         self.results = self.hands.process(image)

#         hands = {LEFT:[], RIGHT:[]}
#         if self.results.multi_hand_landmarks:
#             for i, handLms in enumerate(self.results.multi_hand_landmarks): # working with each hand
#                 # Separate results accoridng to the hand
#                 handedness = self.results.multi_handedness[i].classification[0].label
#                 if handedness==LEFT : handedness=RIGHT # Mediapipe has inverted handednesses
#                 else : handedness=LEFT
#                 for lm in handLms.landmark:
#                     h,w,c = image.shape
#                     cx,cy,cz = int(lm.x*w), int(lm.y*h), int(lm.z*h)
#                     hands[handedness].append(NormalizedLandmark(cx,cy,cz))

#         print(f"hands : {hands}")
        
#         return self.results.multi_hand_landmarks


# BaseOptions = mp.tasks.BaseOptions
# HandLandmarker = mp.tasks.vision.HandLandmarker
# HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
# HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
# VisionRunningMode = mp.tasks.vision.RunningMode

# # Create a hand landmarker instance with the live stream mode:
# def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
#     print('hand landmarker result: {}'.format(result))

def create_detector() :
    # Mediapipe treatement
    base_options = python.BaseOptions(model_asset_path=HAND_LANDMARK_PATH)
    options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
    return vision.HandLandmarker.create_from_options(options)

# def stream_detector(function) :
#     options = HandLandmarkerOptions(
#         base_options=BaseOptions(model_asset_path=HAND_LANDMARK_PATH),
#         running_mode=VisionRunningMode.LIVE_STREAM,
#         result_callback=function)
#     return HandLandmarker.create_from_options(options) 

def input_treatement(image_name, detector) :
    # For treating the input
    if type(image_name) == str :
      if image_name == "" :
          print("errror: no path given")
          return ""
      else :
          image = mp.Image.create_from_file(image_name)
          image_numpy=image.numpy_view()
    else:
        image = mp.Image(image_format=mp.ImageFormat.SRGB,data=image_name)
        image_numpy = image.numpy_view()

    return image_numpy, detector.detect(image)


def update_mp_results(mp_results, list, max_size) :
    if len(list) == max_size :
        list.pop(0)

    detected_hands = {LEFT : [], RIGHT : []}

    handednesses = mp_results.handedness
    hand_landmarks = mp_results.hand_landmarks
    # handednesses = mp_results.multi_handedness
    # hand_landmarks = mp_results.multi_hand_landmarks

    for i in range(len(handednesses)) :
        if handednesses[i][0].category_name == LEFT :
        # if handednesses[i].classification[0].label == LEFT :
            landmarks = hand_landmarks[i]
            detected_hands[LEFT] = landmarks
        else :
            landmarks = hand_landmarks[i]
            detected_hands[RIGHT] = landmarks
            
    list.append(detected_hands)

    return compute_mean_detected_hands(list)

def compute_mean_detected_hands(list) :
    if len(list) == 0 :
        return None
    else :
        mean_detected_hands = list[0]

        for handedness in mean_detected_hands.keys() :
                
            if mean_detected_hands[handedness] == [] :
                mean_hand_landmarks = [NormalizedLandmark(0, 0, 0) for i in range(21)]
            else :
                mean_hand_landmarks = mean_detected_hands[handedness]

            not_detected = False

            # compute the mean_detected_hands
            for i in range(1, len(list)) :
                hand_landmarks = list[i][handedness]

                if hand_landmarks != [] :
                    for landmark_index, landmark in enumerate(hand_landmarks):
                        mean_hand_landmarks[landmark_index].x += landmark.x
                        mean_hand_landmarks[landmark_index].y += landmark.y
                        mean_hand_landmarks[landmark_index].z += landmark.z

                        if i == len(list) - 1 :
                            mean_hand_landmarks[landmark_index].x /= len(list)
                            mean_hand_landmarks[landmark_index].y /= len(list)
                            mean_hand_landmarks[landmark_index].z /= len(list)
                else :
                    not_detected = True

            if not_detected :
                mean_detected_hands[handedness] = []
                            
        return mean_detected_hands

# Create a dictionnary from an xml file of microgesture
def get_microgest_xml() :
    file = etree.parse(MOVES_XML_PATH)
    hand = file.getroot()
    dic = {}
    m_key=""
    
    for char in hand :
        m_key=char.get("fingerType")
        dic[m_key] = {}
        for gesture in char :
            microgest = gesture.get("microgesture")
            charac = gesture.get("charac")
            mark_type = gesture.get("markerType")
            key = f"{microgest}, {charac}, {mark_type}"
            coord = int(gesture.get("id_coord"))
            dic[m_key][key] = coord
    return dic

# Create an xml file from a dictionnary of microgesture
def dic_to_microgest_xml(dic) :
    hand = etree.Element("hand")
    
    for char in dic :
        finger=etree.SubElement(hand,"finger")
        finger.set("fingerType",char)
        for i in dic[char] :
            list_config = i.split(",")
            gesture = etree.SubElement(finger,"gesture")
            gesture.set("microgesture",list_config[0])
            gesture.set("charac",list_config[1])
            gesture.set("markerType",list_config[2])
            gesture.set("id_coord",f"{dic[char][i]}")  
    etree.ElementTree(hand).write(MOVES_XML_PATH, pretty_print=True, encoding="UTF-8", standalone="no", xml_declaration=True)

def angle(vector1, vector2) :
    # Calculate the angle between two vectors
    dotProduct = vector1[0]*vector2[0] + vector1[1]*vector2[1] + vector1[2]*vector2[2]
    magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2 + vector1[2]**2)
    magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2 + vector2[2]**2)

    if (magnitude1*magnitude2) == 0 :
        return 0
    return math.acos(dotProduct/(magnitude1*magnitude2)) * 180/math.pi

def list_coord_marks(handLandmarks, height, width) :
    i=0
    j=0
    coord_marqueur = []
    # For the marker on the thumb
    coord_marqueur.append((int((handLandmarks[4][0])*width), int((handLandmarks[4][1])*height))) 

    # For the marker next to  the thumb   
        # Give a fix position relative to the thumb
    dist_under_mark = (math.sqrt(((handLandmarks[13][0]-handLandmarks[9][0]))**2+((handLandmarks[13][1]-handLandmarks[9][1]))**2)*math.sin(math.radians(45)))/math.sin(math.radians(180-60-45))


    # Correct the orientationof the marks
    if handLandmarks[0][0]-handLandmarks[1][0] != 0 :
        side_hand = (handLandmarks[0][0]-handLandmarks[1][0])/abs(handLandmarks[0][0]-handLandmarks[1][0])
    else :
        side_hand = 1

    # Give the possibility to move marks to match the position of the thumb
    v1 = [handLandmarks[4][0]-handLandmarks[0][0], handLandmarks[4][1]-handLandmarks[0][1], handLandmarks[4][2]-handLandmarks[0][2]]
    v2 = [handLandmarks[5][0]-handLandmarks[0][0], handLandmarks[5][1]-handLandmarks[0][1], handLandmarks[5][2]-handLandmarks[0][2]]
    angle_thumb = math.radians(angle(v1,v2))

    coord_marqueur.append((
                    int((handLandmarks[4][0]+ side_hand*angle_thumb*(dist_under_mark*math.cos(math.radians(70)))*1.7) *width),
                    int((handLandmarks[4][1]- angle_thumb*(dist_under_mark*math.sin(math.radians(70)))*1.7) *height)))
    coord_marqueur.append((
                    int((handLandmarks[4][0]+ side_hand*angle_thumb*(dist_under_mark*math.cos(math.radians(40)))*2) *width),
                    int((handLandmarks[4][1]- angle_thumb*(dist_under_mark*math.sin(math.radians(40)))*2) *height)))
    coord_marqueur.append((
                    int((handLandmarks[4][0]+ side_hand*angle_thumb*(dist_under_mark*math.cos(math.radians(10)))*2.7) *width),
                    int((handLandmarks[4][1]- angle_thumb*(dist_under_mark*math.sin(math.radians(10)))*2.7) *height)))

    # For the other markers :    
    fix_shift_x = [handLandmarks[5][0]-handLandmarks[9][0],handLandmarks[9][0]-handLandmarks[13][0],handLandmarks[9][0]-handLandmarks[13][0],(handLandmarks[13][0]-handLandmarks[17][0])/1.5]
    fix_shift_y = [handLandmarks[5][1]-handLandmarks[9][1],handLandmarks[9][1]-handLandmarks[13][1],handLandmarks[9][1]-handLandmarks[13][1],(handLandmarks[13][1]-handLandmarks[17][1])/1.5]
    while i<=12 :
        # For the other markers next to the fingers, from tip to base
        coord_marqueur.append((
                        int((handLandmarks[8+i][0]+(handLandmarks[7+i][0]-handLandmarks[8+i][0])/2+(fix_shift_x[j])/1.5)*width),
                        int((handLandmarks[8+i][1]+(handLandmarks[7+i][1]-handLandmarks[8+i][1])/2+(fix_shift_y[j])/1.5)*height)))
        coord_marqueur.append((
                        int((handLandmarks[7+i][0]+(handLandmarks[6+i][0]-handLandmarks[7+i][0])/2+(fix_shift_x[j])/1.5)*width),
                        int((handLandmarks[7+i][1]+(handLandmarks[6+i][1]-handLandmarks[7+i][1])/2+(fix_shift_y[j])/1.5)*height)))
        coord_marqueur.append((
                        int((handLandmarks[6+i][0]+(handLandmarks[5+i][0]-handLandmarks[6+i][0])/2+(fix_shift_x[j])/1.5)*width),
                        int((handLandmarks[6+i][1]+(handLandmarks[5+i][1]-handLandmarks[6+i][1])/2+(fix_shift_y[j])/1.5)*height)))

        # For the other markers on fingers, from tip to base
        coord_marqueur.append((
                        int((handLandmarks[8+i][0])*width),
                        int((handLandmarks[8+i][1])*height)))
        coord_marqueur.append((
                        int((handLandmarks[8+i][0]+(handLandmarks[7+i][0]-handLandmarks[8+i][0])/2)*width),
                        int((handLandmarks[8+i][1]+(handLandmarks[7+i][1]-handLandmarks[8+i][1])/2)*height)))
        coord_marqueur.append((
                        int((handLandmarks[7+i][0]+(handLandmarks[6+i][0]-handLandmarks[7+i][0])/2)*width),
                        int((handLandmarks[7+i][1]+(handLandmarks[6+i][1]-handLandmarks[7+i][1])/2)*height)))
        coord_marqueur.append((
                        int((handLandmarks[6+i][0]+(handLandmarks[5+i][0]-handLandmarks[6+i][0])/4)*width),
                        int((handLandmarks[6+i][1]+(handLandmarks[5+i][1]-handLandmarks[6+i][1])/4)*height)))
        coord_marqueur.append((
                        int((handLandmarks[5+i][0]+(handLandmarks[6+i][0]-handLandmarks[5+i][0])/3)*width),
                        int((handLandmarks[5+i][1]+(handLandmarks[6+i][1]-handLandmarks[5+i][1])/3)*height)))
        i=i+4
        j=j+1

    return coord_marqueur