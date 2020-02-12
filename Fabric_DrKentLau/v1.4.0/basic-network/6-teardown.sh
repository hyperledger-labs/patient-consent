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
#  teardown.sh

# Exit on first error, print all commands.
set -e

# Shut down the Docker containers for the system tests.
docker-compose -f docker-compose.yml kill && docker-compose -f docker-compose.yml down

# remove the local state
rm -f ~/.hfc-key-store/*

# remove chaincode docker images
docker rm $(docker ps -aq)
docker rmi $(docker images dev-* -q)

# Your system is now clean
