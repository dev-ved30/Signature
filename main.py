import kivy
import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.image import Image as KImage
from kivy.core.window import Window
from process import *


def RGBA_to_kvRGBA(RGBA_tup):
    """
    Converts normal RGBA values into Kivy's relative representation and returns the converted tuple.

    Args:
        RGBA_tup (tuple): The tuple of standard RGBA values

    Returns:
        tuple: Kivy's representation of RGBA values
    """
    retval = (
        RGBA_tup[0] / 255,
        RGBA_tup[1] / 255,
        RGBA_tup[2] / 255,
        RGBA_tup[3] / 255,
    )
    return retval


class SignatureFloat(FloatLayout):
    def __init__(self, **kwargs):
        """Initializes the Float window for the app
        """
        super(SignatureFloat, self).__init__(**kwargs)

        self.orig_im = None
        self.temp_img = None

        self.start()

    def start(self):
        """The window to get the process started.
        """
        self.add_welcome_label()
        self.add_choose_srcImage_button()

    def choose_image(self, instance):
        """
        This function is called when the user clicks the choose image button.

        Args:
            instance: The instance of the button that is passed in. 
        """
        self.orig_im = input_image()

        # Get rid of the stuff from the start screen
        self.remove_widget(self.choose_button)
        self.remove_widget(self.welcome_label)

        # Prepare the things we want to display next
        self.add_slider()
        self.add_save_image_button()
        self.add_processing_label()

        # The first time we call process_image we set threshold to 200
        self.process_image(200)

    def slider_update(self, instance, touch):
        """
        This function is called when the user clicks away from the slider.

        Args:
            instance : Instance of the slider being used
            touch : The coordinates that were clicked
        """
        # Get and use the threshold value to reprocess the image with the user's threshold
        threshold = self.slider.value
        self.process_image(threshold)

    def process_image(self, thresh):
        """
        Processes the image with the given threshold value.

        Args:
            thresh (float): The threshold value to process the image based on
        """

        # Process the image
        self.im_arr = process_image_to_LA_array(self.orig_im)
        self.im_arr = shadow_crusher(self.im_arr)
        self.final_im_arr = threshold_image(self.im_arr, threshold=thresh)
        self.final_im_arr = alias(self.final_im_arr)

        # Save to the temporary file internally
        save_to_temp(self.final_im_arr)
        self.remove_widget(self.label)

        if self.temp_img is None:
            # If this is the first time the function is called, add the temporary image
            self.add_temp_image()
        else:
            # Reload the image everytime the threshold is modified
            # Reloading reloads from the temporary image we update internally
            self.temp_img.reload()

    def save_image(self, instance):
        """
        Called when the user clicks the save image button.

        Args:
            instance : Instance of the calling button
        """
        save_to_file(self.final_im_arr)

    def add_temp_image(self):
        """Adds a temporary image for the class to keep track of. This image is used to update the
        real time representation the user sees.
        """
        self.temp_img = KImage(
            source=".temp.png", size_hint=(0.80, 0.5), pos_hint={"x": 0.10, "y": 0.40}
        )
        self.add_widget(self.temp_img)

    def add_welcome_label(self):
        """
        Adds the welcome label used for the start screen.
        """
        self.welcome_label = Label(
            text="Welcome to signature :)",
            font_size=80,
            color=RGBA_to_kvRGBA((0, 0, 0, 255)),
            size_hint=(0.5, 0.5),
            pos_hint={"x": 0.25, "y": 0.35},
        )
        self.add_widget(self.welcome_label)

    def add_choose_srcImage_button(self):
        """Adds the button the user needs to click on the start screen to choose an image.
        """
        self.choose_button = Button(
            text="Choose an image",
            font_size=32,
            size_hint=(0.5, 0.25),
            pos_hint={"x": 0.25, "y": 0.05},
            background_normal="",
            background_color=RGBA_to_kvRGBA((86, 186, 190, 255)),
        )
        self.choose_button.bind(on_press=self.choose_image)
        self.add_widget(self.choose_button)

    def add_save_image_button(self):
        """Adds the button used to save an image.
        """
        self.save_button = Button(
            text="Save image",
            font_size=32,
            size_hint=(0.25, 0.20),
            pos_hint={"x": 0.70, "y": 0.05},
            background_normal="",
            background_color=RGBA_to_kvRGBA((86, 186, 190, 255)),
        )
        self.save_button.bind(on_press=self.save_image)
        self.add_widget(self.save_button)

    def add_processing_label(self):
        """Adds the label that is shown while the image is being processed.
        """
        self.label = Label(
            text="Processing...", font_size=80, color=RGBA_to_kvRGBA((0, 0, 0, 255))
        )
        self.add_widget(self.label)

    def add_slider(self):
        """Adds the sldie the user uses to adjust the threshold.
        """
        self.slider = Slider(
            min=0,
            max=255,
            value=200,
            size_hint=(0.60, 0.20),
            pos_hint={"x": 0.05, "y": 0.05},
        )
        self.slider.bind(on_touch_up=self.slider_update)
        self.add_widget(self.slider)


class SignatureApp(App):
    """The app for Signature backed by a Float layout
    """

    def build(self):
        return SignatureFloat()


if __name__ == "__main__":

    # Make the root window grey and set its resolution to be 1440x900
    Window.clearcolor = RGBA_to_kvRGBA((193, 199, 198, 255))
    Window.size = (1440, 900)

    # Run the app
    SignatureApp().run()

    # Delete the temporary file after each run
    os.remove(".temp.png")
