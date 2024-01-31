
import threading
import time
import os
from PySide6.QtCore import Signal, Qt, QBuffer, QThread
from PySide6.QtGui import QPixmap,QImage
import cv2
from microrep.core.utils import TRAJ_END, TRAJ_START, get_fmc_combination
from microrep.create_representations.create_representations.configuration_file import get_combinations_from_file
import PIL as pix

from lxml import etree
import numpy as np

import time, numpy,cv2, subprocess, copy
import threading

# Classe QThread personnalisée pour la capture vidéo
class VideoThread(QThread):
    image_data = Signal(np.ndarray)
    
    def __init__(self, frame_rate=60, frame_skip=1):
        super(VideoThread, self).__init__()
        self.is_running = True
        
        self.frame_rate = frame_rate
        self.frame_skip = frame_skip

    def run(self):
        cap = cv2.VideoCapture(0)
        prev = 0
        while cap.isOpened() and self.is_running:
            time_elapsed = time.time() - prev
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            if time_elapsed > 1./self.frame_rate:
                prev = time.time()
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                # Upscale the image by 450%
                image = cv2.resize(image, None, fx=2.28, fy=2.28, interpolation=cv2.INTER_LANCZOS4)
                # print(f"Image shape : {image.shape}")
                self.image_data.emit(image)
        self.quit()
    
    def stop(self):
        self.is_running = False