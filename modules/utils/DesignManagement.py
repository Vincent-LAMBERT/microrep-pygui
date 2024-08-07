import copy
import csv
import logging
import os
from PySide6.QtGui import QPixmap,QImage
import random
import cv2
import svg.path
from inkex import PathElement
from inkex.styles import Style
import numpy as np
import math

from microrep.core.mg_maths import apply_matrix_to_path, compute_translation, convert_from_complex, get_rotation_matrix
from microrep.core.ref_and_specs import LayerRef, get_layer_refs, get_mg_layer_refs, get_marker_layer_refs, get_markers_pos
from microrep.create_representations.create_representations.create_representations import CreateRepresentations
from microrep.core.utils import TRAJ_END, TRAJ_START, get_fmc_combination
from microrep.create_representations.create_representations.configuration_file import get_combinations_from_file
from microrep.create_representations.create_representations.create_mg_rep import create_mg_rep, move_element, move_path

from inkex.paths import CubicSuperPath, Path

from modules.utils.applytransforms.applytransform import ApplyTransform
# from imports.create_representations.create_representations import CreateRepresentations
from .HandDetection import list_coord_marks, get_microgest_xml
from .AppUtils import *
from lxml import etree
import inkex
from inkex.transforms import Transform

NULL_TRANSFORM = Transform([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])

from inkex.base import SvgOutputMixin, SvgInputMixin

def write_file(tree, file) :
    with open(file, "wb") as f:
        f.write(etree.tostring(tree))

def read_file(file) :
    families_tree = etree.parse(file)
    return families_tree

def get_markers_tree() :
    family_tree = get_families_tree()
    markers_tree = set_only_markers_visible(family_tree)
    return markers_tree

def get_families_tree() :
    return read_file(DESIGN_FILE)

def set_only_markers_visible(tree) :
    for child in tree.getroot():
        # Check that the child has the attribute style
        if child.attrib.get("style") is None:
            continue
        if child.attrib.get("id") != "markers-layer":
            # Replace "display:inline" with "display:none"
            child.attrib['style'] = child.attrib['style'].replace("display:inline", "display:none")
        else : 
            # Replace "display:none" with "display:inline"
            child.attrib['style'] = child.attrib['style'].replace("display:none", "display:inline")

    return tree

def flip_tree(tree) :
    for child in tree.getroot():
        # The patterns must NOT be flipped
        if child.attrib.get("id") == "designs-layer" :
            child.attrib['transform'] = f"scale(-1, 1)"
    return tree

def get_resize_ratio(tree, hand_landmarks) :    
    index_metacarpal_position = hand_landmarks[INDEX_METACARPAL]
    wrist_position = hand_landmarks[WRIST]

    # Getting the palm length
    palm_length_squared = np.sqrt((index_metacarpal_position.x - wrist_position.x)**2 + (index_metacarpal_position.y - wrist_position.y)**2)
    # Convert to mm (mediapipe gives the position in meters)
    palm_length_squared *= 1000
    
    # Getting the layers with the attribute 'mgrep-scale-marker'
    svg_layers = tree.xpath('//svg:g[@inkscape:groupmode="layer"]', namespaces=inkex.NSS)
    scale_marker_layers = [layer for layer in svg_layers if layer.attrib.get('mgrep-scale-marker') is not None]
    
    assert(len(scale_marker_layers) == 2)
    scale_markers = [scale_marker_layers[0][0], scale_marker_layers[1][0]]
    
    # Get the length of the segment between the two markers
    scale_markers_length_squared = np.sqrt((float(scale_markers[0].attrib['cx']) - float(scale_markers[1].attrib['cx']))**2 + (float(scale_markers[0].attrib['cy']) - float(scale_markers[1].attrib['cy']))**2)

    # Get the scale factor
    return palm_length_squared / scale_markers_length_squared

def scale_children(tree, scale_factor) :    
    # The patterns must be scaled too
    for child in tree.getroot() :
        child.attrib['transform'] = f"scale({scale_factor})"
        
    return tree

