# CircuitQuest

Welcome to CircuitQuest, an educational software with gamification elements, all about logic gates and circuits. This software was created as a semester project by a group of students at the University of Agder, Norway.

## Setting up local development
You can automatically install all required packages for the project. First you have to set up a virtual environment for Python. On Linux, it works like this:
````
python3 -m venv env
source env/bin/activate
````

The process on Windows is a bit different:
````
python3 -m venv env
env\Scripts\activate.bat
````

Once you are in the env, run this to install all packages:
````
pip install -r requirements.txt
````

Now you should be good to go to run the app like this:
````
python3 -m src.main
````

When you install a new package, remember to run the following command to update the requirements.txt:
````
pip freeze > requirements.txt
````

## Building the app from source
We have a script that builds the app specifically for your system, the `setup.py`. To run it, execute the following command (remember you have to be in your virtual environment):
````
python3 -m src.setup build
````

It will create a folder with the executable file and other relevant files. It is located inside the `build` folder inside the project root directory. To start the app, just navigate there and run the executable file.
