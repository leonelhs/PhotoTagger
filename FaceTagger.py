import pickle

import PIL.Image
import face_recognition
import numpy as np

# Exif metadata tags
# FACE_TAGS = 0x9286
# ENCODINGS = 42020
# LANDMARKS = 42022

ENCODINGS = 42020
LANDMARKS = 42022
FACE_TAGS = 42024


def serialize(data):
    return pickle.dumps(data)


def unserialize(raw):
    return pickle.loads(raw)


def face_landmarks(np_array, face_locations=None):
    try:
        return face_recognition.face_landmarks(np_array, face_locations)
    except IndexError:
        return False


def face_encodings(image, np_array, face_locations=None):
    if max(np_array.shape) > 1600:
        image.thumbnail((1600, 1600), PIL.Image.LANCZOS)
        np_array = np.array(image)
    try:
        return face_recognition.face_encodings(np_array, face_locations)
    except IndexError:
        return False


def compareFaces(known_face, unknown_face):
    try:
        return face_recognition.compare_faces(known_face, unknown_face[0])[0]
    except IndexError:
        return False


def openImage(image_path):
    return PIL.Image.open(image_path).convert('RGB')


def saveImageMetadata(image_path, exif):
    image = openImage(image_path)
    exif[LANDMARKS] = serialize(exif[LANDMARKS])
    exif[ENCODINGS] = serialize(exif[ENCODINGS])
    exif[FACE_TAGS] = serialize(exif[FACE_TAGS])
    try:
        image.save(image_path, exif=exif)
    except OSError:
        print("No able to save %s " % image_path)
        return False


def getMetadata(image_path):
    image = openImage(image_path)
    exif = image.getexif()

    if exif.get(FACE_TAGS):
        image.thumbnail((128, 128), PIL.Image.LANCZOS)
        try:
            return unserialize(exif[ENCODINGS]), unserialize(exif[LANDMARKS]), image, unserialize(exif[FACE_TAGS])
        except KeyError:
            print("No able to open %s " % image_path)
            return None
    else:
        np_array = np.array(image)
        locations = face_recognition.face_locations(np_array)
        exif[LANDMARKS] = face_landmarks(np_array, locations)
        exif[ENCODINGS] = face_encodings(image, np_array, locations)
        exif[FACE_TAGS] = ""
        image.thumbnail((128, 128), PIL.Image.LANCZOS)
        saveImageMetadata(image_path, exif)
        return exif[LANDMARKS], exif[ENCODINGS], image, ""
