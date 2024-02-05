from main import *

import modules.utils.HandDetection as hd
import modules.utils.DesignManagement as dm
import modules.utils.AppUtils as u
from lxml import etree

class Generator(QWidget) :

    def __init__(self, parent=None) :
        super().__init__(parent)

        with open(u.get_config("default_config.csv"), "r") as config_file :
            self.list_config = config_file.read().split("\n")
        self.config_str = ""

    def configure(self, ui, microrep_thread) :
        self.ui = ui
        self.microrep_thread = microrep_thread
        self.default_config()

        # Création des labels
        self.label_file = ImageViewer()
        self.label_markers = ImageViewer()

        # Permet la superposition des labels/images
        frame_layout = self.ui.frame_img.layout()
        frame_layout.addWidget(self.label_file,0,0)
        frame_layout.addWidget(self.label_markers,0,0)

    ################################################################
    #################### SLOT FUNCTIONS ############################
    ################################################################

    def import_image(self) :
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilter('JPG files (*.jpg);;All files (*.*)')
        if file_dialog.exec():
            file_names = file_dialog.selectedFiles()
            if len(file_names) != 1 :
                print('Select only one file')
            else :
                self.canva = ""
                self.image = file_names[0]
                if self.image :
                    pixmap = QPixmap(self.image)
                    self.label_file.setPixmap(pixmap)

    def lock_mappings(self) :
        # Change enabled state of the mapping_frame
        status = self.ui.mapping_frame.isEnabled()

        if status == True :
            self.ui.mapping_frame.setEnabled(False)
            self.ui.btn_mapping.setText("Unlock mappings")
        else :
            self.ui.mapping_frame.setEnabled(True)
            self.ui.btn_mapping.setText("Lock mappings")

    def clear_config(self) :
        self.list_config = []
        self.ui.list_config.clear()

        self.clear_configFile()

    def remove_config(self) :
        print(self.ui.list_config.currentRow())
        cur = self.ui.list_config.currentRow()
        self.list_config.pop(cur)
        self.ui.list_config.takeItem(cur)

        self.clear_configFile()

    def default_config(self) :
        with open(u.get_config("default_config.csv"), "r") as file :
            self.clear_config()
            self.list_config = file.read().split("\n")
            for str in self.list_config :
                self.ui.list_config.addItem(str)

            self.clear_configFile()

    def apply_config(self) :
        if self.config_str != "" :
            self.list_config.append(self.config_str)
            self.ui.list_config.addItem(self.config_str)
            self.config_str = ""
            self.ui.label_str_config.setText(self.config_str)

            self.clear_configFile()

    def save_config_as_file(self) :
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,
            "Save File", "", "CSV files (*.csv);;All Files(*)", options = options)

        # add .csv to the file name if it's not already there
        if not self.fileName.endswith('.csv'):
            self.fileName += '.csv'

        if fileName:
            with open(fileName, 'w') as f:
                text = '\n'.join(self.ui.list_config.item(ii).text() for ii in range(self.ui.list_config.count()))
                f.write(text)

    def select_file_config(self) :
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilter('CSV files (*.csv);;All files (*.*)')
        if file_dialog.exec():
            file_names = file_dialog.selectedFiles()
            if len(file_names) != 1 :
                print('Select only one file')
            else :
                self.clear_config()
                file_name = file_names[0]
                with open(file_name, "r") as open_file :
                    self.list_config = open_file.read().split("\n")
                    for str in self.list_config :
                        self.ui.list_config.addItem(str)

                self.ui.entry_config.setText(file_name)

    def add_mapping(self) :
        finger = self.ui.comboBox_finger.currentText().lower()
        rep_type = self.ui.comboBox_microgesture.currentText().lower()
        rep_charac = self.ui.comboBox_charac.currentText().lower()
        if self.config_str == "" :
            self.config_str = f"{finger}+{rep_type}-{rep_charac}"
        else :
            self.config_str += f",{finger}+{rep_type}-{rep_charac}"
        self.ui.label_str_config.setText(self.config_str)

    def export_image_with_mappings(self) :
        if (self.image == "") :
            print('Select an image')
        else :
            # Create temporary config path file
            with open(u.TEMP_CONFIG_PATH, "w") as temp_config_path :
                temp_config_path.write('\n'.join(self.list_config))

            self.microrep_thread.set_config(u.TEMP_CONFIG_PATH)
            self.microrep_thread.recompute_design()
            # Show export page
            self.ui.stackedWidget.setCurrentWidget(self.ui.exporter_page)

    ################################################################
    #################### WORKING FUNCTIONS #########################
    ################################################################

    # def applyMarkers(self):
    #     if (self.image == "") :
    #         print('Select an image')
    #     else :
    #         image_numpy, mp_results = hd.input_treatement(self.image)
    #         self.img_height, self.img_width, channel = image_numpy.shape

    #         if len(mp_results.hand_landmarks) > 0:
    #             # self.tree = hd.svg_resize(height,width)
    #             # self.tree = hd.creat_svg_layer_image(image_numpy, mp_results, self.tree, self.dic)
    #             self.tree = dm.get_families_tree()
    #             self.tree = dm.set_only_markers_visible(self.tree)
    #             self.tree = dm.family_resize(self.tree, mp_results, self.img_height, self.img_width)
    #             self.tree = dm.move_rep_markers(image_numpy, mp_results, self.tree, self.dic)

    #             # Save as families_out.svg
    #             with open(u.TEMP_FILE_PATH, "wb") as f:
    #                 f.write(etree.tostring(self.tree))

    #             self.canva = u.svg_to_pixmap(self.tree, self.img_height, self.img_width)
    #             self.label_markers.setPixmap(QPixmap(self.canva))
    #             print('Markers applied')
    #         else :
    #             print('No hand detected')

    def clear_configFile(self) :
        self.ui.entry_config.setText("")