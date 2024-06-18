# crowdstrike take-home assignment

https://github.com/4eburator/crowdstrike

The test assignments is implemented in python 3.9+ as web service by means of the following frameworks
and dependencies:
- FastAPI framework
- uvicorn application server
- TinyDB json database

and can be run locally and from Docker container.

**API**

REST API consists of the following methods:

* `POST /scan/<HOST>`
This asynchronous call generates a unique `SCAN_ID`, launchers a background scan of the target host by means of 'nmap' 
tool, and immediately returns `SCAN_ID` (see `ScanSession` model). The background task captures 'nmap' output in XML, 
processes it (coverts to json) and stores in document-based Database TinyDB (json file stored locally per target host).


* `GET /scan/<HOST>/<SCAN_ID>`
The call extracts the scan result of the target host with the requested `SCAN_ID` from the storage and returns it. 


* `GET /diff/<HOST>`
The call retrieves two latest successful scan results of the target host from the storage (if they are available),
compares the port states and returns the difference (if any).


**CONFIGURATION**

- Default application settings are defined in `app/config/crowdstrike_config.py` as `pydantic_settings` and can be 
overridden (see example in `Dockerfile`). 
- `nmap_cli` defines the location and command-line parameters of `nmap` tool
- `storage_connect` defines a connection string for a storage (TinyDB - refers to a local path of json files)
- service port is specified in `main.py` (when started locally)
- internal port is explicitly set in `Dockerfile` 


**STORAGE**

In order to keep implementation easy to implement but open to extend/replace, document-oriented TinyDB
(https://tinydb.readthedocs.io/en/latest/index.html) was chosen (document versions are stored in json files locally).
TinyDB is not thread-safe and obviously cannot be easily replicated and used in distributed setup but still can be 
replaced with any other document-oriented database like MongoDB or Couchbase.


**PREREQUISITES**

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


**TEST STRATEGY**
These tests below I'd like to add in real-life scenario:
- functional tests
- performance/scalability tests
- security tests


**POTENTIAL PROBLEMS AND IMPROVEMENTS**
- hostnames and ip addresses are not normalized and are considered as independent entities;
It can be improved by converting the hostnames into ip addresses just after 'nmap' tool call and before
saving the scan result into storage
- 
- support of new type of storage (document-oriented database) can be added and database service can be
launched from docker-compose together with web-service
- storage clean-up process should be added in order to remote outdated scan results
