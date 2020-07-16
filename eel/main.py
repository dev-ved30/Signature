import os
from os import path
from process import *
import eel

@eel.expose
def process():
    im = input_image()
    im_la = process_image_to_LA_array(im)
    im_shadow_crush = shadow_crusher(im_la)
    save_shadow_crush(im_shadow_crush)
    im_thresh = threshold_image(im_shadow_crush)
    im_alias = alias(im_thresh)
    save_to_temp(im_alias)

@eel.expose
def change_thresh(thresh):
    print("hi")
    print(thresh)
    print(type(thresh))
    im = input_crushed_img()
    im_la = process_image_to_LA_array(im)
    im_thresh = threshold_image(im_la, int(thresh))
    im_alias = alias(im_thresh)
    save_to_temp(im_alias)
    

if __name__=="__main__":
    eel.init('web')
    eel.start('home.html')
    
