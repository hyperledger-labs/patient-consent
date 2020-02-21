# Patient Consent 

# About

Use Case Patient Data in Clinical Trials Automation with focus of Patient Consent.
This prototype includes two versions developed with Sawtooth and Fabric 

# Sawtooth

## Features

### Functional

- Create mandatory participants (like Hospital, Patient and Investigator)
- Patient grants permission to Hospital to process his/her EHR
- Hospital registers new EHRs
- Hospital grants permission to Investigator to read data
- Hospital applies certain exclusion/inclusion criteria to the retrieved EHRs
- Investigator contacts to Patients whose EHRs match the criteria
- Investigator requests Patient to sign Inform Consent document
- Patient signs the document
- Investigator is allowed to import the patient's data and harmonize it.
- Investigator finally identifies if the data is eligible

### Technical

- Private key to store/read data (private key of every participant is stored on server side)
- Private data access management (every participant has a role assigned with corresponding permissions)
- Docker compliance (every component of this project has separate docker image and fully isolated)
- Various network representation (blockchain network has few options (1 node/Dev-Mode consensus, 
  3 nodes/PoET consensus/single VM, 3 nodes/PoET consensus/3 separate VMs)

## Components

- Consent/Identity/Authorization Management smart contract (responsible to operate with identity/permission related 
  data as well as patients' consent)
- Data Management smart contract (responsible to handle EHR patient’s data)
- Investigator Management smart contract (responsible to operate with investigator related data)
- Hospital REST-API service (provides interface between Hospital, Patient and blockchain network)
- hospital Web client (web page where a participant can operate as one of predefined roles such as hospital, 
  patient etc)
- Investigator REST-API service (provides interface between Investigator and blockchain network)
- Investigator Web client (web page where a participant can operate as one of predefined roles such as 
  investigator etc)


## Architecture

![SawtoothArchitecture](https://github.com/AlexZhovnuvaty/patient-consent/blob/master/SawtoothArchitecture.png)

The whole use case is divided on 3 isolated blockchain networks: 
- The 1st one (green) is dedicated for hospitals. They store there all EHR data related to patient
- The 2nd one (blue) is dedicated for investigators. They store there all Clinical Trial data
- The 3rd one (orange) is shared between both types of participants: hospital and investigator. 
  It stores accounts for any participant, their roles and corresponding permissions. Also it includes 
  requested and signed by patients inform consent documents

## Technology stack

Python/Hyperledger Sawtooth/Docker/Docker-Composer/Protobuf/Setuptools/Sanic/Shell/Webpack

## How to setup and run infrastructure (1 node/Dev-Mode consensus)

- Go to root project’s directory
- Clone this repo (if not cloned yet))
- Ensure all containers stopped: “docker-compose down -v --remove-orphans”
- Get recent data from the repo: “git pull”
- Start new containers: “docker-compose up”
