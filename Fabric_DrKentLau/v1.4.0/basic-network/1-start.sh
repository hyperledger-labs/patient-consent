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
#  start.sh

sudo docker-compose -f docker-compose.yml down

echo
echo "#################################################################"
echo "#######    Starting network:  ca.patient.com              #######"
echo "#######                       orderer.patient.com         #######"
echo "#######                       peer0.patient.com           #######"
echo "#######                       couchdb.peer0.patient.com   #######"
echo "#################################################################"

sudo docker-compose -f docker-compose.yml up -d ca.patient.com orderer.patient.com peer0.patient.com couchdb

echo
echo "#################################################################"
echo "#######    List of all network containers   #####################"
echo "#################################################################"

sudo docker ps -a

# wait for Hyperledger Fabric to start
# incase of errors when running later commands, issue export FABRIC_START_TIMEOUT=<larger number>
export FABRIC_START_TIMEOUT=10
#echo ${FABRIC_START_TIMEOUT}
sleep ${FABRIC_START_TIMEOUT}


echo
echo "#################################################################"
echo "#######    Creating patientchannel   ############################"
echo "#################################################################"

# Create the channel
sudo docker exec -e "CORE_PEER_LOCALMSPID=PatientMSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@patient.com/msp" peer0.patient.com peer channel create -o orderer.patient.com:7050 -c patientchannel -f /etc/hyperledger/configtx/patientchannel.tx

echo
echo "#################################################################"
echo "#######    Joining peer0.patient.com to patientchannel   ########"
echo "#################################################################"

# Join peer0.patient.com to the channel.
sudo docker exec -e "CORE_PEER_LOCALMSPID=PatientMSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@patient.com/msp" peer0.patient.com peer channel join -b patientchannel.block


echo
echo "#################################################################"
echo "#######    List of all channels joined by peer0.patient.com   ###"
echo "#################################################################"

# Peer channel list
sudo docker exec -e "CORE_PEER_LOCALMSPID=PatientMSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@patient.com/msp" peer0.patient.com peer channel list

echo
echo "#################################################################"
echo "#######    Starting network:  cli   #############################"
echo "#################################################################"

#Creating CLI Container
sudo docker-compose -f ./docker-compose.yml up -d cli