def apply_transforms(tree) :
    random_nbr = str(np.random.randint(0, 1000000))
    # Save as temp.svg

    write_file(tree, TEMP_FILE_PATH[:-4]+random_nbr+".svg")

    aply = ApplyTransform()
    aply.run([TEMP_FILE_PATH[:-4]+random_nbr+".svg"], output=TEMP_DESIGN_FILE_PATH[:-4]+random_nbr+".svg")

    # Get the new tree
    families_tree = etree.parse(TEMP_DESIGN_FILE_PATH[:-4]+random_nbr+".svg")

    # Remove the temporary file
    os.system(f"rm {TEMP_FILE_PATH[:-4]+random_nbr+'.svg'}")
    # Remove the temporary file
    os.system(f"rm {TEMP_DESIGN_FILE_PATH[:-4]+random_nbr+'.svg'}")

    return families_tree

def move_rep_markers(hand_landmarks, tree, img_height, img_width, dic=get_microgest_xml()) :
    # Fill list with x, y and z positions of each landmark
    handLandmarks = []
    for landmarks in hand_landmarks:
        handLandmarks.append([landmarks.x, landmarks.y, landmarks.z])
    # To get the coord for the marks
    coord_marqueur = list_coord_marks(handLandmarks, img_height, img_width)
    
    for finger in dic :
        if finger != "thumb" : finger_name = finger
        else : finger_name = 'index|middle|ring|pinky' 
        for elem in  dic[finger] :
            id_coord = dic[finger][elem]
            list_config = elem.split(", ")
            move_rep_marker(finger_name, list_config[0], list_config[1], list_config[2],
                        coord_marqueur[id_coord][0], coord_marqueur[id_coord][1], tree)
    return tree

def move_rep_marker(fingerCombo, mgCombo, characCombo, markerTypeCombo, coord_x, coord_y, tree) :
    # Get the layer group with the attribute mgrep-marker
    # associated with the values of fingerCombo, mgCombo, characCombo and markerTypeCombo
    marker_layer = tree.xpath(f'//svg:g[@mgrep-marker="{fingerCombo}, {mgCombo}, {characCombo}, {markerTypeCombo}"]', namespaces=inkex.NSS)
    # The marker is the only child of the layer group
    marker = marker_layer[0][0]
    # Move it to the new position
    marker.attrib['cx'] = str(coord_x)
    marker.attrib['cy'] = str(coord_y)
    return tree

def move_rep(rep_tree, markers_tree, fmc_combinations) :
    # Get a dictionnary of each exported family with their
    # element layers also put in a dictionnary corresponding 
    # to the element considered
    rep_tree_layer_refs = get_layer_refs(rep_tree, visible_only=True)
    microgesture_layer_refs = get_mg_layer_refs(rep_tree_layer_refs)
    
    # Get a dictionnary of each wanted microgesture marker
    # with their positions put in a dictionnary according to their type
    markers_tree_layers_refs = get_layer_refs(markers_tree, visible_only=True)
    marker_layer_refs = get_marker_layer_refs(markers_tree_layers_refs)
    markers = get_markers_pos(marker_layer_refs, fmc_combinations)

    for finger, mg, charac in fmc_combinations :
        if mg in microgesture_layer_refs[finger] and charac in microgesture_layer_refs[finger][mg]: 
            specific_markers = markers[finger][mg][charac]
            for layer_ref in microgesture_layer_refs[finger][mg][charac] :
                design_layer = layer_ref.source
                mg_specs = layer_ref.mg_export_specs
                assert(len(mg_specs)==1)
                element = mg_specs[0].element
                create_mg_rep(design_layer, element, specific_markers)

    return rep_tree

