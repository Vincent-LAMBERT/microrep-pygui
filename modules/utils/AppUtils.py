import os
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import QByteArray
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QSize, Qt
from lxml import etree
import pathlib
from microrep.core.ref_and_specs import LayerRef, get_layer_refs, get_mg_layer_refs, get_marker_layer_refs, get_markers_pos
from microrep.create_representations.create_representations.create_representations import CreateRepresentations
import random

def getFilePath(filePath, localPath) :
    if os.name == 'nt' :
        # Convert locaPath to windows format
        localPath = localPath.replace("/", "\\")
    return os.path.join(os.path.dirname(filePath), localPath)

# Constants
RESOURCES_PATH=getFilePath(__file__, "../../resources/")
DATA_PATH=getFilePath(RESOURCES_PATH, "data/")
HAND_LANDMARK_PATH=getFilePath(DATA_PATH, "task/HandLandmarker.task")
MOVES_XML_PATH=getFilePath(DATA_PATH, "xml/list_move.xml")

SVG_FOLDER_PATH=getFilePath(RESOURCES_PATH, "images/svg/")
DESIGN_FILE=SVG_FOLDER_PATH+"families.svg"
TEMP_FOLDER_PATH=getFilePath(SVG_FOLDER_PATH, "temp/")
TEMP_FILE_PATH=TEMP_FOLDER_PATH+"temp.svg"
TEMP_CONFIG_PATH=TEMP_FOLDER_PATH+"tempConfig.csv"
TEMP_LIVE_VIDEO_PATH=TEMP_FOLDER_PATH+"tempLiveVideo.mp4"
TEMP_AT_FILE_PATH=TEMP_FOLDER_PATH+"tempAT.svg"
TEMP_COPY_FILE_PATH=TEMP_FOLDER_PATH+"tempCopy.svg"
TEMP_DESIGN_FILE_PATH=TEMP_FOLDER_PATH+"tempDesign.svg"
TEMP_REP_FILE_PATH=TEMP_FOLDER_PATH+"tempRep.svg"
TEMP_LIVE_FILE_PATH=TEMP_FOLDER_PATH+"tempLive.svg"
TEMP_REP_FOLDER_PATH=getFilePath(TEMP_FOLDER_PATH, "reps/")
TEMP_LIVE_FOLDER_PATH=getFilePath(TEMP_FOLDER_PATH, "live/")

CREATE_REP_PATH="create_representations/create_representations.py"
# CREATE_REP_PATH="inkscape_create_representations/create_representations/create_representations.py"
CREATE_REP_EXTENSION=getFilePath(__file__, '../../imports/'+CREATE_REP_PATH)

# MediaPipe hands model
WRIST = 0
THUMB_CARPAL = 1
THUMB_METACARPAL = 2
THUMB_PROXIMAL = 3
THUMB_DISTAL = 4
INDEX_METACARPAL = 5
INDEX_PROXIMAL = 6
INDEX_INTERMEDIATE = 7
INDEX_DISTAL = 8
MIDDLE_METACARPAL = 9
MIDDLE_PROXIMAL = 10
MIDDLE_INTERMEDIATE = 11
MIDDLE_DISTAL = 12
RING_METACARPAL = 13
RING_PROXIMAL = 14
RING_INTERMEDIATE = 15
RING_DISTAL = 16
PINKY_METACARPAL = 17
PINKY_PROXIMAL = 18
PINKY_INTERMEDIATE = 19
PINKY_DISTAL = 20
INDEX_MIDDLE = 21
MIDDLE_RING = 22
RING_PINKY = 23


LEFT = "Left"
RIGHT = "Right"

def getUI(fileName) :
    # Get the config tree
    return getFilePath(__file__, RESOURCES_PATH+'/data/ui/'+fileName)

def get_config(fileName) : 
    # Get the config tree
    return getFilePath(__file__, RESOURCES_PATH+'data/config/'+fileName)

def getExportPath() :
    download_path = str(pathlib.Path.home())+"/Downloads/"
    random_nbr = random.randint(0, 1000000)
    export_path = download_path+"export_"+str(random_nbr)+"/"
    # On Windows
    if os.name == 'nt' :
        export_path = export_path.replace("/", "\\")

    # Check that the folder does not already exist
    if os.path.isdir(export_path) :
        return getExportPath()
    else :
        os.mkdir(export_path)
        return export_path


def svg_to_pixmap(svg_tree, height=715, width=564):
    # Convert the SVG tree to an SVG string
    svg_string = etree.tostring(svg_tree, pretty_print=True).decode()

    # Create a QSvgRenderer
    svg_renderer = QSvgRenderer(QByteArray(svg_string.encode()))

    # Create a QPixmap to render the SVG
    pixmap = QPixmap(QSize(width, height))

    # Fill the QPixmap with a transparent background
    pixmap.fill(Qt.transparent)

    # Create a QPainter and render the SVG onto the QPixmap
    painter = QPainter(pixmap)
    svg_renderer.render(painter)
    painter.end()

    return pixmap

def deleteFolder(temp_folder) :
    if (os.name == 'nt'):
        os.system(f"rmdir /S /Q {temp_folder}")
    else :
        os.system(f"rm -rf {temp_folder}")

def createFolder(temp_folder) :
    if (os.name == 'nt'):
        os.system(f"mkdir {temp_folder}")
    else :
        os.system(f"mkdir {temp_folder}")
