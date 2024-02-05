from main import *

import modules.utils.HandDetection as hd
import modules.utils.DesignManagement as dm
import modules.utils.AppUtils as u
from lxml import etree

class Exporter(QWidget) :
    index = 0
    dic = hd.get_microgest_xml()

    markers_tree = None

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

    def update_background(self, background) :
        self.background = background
        self.label_file.setPixmap(QPixmap(background))

        image = cv2.imread(background)
        self.mgc.resize_design(image)
        mp_results = self.mgc.detect(image)
        
        if mp_results.hand_landmarks != [] :
            self.markers_tree, markers_pixmap = self.mgc.update_markers(mp_results, self.dic, self.mgc.img_height, self.mgc.img_width)
    
    def update_image(self) :
        if self.markers_tree :
            rep_tree, fmc_combination = self.mgc.getRep(self.index)
            if rep_tree is not None :
                # In that case, the fmc_combinations contains ALL THE POSSIBLE COMBINATIONS
                # We need to fetch the right one corresponding to the current representation
                tree, rep_pixmap = self.mgc.update_representation(rep_tree, self.markers_tree, fmc_combination, self.mgc.img_height, self.mgc.img_width)

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

    def export_current(self) :
        print("export_current")

    def export_all(self) :
        print("export_all")
    
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