#!/bin/bash
#
# Copyright IBM Corp All Rights Reserved
#
# SPDX-License-Identifier: Apache-2.0
#
# Exit on first error, print all commands.
set -ev

# don't rewrite paths for Windows Git Bash users
export MSYS_NO_PATHCONV=1

sudo docker-compose -f docker-compose.yml down

sudo docker-compose -f docker-compose.yml up -d orderer.patient.com peer0.patient.com couchdb.peer0.patient.com
sudo docker ps -a

# wait for Hyperledger Fabric to start
# incase of errors when running later commands, issue export FABRIC_START_TIMEOUT=<larger number>
export FABRIC_START_TIMEOUT=10
#echo ${FABRIC_START_TIMEOUT}
sleep ${FABRIC_START_TIMEOUT}

# Create the channel
sudo docker exec -e "CORE_PEER_LOCALMSPID=PatientMSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@patient.com/msp" peer0.patient.com peer channel create -o orderer.patient.com:7050 -c patientchannel -f /etc/hyperledger/configtx/patientchannel.tx

# Join peer0.patient.com to the channel.
sudo docker exec -e "CORE_PEER_LOCALMSPID=PatientMSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@patient.com/msp" peer0.patient.com peer channel join -b patientchannel.block

# Peer channel list
sudo docker exec -e "CORE_PEER_LOCALMSPID=PatientMSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@patient.com/msp" peer0.patient.com peer channel list


#Creating CLI Container
sudo docker-compose -f ./docker-compose.yml up -d cli

