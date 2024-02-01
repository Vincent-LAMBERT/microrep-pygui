
from main import *

class Generator(QWidget) :
    def __init__(self, parent=None) :
        super().__init__(parent)
    
    def testSlot(self) :
        print("test")