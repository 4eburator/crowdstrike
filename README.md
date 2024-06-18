# crowdstrike take-home assignment

https://github.com/4eburator/crowdstrike

The test assignment is implemented in Python 3.9+ as a web service using the following frameworks and dependencies:
- FastAPI framework
- Uvicorn application server
- TinyDB JSON database

The service can be run both locally and from a Docker container (if `nmap` is installed manually).


**API**

The REST API consists of the following methods:

* `POST /scan/<HOST>`

  This asynchronous call generates a unique SCAN_ID, initiates a background scan of the target host using the `nmap` 
  tool, and immediately returns the `SCAN_ID` (refer to the `ScanSession` model). The background task captures the `nmap` 
  output in XML format, converts it to JSON, and stores it in the TinyDB document-based database (with the JSON file 
  stored locally for each target host).


* `GET /scan/<HOST>/<SCAN_ID>`
  This call retrieves the scan result for the target host with the specified `SCAN_ID` from the storage and returns it. 


* `GET /diff/<HOST>`
  This call fetches the two latest successful scan results for the target host from the storage (if available), 
  compares the port states, and returns any differences found.


**CONFIGURATION**

- Default application settings are defined in `app/config/crowdstrike_config.py` as `pydantic_settings` and can be 
overridden (see example in the `Dockerfile`). 
- `nmap_cli` specifies the location and command-line parameters for the `nmap` tool
- `storage_connect` provides the connection string for the storage (TinyDB, referring to a local path for JSON files)
- The service port is specified in `main.py` when the application is started locally
- The internal port is explicitly set in the Dockerfile


**STORAGE**

To maintain simplicity while allowing for future extensibility or replacement, the document-oriented 
TinyDB (https://tinydb.readthedocs.io/en/latest/index.html) was chosen. Document versions are stored 
in local JSON files. While TinyDB is not thread-safe and does not easily support replication or 
distributed setups, it can be replaced with other document-oriented databases like MongoDB or Couchbase 
if needed.


**PREREQUISITES**

- install `pyenv`: Refer to the installation guide at https://github.com/pyenv/pyenv#readme
- Ensure `nmap` is installed


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

The default settings for the web service are defined in `app/api/config/crowdstrike_config.py`:
- nmap_cli
- storage_connect

- These settings can be overridden in the `Dockerfile` via environment variables (see example).


The commands to build a Docker image and launch a container 
- `docker build -t crowdstrike_service .`
- `docker run -d --name crowdstrike -p 80:5000 crowdstrike_service`

*Service endpoint (from docker):* http://127.0.0.1:80
(`nmap` must be installed manually or via Docker compose)

**TEST STRATEGY**

In a real-life scenario, I would include the following tests:

- Configuration Tests to check if:
  - Storage is initialized correctly (e.g., local folders are created if necessary or opened if they exist)
  - An appropriate error message is displayed if the configuration path is incorrect
  - The service is launched on the specified port
  - API documentation is accessible


- Functional Tests to:
  - Trigger a known host scan and verify that an appropriate record is added to the correct JSON file with a unique UUID 
  - Trigger a sequence of identical host scans in parallel and ensure all are processed correctly and consistently
  - Retrieve a scan result for the known host and compare it with the expected model
  - Trigger a scan for an incorrect host and verify that the scan result status is "FAIL"
  - Conduct multiple target host scans and request the difference between the latest ones
  - Trigger a host scan, open/close a port on the host, trigger another scan, and retrieve the difference
  - Ensure the service can handle 'nmap' output properly, even with incorrect CLI parameters or non-XML output formats 


- Performance/Scalability Tests to:
  - Check if the service response is immediate and independent of background ta
  - Measure latency dependency as the request rate increases 
  - In a multi-container environment, verify the health of the storage
  - Test how auto-balancing distributes the load between service endpoints under dynamic load


- Load/Durability/Endurance Testing to:
  - Verify the service can consistently handle requests over a prolonged period

- Security Tests to:
  - Ensure that only authorized users or service accounts can use the methods



**POTENTIAL PROBLEMS AND IMPROVEMENTS**
- Hostnames and IP addresses are not normalized and are treated as independent entities. This can 
be improved by converting hostnames into IP addresses immediately after the 'nmap' tool call and  
before saving the scan result into storage;

- Support for a new type of storage (document-oriented database) can be added, and the database 
service can be launched from Docker Compose alongside the web service;

- A storage cleanup process should be implemented to remove outdated scan results


Vitalii Sigov
vsigov@yahoo.com
