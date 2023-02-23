import pickle
from copy import copy

import PIL.Image
import numpy as np
import face_recognition

# Exif new metadata tags
ENCODINGS = 42020
LANDMARKS = 42022
FACE_TAGS = 42024


def serialize(data):
    return pickle.dumps(data)


def unserialize(raw):
    return pickle.loads(raw)


def face_landmarks(image):
    try:
        np_array = np.array(image)
        return face_recognition.face_landmarks(np_array)
    except IndexError:
        return False


def face_encodings(image):
    image = np.array(image)
    if max(image.shape) > 1600:
        shorten_image = PIL.Image.fromarray(image)
        shorten_image.thumbnail((1600, 1600), PIL.Image.LANCZOS)
        image = np.array(shorten_image)
    try:
        return face_recognition.face_encodings(image)
    except IndexError:
        return False


def compareFaces(known_face, unknown_face):
    try:
        return face_recognition.compare_faces(known_face, unknown_face[0])[0]
    except IndexError:
        return False


def openImage(image_path):
    return PIL.Image.open(image_path)


def openImageTuple(image_path):
    original = openImage(image_path)
    clone = copy(original)
    clone.convert('RGB')
    return original, clone


def thumb(image):
    image.thumbnail((128, 128), PIL.Image.LANCZOS)
    return image


def getMetadata(image_path):

    try:
        image_original, image_clone = openImageTuple(image_path)
    except OSError:
        print("Not able to open image %s" % (image_path,))
        return None

    exif = image_original.getexif()

    try:
        return unserialize(exif[ENCODINGS]), \
            unserialize(exif[LANDMARKS]), \
            thumb(image_clone), \
            exif[FACE_TAGS]
    except KeyError:
        try:
            landmarks = face_landmarks(image_original)
            encodings = face_encodings(image_original)
            exif[ENCODINGS] = serialize(encodings)
            exif[LANDMARKS] = serialize(landmarks)
            exif[FACE_TAGS] = ""
            return encodings, landmarks, thumb(image_clone), ""
        finally:
            try:
                image_original.save(image_path, exif=exif)
            except OSError:
                print("Not able to save image %s" % (image_path,))
                return None
