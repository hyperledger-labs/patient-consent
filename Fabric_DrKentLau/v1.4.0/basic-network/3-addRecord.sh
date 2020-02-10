#!/bin/bash

#  Dr Kent G Lau
#  kenty@kenty.com
#  February 2020

#  For testing use only.  No guarantees or warranties provided whatsoever.
#  SPDX-License-Identifier: Apache-2.0

#  Hyperledger Healthcare Special Interest Group (SIG)
#  Patient Consent
#  Clinical Trial Protocol

#  http://github.com/hyperledger-labs/patient-consent
#  1org1peer1channel
#  basic-network
#  addRecord.sh


echo
echo "#################################################################"
echo "#######    Add Record:  PATIENT-123   ###########################"
echo "#######                 PATIENT-456   ###########################"
echo "#######                 PATIENT-789   ###########################"
echo "#################################################################"
sudo docker exec cli peer chaincode invoke -o orderer.patient.com:7050 -C patientchannel -n ehrcc -c '{"function":"addRecord","Args":["PATIENT-123","18","F","18","5.0","N","N","asian","N","Y"]}' &&
sudo docker exec cli peer chaincode invoke -o orderer.patient.com:7050 -C patientchannel -n ehrcc -c '{"function":"addRecord","Args":["PATIENT-456","30","M","22","7.0","Y","N","asian","N","N"]}' &&
sudo docker exec cli peer chaincode invoke -o orderer.patient.com:7050 -C patientchannel -n ehrcc -c '{"function":"addRecord","Args":["PATIENT-789","55","M","30","9.9","N","Y","asian","Y","N"]}'
