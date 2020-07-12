import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.image import Image as KImage
from kivy.core.window import Window
from process import *

Window.clearcolor = (1,1,1,1)
Window.size = (1440, 900)


class SignatureFloat(FloatLayout):
    def __init__(self, **kwargs):
        super(SignatureFloat, self).__init__(**kwargs)

        self.welcome_label = Label(
            text="Welcome to signature :)",
            font_size=50,
            color = (0,0,0,1),
            size_hint=(0.5, 0.5),
            pos_hint={"x": 0.25, "y": 0.35},
        )
        self.add_widget(self.welcome_label)
        self.choose_button = Button(
            text="Choose an image",
            font_size=32,
            size_hint=(0.5, 0.25),
            pos_hint={"x": 0.25, "y": 0.05},
        )
        self.choose_button.bind(on_press=self.choose_and_prepare_image)
        self.add_widget(self.choose_button)

    def choose_and_prepare_image(self, instance):
        self.orig_im = input_image()
        self.temp_img = None
        self.remove_widget(self.choose_button)
        self.remove_widget(self.welcome_label)

        self.slider = Slider(min=0, max=255, value=200, size_hint=(0.60, 0.20), pos_hint={"x": 0.05, "y": 0.05})
        self.slider.bind(on_touch_up=self.slider_update)
        self.add_widget(self.slider)

        self.process_image(200)
    
    def slider_update(self, instance, touch):
        threshold = self.slider.value
        self.process_image(threshold)
        self.temp_img.reload()


    def process_image(self, thresh):
        label = Label(text="Processing...", font_size=50)
        self.add_widget(label)

        self.im_arr = process_image_to_LA_array(self.orig_im)
        self.im_arr = shadow_crusher(self.im_arr)
        self.final_im_arr = threshold_image(self.im_arr, threshold=thresh)
        self.final_im_arr = alias(self.final_im_arr)
        save_to_temp(self.final_im_arr)
        
        self.remove_widget(label)

        if self.temp_img is None:


            self.temp_img = KImage(
            source="temp.png", size_hint=(0.5, 0.5), pos_hint={"x": 0.25, "y": 0.25}
            )        
            self.add_widget(self.temp_img)
        else:
            self.temp_img.reload()

        self.save_button = Button(
            text="Save image",
            font_size=32,
            size_hint=(0.25, 0.20),
            pos_hint={"x": 0.70, "y": 0.05},
        )
        self.save_button.bind(on_press=self.save_image)
        self.add_widget(self.save_button)

    def save_image(self, instance):
        save_to_file(self.final_im_arr)


class SignatureApp(App):
    def build(self):
        return SignatureFloat()


if __name__ == "__main__":
    SignatureApp().run()
