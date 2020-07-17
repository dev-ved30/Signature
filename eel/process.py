from tkinter import Tk
from tkinter import filedialog
import numpy as np
import cv2 as cv
from PIL import Image
import os.path


def input_image():
    """
    This function asks the user to input a file through the standard OS
    filewindow. It only accepts PNG and JPG files and will print and error to
    the terminal otherwise. It reads an image in greyscale.
    Returns:
        PIL Image: The image read from file
    """

    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    root.lift()
    root.filename = filedialog.askopenfilename(
        initialdir="/$HOME/",
        title="Select file",
        filetypes=(("PNG files", "*.png"), ("PNG files", "*.jpg")),
    )
    if root.filename:
        im = Image.open(root.filename)
    else:
        print("No image was chosen")
        exit(1)
    return im

def input_crushed_img():
    """
    This function opens the shadow crushed image from the temp folder and returns it.

    Returns:
        image[.png]: shadow crushed image
    """
    filename = os.path.join("web/temp/.shadow.png")
    im = Image.open(filename)
    return im

def input_temp_img():
    """
    This function opens the temp image from the temp folder and returns it.

    Returns:
        image[.png]: temp image
    """
    filename = os.path.join("web/temp/.temp.png")
    im = Image.open(filename)
    return im


def process_image_to_LA_array(im):
    """
    This function converts the image to LA mode if it wasn't already and
    then converts the image into its nd array representation.
    Args:
        im (PIL Image): The image to convert to an nd array in LA format
    Returns:
        Numpy array: An nd numpy array. In this case each pixel position has a depth of 2 including the alpha channel.
    """

    im = im.convert("LA")
    im_arr = np.array(im)
    return im_arr


def threshold_image(im_arr, threshold=204):
    """
    This function accepts an image array and sets all pixels in the grescale channel below the threshold value
    to black. The blackend pixels' alpha channel is set to 255 as well.

    Modifications are executed "in place" (by reference)

    Note: This function first modifies the image to have a completely tansparent alpha channel (values = 0). It then checks which
    pixels in greyscale are below the threshold value and then converts them to black and opaque.

    Args:
        im_arr (Numpy array): The array representing the image in LA.

        threshold (int, optional): Pixels in the greyscale whose values are below this threshold are set to [0,255]. Threshold to 204.

    Returns:
        Numpy array: The thresholded image.
    """

    im_arr[:, :, 1] = 0  # setting the entire alpha channel to 0

    l_channel = im_arr[:, :, 0]  # Extract the greyscale channel
    # Find positions of pixels whose value is below threshold
    row_indices, col_indices = np.where(l_channel < threshold)
    # Set to black with no transparency
    im_arr[row_indices, col_indices] = [0, 255]

    return im_arr


def save_to_file(im_arr):
    """
    Saves the given image to a file through the OS filedialog.

    Args:
        im_arr (Numpy array): The image to be saved
    """

    im = Image.fromarray(im_arr, mode="LA")

    filename = filedialog.asksaveasfile(mode="wb", defaultextension=".png")

    if filename:
        im.save(filename)
        print("Final image saved")
        im.show()
    else:
        print("No save location was chosen")
        pass


def save_to_temp(im_arr):
    """
    Saves the given image to the temp file through the OS filedialog.

    Args:
        im_arr (Numpy array): The image to be saved
    """

    im = Image.fromarray(im_arr, mode="LA")

    temp_file = open(os.path.join("web/temp/.temp.png"), "wb")

    im.save(temp_file)
    print("Temp image is saved")

def save_shadow_crush(im_arr):
    """
    Saves the given image to the shadow file through the OS filedialog.

    Args:
        im_arr (Numpy array): The image to be saved
    """

    im = Image.fromarray(im_arr, mode="LA")

    temp_file = open(os.path.join("web/temp/.shadow.png"), "wb")

    im.save(temp_file)
    print("Shadow Crushed Image is saved")


def shadow_crusher(im_arr):
    """
    This function takes the numpy LA array of an image and removes the shadows.
    It returns a normalised image in the form of an array.

    Modifications to the greyscale channel are made in-place.

    Steps:

    Extract: Extract the greyscale channel and perform the following on it.

    Dilation: This uses pixel clusters to dilate the channel. It replaces the
    parts of the channel where content appears with white squares that are 7 by 7
    pixels which helps remove the content while preserving the shadows.

    Median Blur: This blurs or smoothens the dilated channel. As a result,
    the places from where the content is removed do not appear to be
    pixelated. The aperture size is 21.

    Absolute Difference: This compares the orignal channel with the blurred one,
    pixel by pixel. If the difference between those is 255, which it would be for
    pixels containing content, diff_image is assigned the value 0, which would make
    those pixels black. Else, the pixel will get a whiter shade due to the difference.

    Normalize: Normalizes the channel to use the entire 8 bit range. alpha is the lower
    boundary while beta is the upper one. It makes light parts of the image lighter and
    dark part darker. This makes it easier to work with higher thresholds in the
    process_signature function.

    Set: Set the image's greyscale channel equal to the normalized channel

    Args:
        img (Numpy array): Image for which that shadow needs to be removed

    Returns:
        Numpy array: Normalized Image with the shadows removed or flattened.
    """
    l_plane = im_arr[:, :, 0]

    dilated_img = cv.dilate(l_plane, np.ones((7, 7), np.uint8))
    bg_img = cv.medianBlur(dilated_img, 21)
    diff_img = 255 - cv.absdiff(l_plane, bg_img)
    im_arr[:, :, 0] = cv.normalize(
        diff_img, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8UC1
    )

    return im_arr


def alias(im_arr):
    """
    This function takes an image as a numpy array and smoothens the jaggy edges that are caused
    due to the thresholding.

    Steps:

    Pyr Up: Increases the image to twice it's orignal size using the image pyramid methodology

    Median Blur: Blurs the image images to soften the edges

    Pyr Down: Decreases the image to half it's sized up version using the image pyramid methodology

    Args:
        img (numpy array): Image that needs to be smoothened

    Returns:
        Numpy array: Smoothened image
    """

    img_blur = cv.pyrUp(im_arr)
    img_blur = cv.medianBlur(img_blur, 3)
    img_blur = cv.pyrDown(img_blur)
    return img_blur

def main():
    im = input_image()
    im_la = process_image_to_LA_array(im)
    im_shadow_crush = shadow_crusher(im_la)
    im_thresh = threshold_image(im_shadow_crush)
    im_alias = alias(im_thresh)
    save_to_file(im_alias)