def remove_invisible_layers(tree) :
    svg_layers = tree.xpath('//svg:g[@inkscape:groupmode="layer"]', namespaces=inkex.NSS)

    # Find all of our "valid" layers.
    for layer in svg_layers:
        if 'style' in layer.attrib and 'display:none' in layer.attrib['style']:
            # Remove the layer from the tree.
            layer.getparent().remove(layer)

    return tree
    
def stroke_to_path(svg_tree, markers_tree, fmc_combinations):
    """
    Converts all strokes to paths in an SVG tree
    """
    # print(etree.tostring(svg_tree, pretty_print=True).decode())

    # Find all microgesture layers
    rep_tree_layer_refs = get_layer_refs(svg_tree, visible_only=True)
    microgesture_layer_refs = get_mg_layer_refs(rep_tree_layer_refs)

    markers_tree_layers_refs = get_layer_refs(markers_tree, visible_only=True)
    marker_layer_refs = get_marker_layer_refs(markers_tree_layers_refs)
    markers = get_markers_pos(marker_layer_refs, fmc_combinations)

    for finger, mg, charac in fmc_combinations :
        if mg in microgesture_layer_refs[finger] and charac in microgesture_layer_refs[finger][mg]: 
            specific_markers = markers[finger][mg][charac]
            for layer_ref in microgesture_layer_refs[finger][mg][charac] :
                parent_layer = layer_ref.source

                # The design layer has the attribute 'mgrep-path-element' set to 'design'
                design_layer = parent_layer.find(".//*[@mgrep-path-element='design']")
                # The trace layer has the attribute 'mgrep-path-element' set to 'trace'
                trace_layer = parent_layer.find(".//*[@mgrep-path-element='trace']")
                trace_start_layer = parent_layer.find(".//*[@mgrep-path-element='trace-start-bound']")
                trace_end_layer = parent_layer.find(".//*[@mgrep-path-element='trace-end-bound']")

                # If no trace layer exist at all, it is a stroke
                if trace_layer == None and trace_start_layer == None and trace_end_layer == None :
                    create_marker_path(svg_tree, parent_layer, design_layer, specific_markers)
    return svg_tree

def create_marker_path(svg_tree, parent_layer, design_layer, specific_markers) :
    path_element = design_layer.attrib['d']
    stroke = svg.path.parse_path(path_element)
    cubic_bezier = stroke[-1]

    end = cubic_bezier.end
    control1, control2 = cubic_bezier.control1, cubic_bezier.control2

    if control2 == end :
        ref_control = convert_from_complex(control1)
    else :
        ref_control = convert_from_complex(control2)
    end = convert_from_complex(end)


    reference_vector = end - ref_control
    # The unit vector for rotation refence goes horizontally to the right
    unit_vector = (1, 0)

    # Compute the rotation
    rotation_matrix = get_rotation_matrix(unit_vector, reference_vector)
    
    # In the following line, the term 'marker' corresponds to SVG markers and not the markers used to create the representations. Hence, we replace the term 'marker' by 'symbol' to avoid confusion in the variable names.
    # Get the symbol id of the marker-end in the style attribute
    symbol_end = design_layer.attrib['style'].split("marker-end:url(#")[1].split(")")[0]

    # Get the path of the symbol corresponding to the id
    symbol = svg_tree.find(f".//*[@id='{symbol_end}']")

    # The issue is that the symbol gets removed with the tiny svg conversion
    # Hence, we only re add it
    symbol_element = symbol.find(".//svg:path", namespaces=inkex.NSS).attrib['d']
    symbol_path = svg.path.parse_path(symbol_element)
    symbol_path = apply_matrix_to_path(symbol_path, {}, rotation_matrix)

    # Add the symbol path to the design layer
    new_node = PathElement()
    new_node.set("d", symbol_path.d())
    parent_layer.append(new_node)                    
    
    # Set new_mode position to the end of the path
    # create_mg_rep(new_node, element, specific_markers)
    new_node_path = compute_translation(new_node, specific_markers[TRAJ_END][1])
    new_node.set("d", new_node_path.d())

    return svg_tree
