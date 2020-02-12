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
#  queryRecord.sh


echo
echo "#################################################################"
echo "#######    Query Record:  PATIENT-123   #########################"
echo "#######                   PATIENT-456   #########################"
echo "#######                   PATIENT-789   #########################"
echo "#################################################################"
sudo docker exec cli peer chaincode query -o orderer.patient.com:7050 -C patientchannel -n ehrcc -c '{"function":"queryRecord","Args":["PATIENT-123"]}' && \
sudo docker exec cli peer chaincode query -o orderer.patient.com:7050 -C patientchannel -n ehrcc -c '{"function":"queryRecord","Args":["PATIENT-456"]}' && \
sudo docker exec cli peer chaincode query -o orderer.patient.com:7050 -C patientchannel -n ehrcc -c '{"function":"queryRecord","Args":["PATIENT-789"]}'
