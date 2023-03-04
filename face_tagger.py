import PIL.Image
import face_recognition
import numpy as np
from PIL import UnidentifiedImageError
from face_recognition.api import face_detector


def face_landmarks(np_array, face_locations=None):
    try:
        return face_recognition.face_landmarks(np_array, face_locations)
    except IndexError:
        print("No able to found face landmarks")
        return False


def face_encodings(image, np_array, face_locations=None):
    if max(np_array.shape) > 1600:
        image.thumbnail((1600, 1600), PIL.Image.LANCZOS)
        np_array = np.array(image)
    try:
        return face_recognition.face_encodings(np_array, face_locations)
    except IndexError:
        print("No able to encode face")
        return False


def compareFaces(known_face, unknown_face):
    try:
        return face_recognition.compare_faces(known_face, unknown_face[0])[0]
    except IndexError:
        print("No able to match a face")
        return False


def openImage(image_path):
    try:
        return PIL.Image.open(image_path).convert('RGB')
    except UnidentifiedImageError:
        print("cannot identify image file")
        return None


def getMetadata(image_path):
    metadata = {}
    image = openImage(image_path)
    if image:
        np_array = np.array(image)
        bounds = face_detector(np_array, 1)
        locations = face_recognition.face_locations(np_array)
        metadata["landmarks"] = face_landmarks(np_array, locations)
        metadata["encodings"] = face_encodings(image, np_array, locations)
        image.thumbnail((128, 128), PIL.Image.LANCZOS)
        metadata["pixmap"] = image
        metadata["bounds"] = bounds
        metadata["tags"] = "Unknown"
        return metadata
    return None
