"""
Module providing useful functions and methods that deal with Qt images.
"""
import sys
import filepath
from pyside.qt_wrapper import QtGui
from pyside.qt_wrapper import QtCore


def lighter(image, factor=150):
    '''
    Returns the given image with a lighter color.
    If the factor is equal to 100, nothing will be changed.
    If the factor is greater than 100, this returns a lighter image.
    e.g. Settings factor to 150 returns an image that is 50% brighter.

    @param image: Image to be made lighter
    @type image: C{QImage}
    @param factor: Brightness factor
    @type factor: C{int}
    @rtype: C{QImage}
    '''
    outImage = QtGui.QImage(image)

    if factor == 100:
        return outImage

    alphaImage = outImage.alphaChannel()
    for x in range(outImage.width()):
        for y in range(outImage.height()):
            pixel = outImage.pixel(x, y)
            color = QtGui.QColor(pixel)
            r, g, b, _ = color.getRgbF()
            a = QtGui.QColor(alphaImage.pixel(x, y)).red()

            if a > 5:
                brightness = 1 - (r + g + b) / 3
                color = color.lighter(100 + int((factor-100) * brightness))
                outImage.setPixel(x, y, color.rgb())

    return outImage

def overlay(baseImage, overlayImages):
    '''
    Overlays the list of images on top of the base image.
    The first item of the list is drawn first, and the last item of the list
    is drawn last and becomes the top layer.

    e.g. overlay(baseImage, [img1, img2, img3])

    will have this draw order:

              ------
             |      |
           --|      |
          |  | img3 |
        --|   ------
       |  | img2 |
     --|   ------
    |  | img1 |
    |   ------
    | base |
     ------

     @param baseImage: The base image to be overlayed on.
     @type baseImage: C{QImage}
     @param overlayImages: The list of images for overlay.
     @type overlayImages: C{QImage} list
     @rtype: C{QImage}
    '''
    if not overlayImages:
        return QtGui.QImage(baseImage)

    currentImage = QtGui.QImage(baseImage)

    painter = QtGui.QPainter()
    painter.begin(currentImage)
    for image in overlayImages:
        painter.drawImage(
            QtCore.QRect(0, 0, baseImage.width(), baseImage.height()),
            image,
            QtCore.QRect(0, 0, image.width(), image.height()))
    painter.end()

    return currentImage