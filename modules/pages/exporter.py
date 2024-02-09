from argparse import ArgumentParser
import base64
from main import *
import threading

import modules.utils.HandDetection as hd
import modules.utils.DesignManagement as dm
import modules.utils.AppUtils as u
from lxml import etree
from microrep.core.export import export
from microrep.create_representations.create_representations import CreateRepresentations
from modules.utils.MicroRepThread import resize_tree

TREE = "tree"
PIXMAP = "pixmap"
NAME = "name"

class Exporter(QWidget) :
    index = 0
    representations = {TREE:{}, PIXMAP:{}, NAME:{}}

    dic = hd.get_microgest_xml()

    markers_tree = None
    images_computed = False

    def __init__(self, parent=None) :
        super().__init__(parent)

        self.download_folder_path = os.path.join(os.path.expanduser("~"), "Downloads")

    def configure(self, ui, microrep_thread) :
        self.ui = ui
        self.mgc = microrep_thread
        
        self.ui.entry_export_path.setText(self.download_folder_path)

        # Création des labels
        self.label_file = ImageViewer()
        self.label_rep = ImageViewer()

        # Permet la superposition des labels/images
        frame_layout = self.ui.frame_mappings.layout()
        frame_layout.addWidget(self.label_file,0,0)
        frame_layout.addWidget(self.label_rep,0,0)

    def start(self, config_path, image) :
        self.mgc.set_config(config_path)
        self.mgc.recompute_design()
        self.background = image
        self.setup_images(self.background)
        self.compute_images()  
        self.update_background()
        self.update_image()

        self.ui.btn_export_current.setEnabled(True)
        self.ui.btn_export_all.setEnabled(True)
        self.ui.btn_previous.setEnabled(True)
        self.ui.btn_next.setEnabled(True)

    def update_background(self) :
        self.label_file.setPixmap(QPixmap(self.background))

    def setup_images(self, background) :
        image = cv2.imread(background)
        self.mgc.update_frame_size(image)

        hand_landmarks = self.mgc.detect(image)
        
        if hand_landmarks != [] :
            self.markers_tree, markers_pixmap = self.mgc.update_markers(hand_landmarks, self.dic, self.mgc.img_height, self.mgc.img_width)

    def compute_images(self) :
        self.nbr_representations = len(os.listdir(u.TEMP_REP_FOLDER_PATH))

        if self.markers_tree :
            for i in range(self.nbr_representations) :
                self.index = i
                self.compute_image(i)

    def compute_image(self, i) :
        rep_tree, fmc_combination, file_name = self.mgc.getRep(i)
        rep_tree = resize_tree(rep_tree, self.mgc.img_height, self.mgc.img_width)
        
        if rep_tree is not None :
            # In that case, the fmc_combinations contains ALL THE POSSIBLE COMBINATIONS
            # We need to fetch the right one corresponding to the current representation
            tree, rep_pixmap = self.mgc.update_representation(rep_tree, self.markers_tree, fmc_combination, self.mgc.img_height, self.mgc.img_width)

            self.representations[TREE][i] = tree
            self.representations[PIXMAP][i] = rep_pixmap
            self.representations[NAME][i] = file_name
    
    def update_image(self) :
        rep_pixmap = self.representations[PIXMAP].get(self.index%self.nbr_representations)
        self.label_rep.setPixmap(rep_pixmap)

    ################################################################
    #################### SLOT FUNCTIONS ############################
    ################################################################

    def previous_rep(self) :
        self.index -= 1
        self.update_image()

    def next_rep(self) :
        self.index += 1
        self.update_image()

    def export_rep(self, i) :
        rep_tree = self.representations[TREE].get(i%self.nbr_representations)
        # Create a svg element from the background image
        # and add it to the representation tree
        svg_image = etree.Element('svg')
        svg_image.set('width', str(self.mgc.img_width))
        svg_image.set('height', str(self.mgc.img_height))
        svg_image.set('xmlns', 'http://www.w3.org/2000/svg')
        svg_image.set('version', '1.1')

        image = etree.SubElement(svg_image, 'image')
        image.set('x', '0')
        image.set('y', '0')
        image.set('width', str(self.mgc.img_width))
        image.set('height', str(self.mgc.img_height))

        href_back = 'data:image/jpg;base64,'
        image_data = base64.b64encode(open(self.background, 'rb').read()).decode('utf-8')
        href_back += image_data
        image.set('{http://www.w3.org/1999/xlink}href', href_back)

        root = rep_tree.getroot()
        root.insert(0, svg_image)
        
        # Create an option object to pass to the export function
        # You are supposed to access the attributes : prefix, path, filetype and dpi
        # Example : options.prefix access the prefix attribute
        options = CreateRepresentations().options
        options.prefix = self.ui.entry_prefix.text()
        options.path = self.ui.entry_export_path.text()
        options.filetype = self.ui.comboBox_export_type.currentText().lower()
        options.dpi = 90.0

        file_name = self.representations[NAME].get(i%self.nbr_representations)
        file_name = self.ui.entry_prefix.text() + file_name
        file_name = file_name.split('.')[0]

        export(rep_tree, file_name, options)

    def export_current(self) :
        # Export the current representation
        self.export_rep(self.index)

    def export_all(self) :
        # Export all the representations
        file_pixmap = self.label_file.getPixmap()
        for i in range(self.nbr_representations) :
            self.export_rep(i, file_pixmap)
    
    def select_export_folder(self) :
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.Directory)
        folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)
        
        # Select a directory 
        if folder_dialog.exec() :
            folder_name = folder_dialog.selectedFiles()
            if len(folder_name) != 1 :
                print('Select only one folder')
            else :
                self.ui.entry_export_path.setText(folder_name[0])

    def back_to_generator(self) :
        # Show export page
        self.ui.stackedWidget.setCurrentWidget(self.ui.generator_page)