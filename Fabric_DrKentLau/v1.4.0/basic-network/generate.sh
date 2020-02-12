#!/bin/sh
#
# Copyright IBM Corp All Rights Reserved
#
# SPDX-License-Identifier: Apache-2.0
#
export PATH=$GOPATH/src/github.com/hyperledger/fabric/build/bin:${PWD}/../bin:${PWD}:$PATH
export FABRIC_CFG_PATH=${PWD}
CHANNEL_NAME=patientchannel


###########################################################
#                                                         #
# remove previous crypto material and config transactions #
#                                                         #
###########################################################

rm -fr config/*
# rm -fr crypto-config/*


############################
#                          #
# generate crypto material #
#                          #
############################

# cryptogen generate --config=./crypto-config.yaml
# if [ "$?" -ne 0 ]; then
#  echo "Failed to generate crypto material..."
#  exit 1
# fi


################################################################
#                                                              #
# The next steps will replace the template's contents with the #
# actual values of the private key file names for the two CAs. #
#                                                              #
################################################################

# CURRENT_DIR=$PWD
# cd crypto-config/peerOrganizations/org1.example.com/ca/
# PRIV_KEY=$(ls *_sk)
# cd "$CURRENT_DIR"
# sed $OPTS "s/CA1_PRIVATE_KEY/${PRIV_KEY}/g" docker-compose-e2e.yaml
# cd crypto-config/peerOrganizations/org2.example.com/ca/
# PRIV_KEY=$(ls *_sk)
# cd "$CURRENT_DIR"
# sed $OPTS "s/CA2_PRIVATE_KEY/${PRIV_KEY}/g" docker-compose-e2e.yaml
#
# # generate genesis block for orderer
# ../../bin/configtxgen -profile PatientOrdererGenesis -outputBlock ./config/genesis.block
# if [ "$?" -ne 0 ]; then
#   echo "Failed to generate orderer genesis block..."
#   exit 1
# fi


# echo "##########################################################"
# echo "#########  Generating Orderer Genesis block ##############"
# echo "##########################################################"
# # Note: For some unknown reason (at least for now) the block file can't be
# # named orderer.genesis.block or the orderer will fail to launch!
# echo "CONSENSUS_TYPE="$CONSENSUS_TYPE
# set -x
# if [ "$CONSENSUS_TYPE" == "solo" ]; then
#   configtxgen -profile TwoOrgsOrdererGenesis -channelID byfn-sys-channel -outputBlock ./channel-artifacts/genesis.block
# elif [ "$CONSENSUS_TYPE" == "kafka" ]; then
#   configtxgen -profile SampleDevModeKafka -channelID byfn-sys-channel -outputBlock ./channel-artifacts/genesis.block
# else
#   set +x
#   echo "unrecognized CONSESUS_TYPE='$CONSENSUS_TYPE'. exiting"
#   exit 1
# fi
# res=$?
# set +x
# if [ $res -ne 0 ]; then
#   echo "Failed to generate orderer genesis block..."
#   exit 1
# fi

##############################################
#                                            #
# generate channel configuration transaction #
#                                            #
##############################################

echo
echo "#################################################################"
echo "### Generating channel configuration transaction 'channel.tx' ###"
echo "#################################################################"

../../bin/configtxgen -profile PatientChannel -outputCreateChannelTx ./config/patientchannel.tx -channelID $CHANNEL_NAME
if [ "$?" -ne 0 ]; then
  echo "Failed to generate channel configuration transaction..."
  exit 1
fi


####################################
#                                  #
# generate anchor peer transaction #
#                                  #
####################################

#configtxgen -profile OneOrgChannel -outputAnchorPeersUpdate ./config/Org1MSPanchors.tx -channelID $CHANNEL_NAME -asOrg Org1MSP
#if [ "$?" -ne 0 ]; then
#  echo "Failed to generate anchor peer update for Org1MSP..."
#  exit 1
#fi
