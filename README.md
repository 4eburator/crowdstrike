# crowdstrike take-home assignment

**Prerequisite**

- pyenv is installed; see https://github.com/pyenv/pyenv#readme;


**Environment setup commands (MacOS)**

- SDK_PYTHON_VERSION=3.9.10
- ENV_NAME=crowdstrike
- pyenv install -v $SDK_PYTHON_VERSION
- pyenv virtualenv $SDK_PYTHON_VERSION $ENV_NAME 
- pyenv local $ENV_NAME
- pip install --upgrade pip
- pip install -r requirements.txt

