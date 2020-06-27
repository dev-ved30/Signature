from tkinter import Tk
from tkinter import filedialog
from PIL import Image
import numpy as np
import cv2


def input_image():
    """
    This function asks the user to input a file through the standard OS
    filewindow. It only accepts PNG and JPG files and will print and error to
    the terminal otherwise.

    Returns:
        PIL Image: The image read from file
    """

    root = Tk()
    root.filename = filedialog.askopenfilename(
        initialdir="/$HOME/",
        title="Select file",
        filetypes=(
            ("PNG files",
             "*.png"),
            ("PNG files",
             "*.jpg")))
    if root.filename:
        im = Image.open(root.filename)
    else:
        print("No image was chosen")
        exit(1)
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


def process_signature(im_arr):
    """
    This function takes the numpy array of an image and goes through it pixel by pixel.
    It checks if a pixel is above a certain threshold value. If it is, the pixel is turned
    to a transparent pixel. Else, it gets converted to dark grey.

    Args:
        im_arr (numpy array): Numpy array that needs to be edited

    Returns:
        numpy array: Edited numpy array
    """
    threshold = 204
    shape = im_arr.shape
    rows = shape[0]
    columns = shape[1]
    for i in range(rows):
        for j in range(columns):
            if im_arr[i][j][0] > threshold:
                # if brightness > threshold then assume it is part of the background and make it transparent.
                im_arr[i][j][1] = 0
            else:
                im_arr[i][j][0] = 15
                # Else make opaque with black value of 15
                im_arr[i][j][1] = 255
    return im_arr


def save_to_file(im_arr):
    """
    This function saves the given array to a PNG image file. The filename is
    whatever the user inputs in the file dialog box.

    Args:
        im_arr (Numpy array): The nd array representing the image. Make sure it can be converted to LA.
    """

    im = Image.fromarray(im_arr, mode="LA")

    filename = filedialog.asksaveasfile(mode='wb', defaultextension=".png")

    if filename:
        im.save(filename)
        im.show()
    else:
        print("No save location was chosen")
        exit(1)


def shadow_crusher(img):
    """
    This function takes the numpy LA array of an image and removes the shadows.
    It returns a normalised image in the form of an array.

    Steps:

    Split: Changes mutlichannel image to 2 seperate single channel Images

    Dilation: This uses pixel clusters to dilate the image. It replaces the 
    parts of the image where content appears with white squares that are 7 by 7
    pixels which helps remove the content while preserving the shadows

    Median Blur: This blurs or smoothens the dilated image. As a result,
    the places from where the content is removed does not appear to be 
    pixelated. The aperture size is 21.

    Absolute Difference: This compares the orignal image with the blurred one,
    pixel by pixel. If the difference between those is 255, which it would be for
    pixels containing content, diff_image is assigned the value 0, which would make
    those pixels black. Else, the pixel will get a whiter shade due to the difference.

    Normalize: Normalizes the image to use the entire 8 bit range. alpha is the lower
    boundary while beta is the upper one. It makes light parts of the image lighter and
    dark part darker. This makes it easier to work with higher thresholds in the 
    process_signature function.

    Merge: Merges the different channels of the image into a single image.

    Args:
        img (numpy array): Image for which that shadow needs to be removed

    Returns:
        [numpy array]: Normalized Image with the shadows removed or flattened.
    """
    la_planes = cv2.split(img)

    result_norm_planes = []
    for plane in la_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(
            diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_norm_planes.append(norm_img)

    result_norm = cv2.merge(result_norm_planes)

    return result_norm


def alias(img):
    """
    This function takes an image as a numpy array and smoothens the jaggy edges that are caused 
    due to the thresholding. 

    Steps:

    Thresholding: Converts Image to a black and white one using the second parameter as the threshold.

    Pyr Up: Increases the image to twice it's orignal size using the image pyramid methodology

    Median Blur: Blurs the image images to soften the edges

    Pyr Down: Decreases the image to half it's sized up version using the image pyramid methodology

    Args:
        img (numpy array): Image that needs to be smoothened

    Returns:
        numpy array: Smoothened image
    """

    img_blur = cv2.pyrUp(img)
    img_blur = cv2.medianBlur(img_blur, 3)
    img_blur = cv2.pyrDown(img_blur)
    return img_blur


def main():
    """
    The directive method that runs the application.

    It reads an image, preprocesses it, then processes it and finally
    saves it to a file.
    """

    im = input_image()
    im_arr = process_image_to_LA_array(im)
    im_arr = shadow_crusher(im_arr)
    im_arr = process_signature(im_arr)
    output_im_array = alias(im_arr)

    save_to_file(output_im_array)


if __name__ == "__main__":
    main()
