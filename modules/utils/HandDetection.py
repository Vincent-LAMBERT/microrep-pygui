
import dataclasses
import math
import time
from lxml import etree
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark
import subprocess
from microrep.core.utils import get_wrist_orientation_nickname, get_status_nickname
from typing import List, Mapping, Optional, Tuple, Union


import numpy as np
from mediapipe.framework.formats import landmark_pb2
import cv2
from mediapipe import solutions

from .AppUtils import *

import microrep.core.utils as u
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green

def draw_landmarks_on_image(rgb_image, detection_result, is_relevant: bool = True):
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(rgb_image)

    # Loop through the detected hands to visualize.
    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]
        handedness = handedness_list[idx]

        # Draw the hand landmarks.
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            hand_landmarks_proto,
            solutions.hands.HAND_CONNECTIONS,
            solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=1),  # Change the color to green
            solutions.drawing_styles.get_default_hand_connections_style())

        # Get the top left corner of the detected hand's bounding box.
        height, width, _ = annotated_image.shape
        x_coordinates = [landmark.x for landmark in hand_landmarks]
        y_coordinates = [landmark.y for landmark in hand_landmarks]
        text_x = int(min(x_coordinates) * width)
        text_y = int(min(y_coordinates) * height) - MARGIN

        # Draw handedness (left or right hand) on the image.
        cv2.putText(annotated_image, f"{handedness[0].category_name}",
                    (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                    FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)
        
        if not is_relevant :
            cv2.putText(annotated_image, "Not relevant",
                        (text_x, text_y+20), cv2.FONT_HERSHEY_DUPLEX,
                        FONT_SIZE, (0, 0, 255), FONT_THICKNESS, cv2.LINE_AA)

    return annotated_image

_PRESENCE_THRESHOLD = 0.5
_VISIBILITY_THRESHOLD = 0.5
_BGR_CHANNELS = 3

WHITE_COLOR = (224, 224, 224)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 128, 0)
BLUE_COLOR = (255, 0, 0)
@dataclasses.dataclass
class DrawingSpec:
    # Color for drawing the annotation. Default to the white color.
    color: Tuple[int, int, int] = WHITE_COLOR
    # Thickness for drawing the annotation. Default to 2 pixels.
    thickness: int = 2
    # Circle radius. Default to 2 pixels.
    circle_radius: int = 2

def _normalized_to_pixel_coordinates(normalized_x: float, normalized_y: float, image_width: int, image_height: int) -> Union[None, Tuple[int, int]]:
    """Converts normalized value pair to pixel coordinates."""

    # Checks if the float value is between 0 and 1.
    def is_valid_normalized_value(value: float) -> bool:
        return (value > 0 or math.isclose(0, value)) and (value < 1 or
                                                        math.isclose(1, value))

    if not (is_valid_normalized_value(normalized_x) and
            is_valid_normalized_value(normalized_y)):
        # TODO: Draw coordinates even if it's outside of the image bounds.
        return None
    x_px = min(math.floor(normalized_x * image_width), image_width - 1)
    y_px = min(math.floor(normalized_y * image_height), image_height - 1)
    return x_px, y_px

class ImageHandLandmarker():
   def __init__(self):
      self.result = mp.tasks.vision.HandLandmarkerResult
      self.landmarker = mp.tasks.vision.HandLandmarker
      self.createLandmarker()
   
   def createLandmarker(self):
        # HandLandmarkerOptions (details here: https://developers.google.com/mediapipe/solutions/vision/hand_landmarker/python#live-stream)
        # Mediapipe treatement
        options = mp.tasks.vision.HandLandmarkerOptions( 
         base_options = mp.tasks.BaseOptions(model_asset_path=HAND_LANDMARK_PATH), # path to model
         running_mode = mp.tasks.vision.RunningMode.IMAGE, # running on a live stream
         num_hands = 2, # track both hands
         min_hand_detection_confidence = 0.3, # lower than value to get predictions more often
         min_hand_presence_confidence = 0.3, # lower than value to get predictions more often
         min_tracking_confidence = 0.3, # lower than value to get predictions more often
         )
        self.landmarker =  self.landmarker.create_from_options(options)
   
   def detect(self, frame):
      # convert np frame to mp image
      mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
      # detect landmarks
      self.landmarker.detect(image = mp_image)

   def close(self):
      # close landmarker
      self.landmarker.close()

