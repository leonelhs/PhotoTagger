import os
import shutil
from os.path import isfile, join

from filetype import is_image

image_folder = "/home/leonel/Photos/galgadot"


def addExtension(folder, extension):
    for file in os.listdir(folder):
        path = join(folder, file)
        if isfile(path):
            if is_image(path):
                current_name, ext = os.path.splitext(path)
                if not ext:
                    os.rename(path, current_name + extension)
                    print(current_name)


def moveFiles(folder, extension, new_path):
    for file in os.listdir(folder):
        path = join(folder, file)
        if isfile(path):
            if is_image(path):
                current_name, ext = os.path.splitext(path)
                if ext == extension:
                    new_path = os.path.join(folder, new_path)
                    new_path = os.path.join(new_path, file)
                    shutil.move(path, new_path)
                    print(new_path)

