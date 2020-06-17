from tkinter import Tk
from tkinter import filedialog
from PIL import Image
import numpy as np

def input_image():
    root = Tk()
    root.filename = filedialog.askopenfilename(initialdir="/$HOME/", title="Select file", filetypes=(("PNG files", "*.png"),("PNG files", "*.jpg")))
    if root.filename:
        im = Image.open(root.filename)
    else:
        print(" No image was chosen")
    return im

def process_image_to_RGBA_array(im):
    im = im.convert("RGBA")
    im_arr = np.array(im)

    return im_arr

def process_signature(im_arr):
    # TODO - This function needs to be implemented
    return im_arr

def save_to_file(im_arr):
    im = Image.fromarray(im_arr, mode="RGBA")
    
    filename = filedialog.asksaveasfile(mode='wb', defaultextension=".png")

    if filename:
        im.save(filename)
    else:
        print("No save location was chosen")
    


def main():
    im = input_image()
    im_arr = process_image_to_RGBA_array(im)
    output_im_array = process_signature(im_arr)
    save_to_file(output_im_array)

if __name__ == "__main__":
    main()
