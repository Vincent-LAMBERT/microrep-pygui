from argparse import ArgumentParser
import base64
from main import *
import threading

import modules.utils.HandDetection as hd
import modules.utils.DesignManagement as dm
import modules.utils.AppUtils as u
from lxml import etree
from modules.utils.AppUtils import get_config
from microrep.core.export import export
from microrep.create_representations.create_representations import CreateRepresentations
from modules.utils.MicroRepThread import resize_tree

from microrep.create_representations.create_representations.configuration_file import get_combination_from_row

from microrep.core.utils import get_fmc_combination, get_combination_name

TREE = "tree"
PIXMAP = "pixmap"
NAME = "name"

class Webcam(QWidget) :
    prefix="export_"

    def __init__(self, parent=None) :
        super().__init__(parent)

        with open(u.get_config("default_config.csv"), "r") as config_file :
            self.list_config = config_file.read().split("\n")

        self.families = ["AandB", "MaS"]
            

    def configure(self, ui, microrep_thread, webcam_thread) :
        self.ui = ui
        self.mgc = microrep_thread
        self.wt = webcam_thread

        self.ui.comboBox_family.addItems(self.families)
        self.ui.comboBox_config.addItems(self.list_config)

    def recompute_config(self) :
        config = self.ui.comboBox_config.currentText()
        with open(get_config("live_config.csv"), "w") as config_file :
            config_file.write(config)
        self.mgc.set_config("live_config.csv")

    ################################################################
    #################### SLOT FUNCTIONS ############################
    ################################################################
        
    def selectFamily(self) :
        self.selectActive()
    
    def selectMapping(self) :
        self.recompute_config()
        self.selectActive()

    def selectActive(self) :
        selected_family = self.ui.comboBox_family.currentText()
        selected_mapping = self.ui.comboBox_config.currentText()

        if selected_family and selected_mapping :
            selected_mapping = selected_mapping.split(",")
            combinations = get_combination_from_row(selected_mapping)
            mapping_name = get_combination_name(combinations)

            self.active = f"{self.prefix}{selected_family}_{mapping_name}.svg"
            
            self.mgc.set_active(self.active)
            self.wt.resetComputing()
