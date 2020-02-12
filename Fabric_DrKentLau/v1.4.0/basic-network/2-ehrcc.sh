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
#  ehrcc.sh


echo
echo "#################################################################"
echo "#######    List all INSTALLED chaincode   #######################"
echo "#################################################################"
sudo docker exec cli peer chaincode list --installed


echo
echo "#################################################################"
echo "#######    Package EHRCC chaincode   ############################"
echo "#################################################################"
sudo docker exec cli peer chaincode package ehrccpack.out -n ehrcc -v 1.0 -p /opt/gopath/src/github.com/EHR/nodejs -l node


echo
echo "#################################################################"
echo "#######    Install EHRCC chaincode package   ####################"
echo "#################################################################"
sudo docker exec cli peer chaincode install ehrccpack.out -n ehrcc -v 1.0 -l node


echo
echo "#################################################################"
echo "#######    List all INSTALLED chaincode   #######################"
echo "#################################################################"
sudo docker exec cli peer chaincode list --installed


echo
echo "#################################################################"
echo "#######    List all INSTANTIATED chaincode   #######################"
echo "#################################################################"
sudo docker exec cli peer chaincode list --instantiated -C patientchannel


echo
echo "#################################################################"
echo "#######    Instantiate EHRCC chaincode   ########################"
echo "#################################################################"
sudo docker exec cli peer chaincode instantiate ehrccpack.out -n ehrcc -v 1.0 -l node -o orderer.patient.com:7050 -C patientchannel -c '{"Args":[]}'


echo
echo "#################################################################"
echo "#######    List all INSTANTIATED chaincode   #######################"
echo "#################################################################"
sudo docker exec cli peer chaincode list --instantiated -C patientchannel
