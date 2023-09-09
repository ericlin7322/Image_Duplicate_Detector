import sys
import os
from tqdm import tqdm
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
import time
from PIL import Image

class Classifier(QThread):

    process = pyqtSignal(int)
    found = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

    @pyqtSlot(str, str)
    def classify(self, image, folder):
        im1 = Image.open(image)

        str = []

        start_time = time.time()
        file_done = 0
        file_count = sum(len(files) for _, _, files in os.walk(folder, topdown=False))
        with tqdm(total=file_count) as pbar:
            for root, dirs, files in os.walk(folder):
                for name in files:
                    if name.endswith('.png') or name.endswith('.PNG') or name.endswith('.jpg') or name.endswith('.jpeg') or name.endswith('.JPG'):
                        try:
                            im2 = Image.open(os.path.join(root, name))
                            if im1 == im2:
                                str.append(os.path.join(root, name))
                                self.found.emit(os.path.join(root, name))
                        except:
                            print(f"Error at {os.path.join(root, name)}")
                    pbar.update(1)
                    file_done += 1
                    self.process.emit(int(file_done/file_count*100))

        
        print("--- %s seconds ---" % (time.time() - start_time))
        return str      
