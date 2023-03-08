##################################
#
#  Just ready to test widgets
#
##################################

import sys

import cv2
import PIL.Image
import face_recognition
import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QLabel
)

image_path = "/home/leonel/leonel.jpg"

img = face_recognition.load_image_file(image_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_rgb_copy = img_rgb.copy()
face_locations = face_recognition.face_locations(img_rgb)

# Define scale factor and window size
scale_factor = 1.1
sz1 = img_rgb.shape[1] * 2
sz2 = img_rgb.shape[0] * 2


def drawFaceBound(pixmap, top, right, bottom, left):
    width = right - left
    height = bottom - top
    cX = left + width // 2
    cY = top + height // 2
    M = (abs(width) + abs(height)) / 2

    # Get the resized rectangle points
    newLeft = max(0, int(cX - scale_factor * M))
    newTop = max(0, int(cY - scale_factor * M))
    newRight = min(img_rgb.shape[1], int(cX + scale_factor * M))
    newBottom = min(img_rgb.shape[0], int(cY + scale_factor * M))

    painter = QPainter(pixmap)
    painter.setPen(QColor(0, 0, 255))
    painter.drawRect(left + 10, top + 10, right, bottom)
    painter.setPen(QColor(255, 0, 0))
    # (81, 236, 236, 81)
    # top, right, bottom, left
    painter.drawRect(newTop, newLeft, newBottom, newRight)


def crop():
    image = PIL.Image.open(image_path)
    np_array = np.array(image)
    pixmap = QPixmap(image_path)
    rect = face_recognition.face_locations(np_array)[0]

    drawFaceBound(pixmap, *rect)
    # (81, 236, 236, 81)
    # top, right, bottom, left
    # image_crop = image.copy(top, bottom, left, right)
    # image_crop = image.copy(rect['x'], rect['y'], rect['w'], rect['h'])
    return pixmap


def showImage(image):
    # Show the original image in window resized to double
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', sz1, sz2)
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def drawBounds(face_locations):
    for top, right, bottom, left in face_locations:
        # Draw a box around the face
        # cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

        crop_img = img_rgb[top:bottom, left:right]
        showImage(crop_img)
        # cv2.imwrite('test_crop.png', crop_img)

        # Calculate center points and rectangle side length
        width = right - left
        height = bottom - top
        cX = left + width // 2
        cY = top + height // 2
        M = (abs(width) + abs(height)) / 2

        # Get the resized rectangle points
        newLeft = max(0, int(cX - scale_factor * M))
        newTop = max(0, int(cY - scale_factor * M))
        newRight = min(img_rgb.shape[1], int(cX + scale_factor * M))
        newBottom = min(img_rgb.shape[0], int(cY + scale_factor * M))

        # Draw the circle and bounding boxes
        cv2.circle(img_rgb_copy, (cX, cY), radius=0, color=(0, 0, 255), thickness=2)
        cv2.rectangle(img_rgb_copy, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(img_rgb_copy, (newLeft, newTop), (newRight, newBottom), (255, 0, 0), 2)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        picture = QLabel()
        image_crop = crop()
        picture.setPixmap(image_crop)
        picture.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(picture)


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()


main()

# drawBounds(face_locations)
