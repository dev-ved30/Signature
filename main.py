from tkinter import Tk
from tkinter import filedialog
from PIL import Image
import numpy as np


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
    return im



def process_image_to_RGBA_array(im):
    """
    This function converts the image to RGBA mode if it wasn't already and
    then converts the image into its nd array representation.

    Args:
        im (PIL Image): The image to convert to an nd array in RGBA format
    Returns:
        Numpy array: An nd numpy array. In this case each pixel position has a depth of 4 including the alpha channel.
    """

    im = im.convert("RGBA")
    im_arr = np.array(im)

    return im_arr


def process_signature(im_arr):
    # TODO - This function needs to be implemented
    return im_arr



def save_to_file(im_arr):
    """
    This function saves the given array to a PNG image file. The filename is
    whatever the user inputs in the file dialog box.

    Args:
        im_arr (Numpy array): The nd array representing the image. Make sure it can be converted to RGBA.
    """

    im = Image.fromarray(im_arr, mode="RGBA")

    filename = filedialog.asksaveasfile(mode='wb', defaultextension=".png")

    if filename:
        im.save(filename)
    else:
        print("No save location was chosen")



def main():
    """
    The directive method that runs the application.

    It reads an image, preprocesses it, then processes it and finally
    saves it to a file.
    """
    
    im = input_image()
    im_arr = process_image_to_RGBA_array(im)
    output_im_array = process_signature(im_arr)
    save_to_file(output_im_array)


if __name__ == "__main__":
    main()
