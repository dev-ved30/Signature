import os.path
from process import *
import eel


@eel.expose
def process_img():
    """
    This function is exposed to eel. It takes the image from tkinter, processes it and saves the image as a temp.
    It also saves a copy of the shadow crushed image to prevent redundant computations when the threshold is being
    tweaked.
    """
    im = input_image()
    if im:
        im_la = process_image_to_LA_array(im)
        im_shadow_crush = shadow_crusher(im_la)
        save_shadow_crush(im_shadow_crush)

        im_thresh = threshold_image(im_shadow_crush)
        im_alias = alias(im_thresh)

        save_to_temp(im_alias)

        return 1
    else:
        return 0


@eel.expose
def change_thresh(thresh):
    """
    This function is exposed to eel. It takes the shadow crushed image saved in the web folder (temp), applies the new threshold, 
    aliases it and then overwrites the temp image.

    It also prints updates to the terminal
    """
    im = input_crushed_img()
    im_la = process_image_to_LA_array(im)

    im_thresh = threshold_image(im_la, int(thresh))
    im_alias = alias(im_thresh)

    save_to_temp(im_alias)


@eel.expose
def save_final_image():
    """
    This function is exposed to eel. It takes the temp image saved in the web folder (temp) and saves it in the user defined location
    with the user defined name using tkinter. It deletes the images in the temp folder.

    It also prints updates to the terminal
    """
    is_saved = save_final()
    if is_saved:
        os.remove(os.path.join("web/temp/.shadow.png"))
        os.remove(os.path.join("web/temp/.temp.png"))
        return 1
    else:
        return 0

if __name__ == "__main__":
    eel.init("web")
    eel.start("home.html")

