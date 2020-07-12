import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.image import Image as KImage
from kivy.core.window import Window
from process import *


def RGBA_to_kvRGBA(RGBA_tup):
    retval = (RGBA_tup[0]/255, RGBA_tup[1]/255,
              RGBA_tup[2]/255, RGBA_tup[3]/255)
    return retval


class SignatureFloat(FloatLayout):

    def __init__(self, **kwargs):
        super(SignatureFloat, self).__init__(**kwargs)
        self.orig_im = None
        self.temp_img = None
        self.add_welcome_label()
        self.add_choose_srcImage_button()

    def choose_image(self, instance):
        self.orig_im = input_image()

        self.remove_widget(self.choose_button)
        self.remove_widget(self.welcome_label)

        self.add_slider()
        self.add_save_image_button()
        self.add_processing_label()
        self.process_image(200)

    def slider_update(self, instance, touch):
        threshold = self.slider.value
        self.process_image(threshold)
        self.temp_img.reload()

    def process_image(self, thresh):
        self.im_arr = process_image_to_LA_array(self.orig_im)
        self.im_arr = shadow_crusher(self.im_arr)
        self.final_im_arr = threshold_image(self.im_arr, threshold=thresh)
        self.final_im_arr = alias(self.final_im_arr)
        save_to_temp(self.final_im_arr)

        self.remove_widget(self.label)

        if self.temp_img is None:
            self.add_temp_image()
        else:
            self.temp_img.reload()

    def save_image(self, instance):
        save_to_file(self.final_im_arr)

    def add_temp_image(self):
        self.temp_img = KImage(source=".temp.png", size_hint=(
            0.80, 0.5), pos_hint={"x": 0.10, "y": 0.40})
        self.add_widget(self.temp_img)

    def add_welcome_label(self):
        self.welcome_label = Label(
            text="Welcome to signature :)",
            font_size=80,
            color=RGBA_to_kvRGBA((0, 0, 0, 255)),
            size_hint=(0.5, 0.5),
            pos_hint={"x": 0.25, "y": 0.35},
        )
        self.add_widget(self.welcome_label)

    def add_choose_srcImage_button(self):
        self.choose_button = Button(
            text="Choose an image",
            font_size=32,
            size_hint=(0.5, 0.25),
            pos_hint={"x": 0.25, "y": 0.05},
            background_normal='',
            background_color=RGBA_to_kvRGBA((86, 186, 190, 255))
        )
        self.choose_button.bind(on_press=self.choose_image)
        self.add_widget(self.choose_button)

    def add_save_image_button(self):
        self.save_button = Button(
            text="Save image",
            font_size=32,
            size_hint=(0.25, 0.20),
            pos_hint={"x": 0.70, "y": 0.05},
            background_normal='',
            background_color=RGBA_to_kvRGBA((86, 186, 190, 255))
        )
        self.save_button.bind(on_press=self.save_image)
        self.add_widget(self.save_button)

    def add_processing_label(self):
        self.label = Label(text="Processing...", font_size=80,
                           color=RGBA_to_kvRGBA((0, 0, 0, 255)))
        self.add_widget(self.label)

    def add_slider(self):
        self.slider = Slider(min=0, max=255, value=200, size_hint=(
            0.60, 0.20), pos_hint={"x": 0.05, "y": 0.05})
        self.slider.bind(on_touch_up=self.slider_update)
        self.add_widget(self.slider)


class SignatureApp(App):
    def build(self):
        return SignatureFloat()


if __name__ == "__main__":
    Window.clearcolor = RGBA_to_kvRGBA((193, 199, 198, 255))
    Window.size = (1440, 900)
    SignatureApp().run()