class StreamHandLandmarker():
    detected_hands = []
    hands_list = []
    max_size_hands_list = 5

    def __init__(self):
        self.result = mp.tasks.vision.HandLandmarkerResult
        self.landmarker = mp.tasks.vision.HandLandmarker
        self.createLandmarker()
        
        self.timestamp = 0
    
    def createLandmarker(self):
        # callback function
        def update_result(result: mp.tasks.vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
            self.result = result

        # HandLandmarkerOptions (details here: https://developers.google.com/mediapipe/solutions/vision/hand_landmarker/python#live-stream)
        options = mp.tasks.vision.HandLandmarkerOptions( 
            base_options = mp.tasks.BaseOptions(model_asset_path=HAND_LANDMARK_PATH), # path to model
            running_mode = mp.tasks.vision.RunningMode.LIVE_STREAM, # running on a live stream
            num_hands = 2, # track both hands
            min_hand_detection_confidence = 0.3, # lower than value to get predictions more often
            min_hand_presence_confidence = 0.3, # lower than value to get predictions more often
            min_tracking_confidence = 0.3, # lower than value to get predictions more often
            result_callback=update_result)
        
        # initialize landmarker
        self.landmarker = self.landmarker.create_from_options(options)
    
    def detect_async(self, frame):
        # convert np frame to mp image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        # detect landmarks
        self.landmarker.detect_async(image = mp_image, timestamp_ms = self.timestamp)
        self.timestamp += 1

    def landmark_finder(self, opencv_image):
        imageRGB = cv2.cvtColor(opencv_image,cv2.COLOR_BGR2RGB)
        
        self.detect_async(imageRGB)

        # With async, the result treated here may be the one 
        # from a previous call of landmark_finder
        return self.result

    def close(self):
        # close landmarker
        self.landmarker.close()

    def direct_draw_landmarks(self, is_relevant: bool = True):
        annotated_image = np.copy(self.image)
        if hasattr(self.mp_results, 'hand_landmarks') and self.mp_results.hand_landmarks != [] :
            annotated_image = draw_landmarks_on_image(annotated_image, self.mp_results, is_relevant)
        # self.drawer.draw_landmarks(self.image, handLms, self.drawer.HAND_CONNECTIONS)
        return annotated_image
    
    #####################################################################
    
    def get_hands(self, image):
        self.image = image   
        # reduced_image = cv2.resize(image, (0, 0), fx=0.1, fy=0.1)

        self.mp_results = self.landmark_finder(image)
    
        if hasattr(self.mp_results, 'hand_landmarks') and self.mp_results.hand_landmarks != [] :
            self.detected_hands = self.optimize_results(self.mp_results)
        else :
            self.detected_hands = []
        return self.detected_hands
    
    def optimize_results(self, mp_results) :
        self.update_detected_hands_list(mp_results)
        # mp_results = self.compute_mean_detected_hands()
        mp_results = self.compute_mean_mp_results()
        
        return mp_results
    
    def update_detected_hands_list(self, mp_results) :
        if len(self.hands_list) == self.max_size_hands_list :
            self.hands_list.pop(0)
        self.hands_list.append(mp_results)

    def compute_mean_mp_results(self) :
        if len(self.hands_list) == 0 :
            return None
        else :
            mean_hands = []
            mp_results = self.hands_list[0]
            
            for hand_index, hand in enumerate(mp_results.hand_landmarks) :
                if hand == [] :
                    mean_hand_landmarks = [NormalizedLandmark(0, 0, 0) for i in range(21)]
                else :
                    mean_hand_landmarks = hand
    
                    # compute the mean_detected_hands
                    for i in range(1, len(self.hands_list)) :
                        for previous_hand_index, previous_hand in enumerate(self.hands_list[i].hand_landmarks) :
                            if previous_hand != [] :
                                for landmark_index, landmark in enumerate(previous_hand):
                                    mean_hand_landmarks[landmark_index].x += landmark.x
                                    mean_hand_landmarks[landmark_index].y += landmark.y
                                    mean_hand_landmarks[landmark_index].z += landmark.z
        
                                    if i == len(self.hands_list) - 1 :
                                        mean_hand_landmarks[landmark_index].x /= len(self.hands_list)
                                        mean_hand_landmarks[landmark_index].y /= len(self.hands_list)
                                        mean_hand_landmarks[landmark_index].z /= len(self.hands_list)
                mean_hands.append(mean_hand_landmarks)

            return mean_hands

def get_hand_pose_file_name(wrist_orientation, hand_pose, extension=".svg"):
    label = get_wrist_orientation_nickname(wrist_orientation.orientation)
    label += f"_"
    for finger in u.FINGERS_WITH_THUMB :
        status = hand_pose.finger_states[finger]
        label += finger[0].capitalize() + get_status_nickname(status) + "-"
    label = label[:-1]+extension
    
    return label

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