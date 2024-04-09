import os

# pyside6-uic resources/data/ui/main.ui> modules/ui_main.py

os.system("pyside6-uic resources/data/ui/main.ui> modules/ui_main.py")

# pyside6-rcc resources/data/ui/resources.qrc -o resources/data/ui/resources_rc.py

os.system("pyside6-rcc resources/data/ui/resources.qrc -o modules/resources_rc.py")

# replace "import resources_rc" by "from .resources_rc import *" in modules/ui_main.py

with open("modules/ui_main.py", "r") as f:
    lines = f.readlines()

with open("modules/ui_main.py", "w") as f:
    for line in lines:
        f.write(line.replace("import resources_rc", "from .resources_rc import *"))