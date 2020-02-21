# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------
import logging

from sawtooth_rest_api.protobuf import client_state_pb2
from sawtooth_rest_api.protobuf import validator_pb2

from trial_rest_api.trial_common import helper as trial_helper
from trial_rest_api.trial_common.protobuf.trial_payload_pb2 import Investigator, Data
from trial_rest_api.consent_common import helper as consent_helper
from trial_rest_api.consent_common.protobuf.consent_payload_pb2 import Client, Permission
from trial_rest_api import messaging
from trial_rest_api.errors import ApiForbidden, ApiUnauthorized

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


async def _send(conn, timeout, batches):
    await messaging.send(conn, timeout, batches)


async def check_batch_status(conn, batch_ids):
    await messaging.check_batch_status(conn, batch_ids)


async def get_state_by_address(conn, address_suffix):
    status_request = client_state_pb2.ClientStateListRequest(address=address_suffix)
    validator_response = await conn.send(
        validator_pb2.Message.CLIENT_STATE_LIST_REQUEST,
        status_request.SerializeToString())

    status_response = client_state_pb2.ClientStateListResponse()
    status_response.ParseFromString(validator_response.content)
    # resp = status_response

    return status_response  # resp.entries


async def add_investigator(conn, timeout, batches):
    await _send(conn, timeout, batches)


# Used
async def get_investigators(inv_conn, consent_conn, client_key):
    client = await get_client(consent_conn, client_key)
    investigator_list = {}
    if Permission(type=Permission.READ_INVESTIGATOR) in client.permissions:
        list_investigator_address = trial_helper.make_investigator_list_address()
        list_investigator_resources = await messaging.get_state_by_address(inv_conn, list_investigator_address)
        for entity in list_investigator_resources.entries:
            dp = Investigator()
            dp.ParseFromString(entity.data)
            LOGGER.debug('investigator: ' + str(dp))
            investigator_list[entity.address] = dp
        return investigator_list
    elif Permission(type=Permission.READ_OWN_INVESTIGATOR) in client.permissions:
        list_investigator_address = trial_helper.make_investigator_address(client_key)
        list_investigator_resources = await messaging.get_state_by_address(inv_conn, list_investigator_address)
        for entity in list_investigator_resources.entries:
            dp = Investigator()
            dp.ParseFromString(entity.data)
            LOGGER.debug('investigator: ' + str(dp))
            investigator_list[entity.address] = dp
        return investigator_list
    raise ApiForbidden("Insufficient permission")


# Used
async def request_inform_document_consent(consent_conn, timeout, batches, client_key):
    client = await get_client(consent_conn, client_key)
    if Permission(type=Permission.REQUEST_INFORM_CONSENT) in client.permissions:
        LOGGER.debug('has permission: True')
        await _send(consent_conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


# Used
async def get_client(conn, client_key):
    client_address = consent_helper.make_client_address(client_key)
    LOGGER.debug('client_address: ' + str(client_address))
    client_resources = await messaging.get_state_by_address(conn, client_address)
    LOGGER.debug('client_resources: ' + str(client_resources))
    for entity in client_resources.entries:
        cl = Client()
        cl.ParseFromString(entity.data)
        LOGGER.debug('client: ' + str(cl))
        return cl
    raise ApiUnauthorized("No such client registered")


# Used
async def get_data_from_investigators(inv_conn, consent_conn, client_key):
    client = await get_client(consent_conn, client_key)
    data_list = {}
    if Permission(type=Permission.READ_TRIAL_DATA) in client.permissions:
        data_list_address = trial_helper.make_investigator_data_list_address()
        LOGGER.debug('has READ_DATA permission: ' + str(client_key))
        data_list_resources = await messaging.get_state_by_address(inv_conn, data_list_address)
        for entity in data_list_resources.entries:
            data = Data()
            data.ParseFromString(entity.data)
            data_list[entity.address] = data
            LOGGER.debug('data: ' + str(data))
        return data_list
    else:
        LOGGER.debug('no READ_DATA permissions')
    raise ApiForbidden("Insufficient permission")


# Used
async def import_screening_data(inv_conn, consent_conn, timeout, batches, client_key):
    client = await get_client(consent_conn, client_key)
    if Permission(type=Permission.IMPORT_TRIAL_DATA) in client.permissions:
        LOGGER.debug('has IMPORT_TRIAL_DATA permission: True')
        await _send(inv_conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


# Used
async def update_investigator(inv_conn, consent_conn, timeout, batches, client_key):
    client = await get_client(consent_conn, client_key)
    if Permission(type=Permission.UPDATE_TRIAL_DATA) in client.permissions:
        LOGGER.debug('has UPDATE_TRIAL_DATA permission: True')
        await _send(inv_conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


# Used
async def set_eligible(inv_conn, consent_conn, timeout, batches, client_key):
    client = await get_client(consent_conn, client_key)
    if Permission(type=Permission.UPDATE_TRIAL_DATA) in client.permissions:
        LOGGER.debug('has UPDATE_TRIAL_DATA permission: True')
        await _send(inv_conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")
