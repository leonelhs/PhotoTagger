import pickle

import PIL.Image
import numpy as np
from face_recognition import face_encodings, face_landmarks, compare_faces


def serialize(data):
    return [pickle.dumps(d) for d in data]


def unserialize(raw):
    return pickle.loads(raw)


def imageOpen(image_path):
    image = PIL.Image.open(image_path)
    return image.convert('RGB')


def processMetadata(image_path):
    image = imageOpen(image_path)
    np_array = np.array(image)
    try:
        encodings = face_encodings(np_array)
        landmarks = face_landmarks(np_array)
        image.thumbnail((128, 128), PIL.Image.LANCZOS)
        return serialize((encodings, landmarks, image))
    except IndexError:
        return None


def compareFaces(known_face, unknown_face):
    try:
        return compare_faces(known_face, unknown_face[0])[0]
    except IndexError:
        return False
