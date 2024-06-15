# crowdstrike take-home assignment

**Prerequisite**

- pyenv is installed; see https://github.com/pyenv/pyenv#readme;
- nmap is installed


**Local environment setup commands (MacOS)**

- `SDK_PYTHON_VERSION=3.9.10`
- `ENV_NAME=crowdstrike`
- `pyenv install -v $SDK_PYTHON_VERSION`
- `pyenv virtualenv $SDK_PYTHON_VERSION $ENV_NAME` 
- `pyenv local $ENV_NAME`
- `pip install --upgrade pip`
- `pip install -r requirements.txt`

**Start Web-app:**

***locally from command-line:***

`uvicorn api.v1.nmap_api:app --reload`

**Endpoints:**

*Service endpoint:* http://127.0.0.1:5000

*API documentation:* http://127.0.0.1:5000/docs


**Start in Docker:**

The following Web-Service default settings are defined in app/api/config/crowdstrike_config.py:
- nmap_cli
- storage_connect
However they can be overridden in Dockerfile via environment variable (see example) 

The commands to build a Docker image and launch a container 
- `docker build -t crowdstrike_service .`
- `docker run -d --name crowdstrike -p 80:5000 crowdstrike_service`

*Service endpoint (from docker):* http://127.0.0.1:80


CONFIG:
- nmap: /usr/local/bin/nmap
- logging
- history: storage_connection: file://~/crowdstrike/history
- clean

STORAGE:
key:  hostname / ip
value:
 - scan_version
 - timestamp
 - result_code
 - scan_result


TODO (further development):
- authentication oauth
- new storage type support
- testing