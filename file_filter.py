import os
from os.path import join, isfile

from filetype import is_image

from meta_data import MetaData


class FileFilter:
    def __init__(self, folder):
        self.__slim_metadata_list = []
        self.__fat_metadata_list = []
        self.__filter(folder)

    def __call__(self, *args, **kwargs):
        return self.__slim_metadata_list

    def __len__(self):
        return len(self.__slim_metadata_list)

    def __filter(self, folder):
        for file in os.listdir(folder):
            path = join(folder, file)
            if isfile(path):
                if is_image(path):
                    file_data = {"path": path, "folder": folder, "file": file, "tags": ""}
                    self.__slim_metadata_list.append(file_data)

    def progress(self):
        return len(self.__fat_metadata_list) * 100 / len(self)

    def append(self, slim_data, fat_data):
        slim_data["encodings"] = fat_data["encodings"]
        slim_data["landmarks"] = fat_data["landmarks"]
        slim_data["bounds"] = fat_data["bounds"]
        slim_data["pixmap"] = fat_data["pixmap"]
        slim_data["tags"] = fat_data["tags"]
        self.__fat_metadata_list.append(slim_data)

    def values(self):
        return self.__fat_metadata_list

    def metadataList(self):
        return [MetaData(metadata) for metadata in self.values()]
