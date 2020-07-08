# Signature
Have you ever been in a situation where you wanted to include a picture of your signature in a document, but were held back due to this?

![](images/orignal.png)

That's where `Signature` comes in. Using python, we built a simple utility that does the job. Take a look!

![](images/processed.png)

## Using Locally

### Before Running (Assuming you have pip and git)

* If you're not worried about breaking anything in your environment:
    
    * Run `pip install -r requirements.txt`

* Otherwise, if you're trying to install the dependencies individually:

    * On Windows in `cmd`:

        * Run `pip install numpy`
        * Run `pip install Pillow`
        * Run `pip install opencv-python`

    * On Debian-based Linux in terminal:
        * Run `pip install numpy`
        * Run `pip install Pillow`
        * Run `sudo apt-get install python3.6-tk`
        * Run `sudo apt-get install python3-opencv`

**Note:** For develoment and testing, we used `Tkinter 8.6`, `Pillow 7.1.2`, `Open CV 4.2.0`,`Python 3.7.4` and `Numpy 1.18.4`.

### Running

In your terminal, navigate to the project folder you cloned and run:

`python main.py`

The command assumes python3 is aliased to python. On Windows if you only have Python 3.x installed the aliasing should be done for you, but on Linux you would have be more explicit depending on the distro and its version. So, if the command above fails try:

`python3 main.py`

We do plan on launching an `exe` for the this utility in a future release!

## Found Bugs?

We would appreciate any support in the form of bug reports in order to provide the best possible experience. Bugs can be reported in the `Issues` tab
