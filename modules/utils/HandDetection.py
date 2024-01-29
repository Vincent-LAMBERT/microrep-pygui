
import math
from lxml import etree
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import subprocess

from .AppUtils import *

def create_detector() :
    # Mediapipe treatement
    base_options = python.BaseOptions(model_asset_path=HAND_LANDMARK_PATH)
    options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
    return vision.HandLandmarker.create_from_options(options)

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
    list.append(mp_results)

    return compute_mean_mp_results(list)

def compute_mean_mp_results(list) :
    if len(list) == 0 :
        return None
    else :
        mean_mp_result = list[0]

        # compute the mean_mp_result
        for i in range(1, len(list)) :
            for hand_index, hand_landmarks in enumerate(list[i].hand_landmarks):
                for landmark_index, landmark in enumerate(hand_landmarks):
                    mean_mp_result.hand_landmarks[hand_index][landmark_index].x += landmark.x
                    mean_mp_result.hand_landmarks[hand_index][landmark_index].y += landmark.y
                    mean_mp_result.hand_landmarks[hand_index][landmark_index].z += landmark.z

                    if i == len(list) - 1 :
                        mean_mp_result.hand_landmarks[hand_index][landmark_index].x /= len(list)
                        mean_mp_result.hand_landmarks[hand_index][landmark_index].y /= len(list)
                        mean_mp_result.hand_landmarks[hand_index][landmark_index].z /= len(list)

        return mean_mp_result

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
    side_hand = (handLandmarks[0][0]-handLandmarks[1][0])/abs(handLandmarks[0][0]-handLandmarks[1][0])
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