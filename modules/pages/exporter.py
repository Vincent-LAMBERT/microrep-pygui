from main import *

import modules.utils.HandDetection as hd
import modules.utils.DesignManagement as dm
import modules.utils.AppUtils as u
from lxml import etree

class Exporter(QWidget) :

    def __init__(self, parent=None) :
        super().__init__(parent)

        self.download_folder_path = os.path.join(os.path.expanduser("~"), "Downloads")

    def configure(self, ui, microrep_thread) :
        self.ui = ui
        self.microrep_thread = microrep_thread
        
        self.ui.entry_export_path.setText(self.download_folder_path)

        # # Création des labels
        # self.label_file = ImageViewer()
        # self.label_markers = ImageViewer()

        # # Permet la superposition des labels/images
        # frame_layout = self.ui.frame_img.layout()
        # frame_layout.addWidget(self.label_file,0,0)
        # frame_layout.addWidget(self.label_markers,0,0)

    ################################################################
    #################### SLOT FUNCTIONS ############################
    ################################################################

    def previous_rep(self) :
        print("previous_rep")

    def next_rep(self) :
        print("next_rep")

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