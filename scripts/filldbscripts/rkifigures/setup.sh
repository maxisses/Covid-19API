# only once
virtualenv venv

source venv/bin/activate
##windows: venv\Scripts\activate.bat or powershell venv\Scripts\Activate.ps1
pip install -r requirements.txt

# on every function update
zip -r functions.zip __main__.py venv
#windows: zip -r functions.zip __main__.py venv parameters.json

ibmcloud fn action create rkidailyload functions.zip --kind=python:3.6 --timeout 600000
## ibmcloud fn action update rkidailyload functions.zip --kind=python:3.6 --timeout 600000
## ibmcloud fn action update testparams functions.zip --kind=python:3.6 --timeout 600000 --param-file parameters.json

# test your update with manually invoking function
ibmcloud fn action invoke rkidailyload --result

## get the logs
# ibmcloud fn activation list
# ibmcloud fn activation get <id>
