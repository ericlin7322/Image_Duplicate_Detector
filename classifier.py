import sys
import os
import tqdm
from PIL import Image

class Classifier:
    def __init__(self) -> None:
        pass

    def classify(self, image, folder):
        im1 = Image.open(image)

        str = []

        for root, dirs, files in os.walk(folder, topdown=False):
            for name in files:
                if name.endswith('.png') or name.endswith('.jpg') or name.endswith('.jpeg'):
                    try:
                        im2 = Image.open(os.path.join(root, name))
                        if im1 == im2:
                            str.append(os.path.join(root, name))
                    except:
                        print(f"Error at {os.path.join(root, name)}")

        return str      