# only once
virtualenv venv
source venv/bin/activate
##windows: venv\Scripts\activate.bat
pip install -r requirements.txt

# on every function update
zip -r functions.zip __main__.py venv
ibmcloud fn action update main functions.zip --kind=python:3.6 --param-file parameters.json

# test your update with manually invoking function
ibmcloud fn action invoke main --result