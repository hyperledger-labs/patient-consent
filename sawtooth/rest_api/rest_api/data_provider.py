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

from sanic import Blueprint
from sanic import response

from rest_api.ehr_common import transaction as ehr_transaction
from rest_api.consent_common import transaction as consent_transaction
from rest_api import general, security_messaging
from rest_api.errors import ApiBadRequest, ApiInternalError

DATA_PROVIDERS_BP = Blueprint('data_providers')

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


@DATA_PROVIDERS_BP.get('data_providers')
async def get_all_data_providers(request):
    """Fetches complete details of all Accounts in state"""
    client_key = general.get_request_key_header(request)
    data_provider_list = await security_messaging.get_data_providers(request.app.config.VAL_CONN, client_key)

    data_provider_list_json = []
    for address, dp in data_provider_list.items():
        data_provider_list_json.append({
            'public_key': dp.public_key,
            'name': dp.name
        })
    return response.json(body={'data': data_provider_list_json},
                         headers=general.get_response_headers())


@DATA_PROVIDERS_BP.post('data_providers')
async def register_data_provider(request):
    """Updates auth information for the authorized account"""
    required_fields = ['name']
    general.validate_fields(required_fields, request.json)

    name = request.json.get('name')

    clinic_signer = request.app.config.SIGNER_DATAPROVIDER  # .get_public_key().as_hex()

    client_txn = consent_transaction.create_data_provider_client(
        txn_signer=clinic_signer,
        batch_signer=clinic_signer
    )
    clinic_txn = ehr_transaction.create_data_provider(
        txn_signer=clinic_signer,
        batch_signer=clinic_signer,
        name=name
    )
    batch, batch_id = ehr_transaction.make_batch_and_id([client_txn, clinic_txn], clinic_signer)

    await security_messaging.add_data_provider(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        [batch])

    try:
        await security_messaging.check_batch_status(
            request.app.config.VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())


@DATA_PROVIDERS_BP.post('data_providers/import_screening_data')
async def import_screening_data(request):
    """Updates auth information for the authorized account"""
    data_provider_key = general.get_request_key_header(request)
    client_signer = general.get_signer(request, data_provider_key)
    LOGGER.debug('request.json: ' + str(request.json))
    data_list = request.json
    data_txns = []
    for data in data_list:
        data_txn = ehr_transaction.add_data(
            txn_signer=client_signer,
            batch_signer=client_signer,
            uid=data['id'],
            height=data['height'],
            weight=data['weight'],
            a1c=data['A1C'],
            fpg=data['FPG'],
            ogtt=data['OGTT'],
            rpgt=data['RPGT'],
            event_time=data['event_time'])
        data_txns.append(data_txn)

    batch, batch_id = ehr_transaction.make_batch_and_id(data_txns, client_signer)

    await security_messaging.import_screening_data(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        [batch], data_provider_key)

    try:
        await security_messaging.check_batch_status(
            request.app.config.VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())


@DATA_PROVIDERS_BP.get('data_providers/data')
async def get_all_data_from_data_providers(request):
    """Fetches complete details of all Accounts in state"""
    client_key = general.get_request_key_header(request)
    data_list = await security_messaging.get_data_from_data_providers(request.app.config.VAL_CONN, client_key)

    data_list_json = []
    for address, data in data_list.items():
        data_list_json.append({
            'id': data.id,
            'height': data.height,
            'weight': data.weight,
            'A1C': data.A1C,
            'FPG': data.FPG,
            'OGTT': data.OGTT,
            'RPGT': data.RPGT,
            'event_time': data.event_time
        })
    return response.json(body={'data': data_list_json},
                         headers=general.get_response_headers())


@DATA_PROVIDERS_BP.post('data_providers/data/update')
async def update_data(request):
    client_key = general.get_request_key_header(request)
    required_fields = ['id', 'height', 'weight', 'A1C', 'FPG', 'OGTT', 'RPGT']
    general.validate_fields(required_fields, request.json)

    uid = request.json.get('id')
    height = request.json.get('height')
    weight = request.json.get('weight')
    A1C = request.json.get('A1C')
    FPG = request.json.get('FPG')
    OGTT = request.json.get('OGTT')
    RPGT = request.json.get('RPGT')

    client_signer = request.app.config.SIGNER_DATAPROVIDER  # .get_public_key().as_hex()

    client_txn = ehr_transaction.update_data(
        txn_signer=client_signer,
        batch_signer=client_signer,
        uid=uid,
        height=height,
        weight=weight,
        a1c=A1C,
        fpg=FPG,
        ogtt=OGTT,
        rpgt=RPGT)

    batch, batch_id = ehr_transaction.make_batch_and_id([client_txn], client_signer)

    await security_messaging.update_data_provider(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        [batch], client_key)

    try:
        await security_messaging.check_batch_status(
            request.app.config.VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())
