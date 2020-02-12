#!/bin/sh
#
# Copyright IBM Corp All Rights Reserved
#
# SPDX-License-Identifier: Apache-2.0
#
export PATH=$GOPATH/src/github.com/hyperledger/fabric/build/bin:${PWD}/../bin:${PWD}:$PATH
export FABRIC_CFG_PATH=${PWD}
CHANNEL_NAME=patientchannel

# remove previous crypto material and config transactions
rm -fr config/*
# rm -fr crypto-config/*

# generate crypto material
# cryptogen generate --config=./crypto-config.yaml
# if [ "$?" -ne 0 ]; then
#  echo "Failed to generate crypto material..."
#  exit 1
# fi

# generate genesis block for orderer
../../bin/configtxgen -profile PatientOrdererGenesis -outputBlock ./config/genesis.block
if [ "$?" -ne 0 ]; then
  echo "Failed to generate orderer genesis block..."
  exit 1
fi

# generate channel configuration transaction
../../bin/configtxgen -profile PatientChannel -outputCreateChannelTx ./config/patientchannel.tx -channelID $CHANNEL_NAME
if [ "$?" -ne 0 ]; then
  echo "Failed to generate channel configuration transaction..."
  exit 1
fi

# generate anchor peer transaction
#configtxgen -profile OneOrgChannel -outputAnchorPeersUpdate ./config/Org1MSPanchors.tx -channelID $CHANNEL_NAME -asOrg Org1MSP
#if [ "$?" -ne 0 ]; then
#  echo "Failed to generate anchor peer update for Org1MSP..."
#  exit 1
#fi
