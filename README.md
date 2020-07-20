# Signature
Have you ever been in a situation where you wanted to include a picture of your signature in a document, but were held back due to this?

![](images/orignal.png)

That's where `Signature` comes in. Using python, we built a simple utility that does the job. Take a look!

![](images/processed.png)

## Using

### From the releases (for standard users)

* Download the appropriate zipped folder for your operating system from our [releases page](https://github.com/dev-ved30/Signature/releases)
* Unzip the folder.
* Run `main` by double clicking the executable.
* That's it! You should now be up and running :)


### From the repo (For developers who want to work with the code)
* Before Running (Assuming you have pip, git and an appropriate version of python):
    * If you're not worried about breaking anything in your environment:
        * On Windows:
            * Run `pip install -r win_requirements.txt`
        * On MacOS/Linux:
            * Run `pip install -r unix_requirements.txt`
            
    * Otherwise, if you're trying to install the dependencies individually:
        * Run `pip install numpy`
        * Run `pip install Pillow`
        * Run `pip install opencv-python`
        * Run `pip install eel`

**Note:** For develoment and testing, we used `Python 3.7.x`,`Eel 0.13.2`, `Pillow 7.2.0`, `Open CV 4.3.0.36`, and `Numpy 1.19.0`.

* Running: 
    * In your terminal, navigate to the project folder you cloned
    * Run `python main.py` (Remember to use python3)
     
## Found Bugs?

We would appreciate any support in the form of bug reports in order to provide the best possible experience. Bugs can be reported in the `Issues` tab
