# automation-tests-3rd
## mc-3rd-automation-tests - test docker
### Contents:
1. 3rd tiles ingestion process


### Deploy and Run:
##### Deploy:
1. Can be deployed as package locally by installing the source into python's environment: \
``pip install . ``
2. Can be deployed as docker - see attached build.sh file that present way of getting tag version to image  
    - can generate image by running build.sh

##### Run [execute] tests:
1. Both docker and local running should be provided with environment relevant variables. mentioned on bottom of documentation
2. If you installed the package locally you should run test folder based on pytest unittest framework.
can see example on file : start.sh
3. In case you would like run as docker, you should provide some extra variables and volumes on running.
     - ``-v /opt/logs/:/opt/logs``
     - ``-v /opt/cert/:/opt/cert`` - in case of running with certification
 
###Environment variables        
|  Variable   | Value       | Mandatory   |   Default   |
| :----------- | :-----------: | :-----------: | :-----------: |
| INGESTION_STACK_URL | API url for ingestion model stack | + | as written on config.py | 
| INGESTION_CATALOG_URL | API url for catalog db | + | as written on config.py |
| INGESTION_JOB_SERVICE_URL | API url for job service | + | as written on config.py |
| FILE_LOGS | For write logs to file | - | 1 | 
| MAX_INGESTION_RUNNING_TIME | Minute buffer value for timeout | - | 5 | 
