# A really cool Readme.md!

## Setup local development
You can automatically install all required packages for the project. If you do not have an env in your project directory yet, run this:
````
python3.13 -m venv env
source env/bin/activate
````

Then run this to install all packages in your env:
````
pip install -r requirements.txt
````

When you install a new package, remember to run the following command to update the requirements.txt:
````
pip freeze > requirements.txt
````
