from tkinter import Tk
from tkinter import filedialog
import numpy as np
import cv2 as cv
from PIL import Image


def input_image():
    """
    This function asks the user to input a file through the standard OS
    filewindow. It only accepts PNG and JPG files and will print and error to
    the terminal otherwise. It reads an image in greyscale.

    Returns:
        Numpy ndarray: Returns ndarray representing the grayscale image.
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


def threshold_image(im_arr, threshold=204):
    """
    This function accepts an image array and sets all pixels in the grescale channel below the threshold value
    to black.The blackend pixels' alpha channel is set to 255 as well.

    Modifications are executed "in place" (by reference)

    Args:
        im_arr (Numpy ndarray): The array representing the image in LA. IMPORTANT NOTE: The image must have it's entire alpha channel set
        to 0 before being passed to this function.

        threshold (int, optional): Pixels in the greyscale whose value is below this are set to 0. Defaults to 204.

    Returns:
        Numpy array: The thresholded image.
    """
    l_channel = im_arr[:, :, 0]  # Extract the greyscale channel
    # Find positions of pixels whose value is below threshold
    row_indices, col_indices = np.where(l_channel < threshold)
    # Set to black with no transparency
    im_arr[row_indices, col_indices] = [0, 255]
    return im_arr


def save_to_file(im_arr):
    """
    Saves the given image to a file through a dialogbox

    Args:
        im_arr (Numpy array): The image to be saved
    """

    im = Image.fromarray(im_arr, mode="LA")

    filename = filedialog.asksaveasfile(mode='wb', defaultextension=".png")

    if filename:
        im.save(filename)
        im.show()
    else:
        print("No save location was chosen")
        exit(1)


def shadow_crusher(im_arr):
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
    la_planes = cv.split(im_arr)

    result_norm_planes = []
    for plane in la_planes:
        dilated_img = cv.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv.medianBlur(dilated_img, 21)
        diff_img = 255 - cv.absdiff(plane, bg_img)
        norm_img = cv.normalize(
            diff_img, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8UC1)
        result_norm_planes.append(norm_img)

    result_norm = cv.merge(result_norm_planes)

    return result_norm


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
        numpy array: Smoothened image
    """

    img_blur = cv.pyrUp(im_arr)
    img_blur = cv.medianBlur(img_blur, 3)
    img_blur = cv.pyrDown(img_blur)
    return img_blur


def main():
    """
    The directive method that runs the application.

    It reads an image, preprocesses it, then processes it and finally
    saves it to a file.
    """

    im = input_image()
    im_arr = process_image_to_LA_array(im)
    shadow_crushed_im_arr = shadow_crusher(im_arr)
    thresholded_im_arr = threshold_image(shadow_crushed_im_arr)
    aliased_im_array = alias(thresholded_im_arr)
    save_to_file(aliased_im_array)


if __name__ == "__main__":
    main()
