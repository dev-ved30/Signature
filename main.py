import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from process import *


class SignatureFloat(FloatLayout):
    def __init__(self, **kwargs):
        super(SignatureFloat, self).__init__(**kwargs)

        self.choose_button = Button(
            text="Choose an image",
            font_size=32,
            size_hint=(0.5, 0.5),
            pos_hint={"x": 0.25, "y": 0.25},
        )
        self.choose_button.bind(on_press=self.choose_and_prepare_image)
        self.add_widget(self.choose_button)

    def choose_and_prepare_image(self, instance):
        im = input_image()
        self.im_arr = process_image_to_LA_array(im)
        self.im_arr = shadow_crusher(self.im_arr)
        self.remove_widget(self.choose_button)
        self.process_image()

    def process_image(self):
        label = Label(text="Processing...", font_size=50)
        self.add_widget(label)

        self.final_im_arr = threshold_image(self.im_arr)
        self.final_im_arr = alias(self.final_im_arr)

        self.remove_widget(label)

        self.save_button = Button(
            text="Save image",
            font_size=32,
            size_hint=(0.5, 0.5),
            pos_hint={"x": 0.25, "y": 0.25},
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
