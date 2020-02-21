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

from trial_rest_api.trial_common import transaction as trial_transaction
from trial_rest_api.consent_common import transaction as consent_transaction
from trial_rest_api import general, security_messaging
from trial_rest_api.errors import ApiBadRequest, ApiInternalError

INVESTIGATORS_BP = Blueprint('investigators')

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


# Used
@INVESTIGATORS_BP.get('investigators')
async def get_all_investigators(request):
    """Fetches complete details of all Accounts in state"""
    client_key = general.get_request_key_header(request)
    investigator_list = await security_messaging.get_investigators(request.app.config.INVESTIGATOR_VAL_CONN,
                                                                   request.app.config.CONSENT_VAL_CONN, client_key)

    investigator_list_json = []
    for address, dp in investigator_list.items():
        investigator_list_json.append({
            'public_key': dp.public_key,
            'name': dp.name
        })
    return response.json(body={'data': investigator_list_json},
                         headers=general.get_response_headers())


# Used
@INVESTIGATORS_BP.post('investigators')
async def register_investigator(request):
    """Updates auth information for the authorized account"""
    required_fields = ['name']
    general.validate_fields(required_fields, request.json)

    name = request.json.get('name')

    clinic_signer = request.app.config.SIGNER_INVESTIGATOR  # .get_public_key().as_hex()

    # Consent network

    client_txn = consent_transaction.create_investigator_client(
        txn_signer=clinic_signer,
        batch_signer=clinic_signer
    )

    batch, batch_id = consent_transaction.make_batch_and_id([client_txn], clinic_signer)

    await security_messaging.add_investigator(
        request.app.config.CONSENT_VAL_CONN,
        request.app.config.TIMEOUT,
        [batch])

    try:
        await security_messaging.check_batch_status(
            request.app.config.CONSENT_VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    # Trial network

    clinic_txn = trial_transaction.create_investigator(
        txn_signer=clinic_signer,
        batch_signer=clinic_signer,
        name=name
    )
    batch, batch_id = trial_transaction.make_batch_and_id([clinic_txn], clinic_signer)

    await security_messaging.add_investigator(
        request.app.config.INVESTIGATOR_VAL_CONN,
        request.app.config.TIMEOUT,
        [batch])

    try:
        await security_messaging.check_batch_status(
            request.app.config.INVESTIGATOR_VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())


# Used
@INVESTIGATORS_BP.get('investigators/import_to_trial_data/<patient_pkey>/<ehr_id>')
async def import_screening_data(request, patient_pkey, ehr_id):
    """Updates auth information for the authorized account"""
    res_json = general.get_response_from_ehr(request, "/ehrs/" + patient_pkey + "/" + ehr_id)
    investigator_pkey = general.get_request_key_header(request)
    client_signer = general.get_signer(request, investigator_pkey)
    data_json = res_json['data']

    if not data_json:
        raise ApiBadRequest("Can not retrieve '" + ehr_id + "' EHR ' for '" + patient_pkey + "' patient")

    data_txn = trial_transaction.add_data(
        txn_signer=client_signer,
        batch_signer=client_signer,
        uid=data_json['id'],
        height=data_json['height'],
        weight=data_json['weight'],
        a1c=data_json['A1C'],
        fpg=data_json['FPG'],
        ogtt=data_json['OGTT'],
        rpgt=data_json['RPGT'],
        event_time=data_json['event_time'])

    batch, batch_id = trial_transaction.make_batch_and_id([data_txn], client_signer)

    await security_messaging.import_screening_data(
        request.app.config.INVESTIGATOR_VAL_CONN,
        request.app.config.CONSENT_VAL_CONN,
        request.app.config.TIMEOUT,
        [batch], investigator_pkey)

    try:
        await security_messaging.check_batch_status(
            request.app.config.INVESTIGATOR_VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())


# Used
@INVESTIGATORS_BP.get('investigators/data')
async def get_all_data_from_investigators(request):
    """Fetches complete details of all Accounts in state"""
    client_key = general.get_request_key_header(request)
    data_list = await security_messaging.get_data_from_investigators(request.app.config.INVESTIGATOR_VAL_CONN,
                                                                     request.app.config.CONSENT_VAL_CONN, client_key)

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
            'event_time': data.event_time,
            'eligible': data.eligible
        })
    return response.json(body={'data': data_list_json},
                         headers=general.get_response_headers())


# Used
@INVESTIGATORS_BP.post('investigators/data/update')
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

    client_signer = request.app.config.SIGNER_INVESTIGATOR  # .get_public_key().as_hex()

    client_txn = trial_transaction.update_data(
        txn_signer=client_signer,
        batch_signer=client_signer,
        uid=uid,
        height=height,
        weight=weight,
        a1c=A1C,
        fpg=FPG,
        ogtt=OGTT,
        rpgt=RPGT)

    batch, batch_id = trial_transaction.make_batch_and_id([client_txn], client_signer)

    await security_messaging.update_investigator(
        request.app.config.INVESTIGATOR_VAL_CONN,
        request.app.config.CONSENT_VAL_CONN,
        request.app.config.TIMEOUT,
        [batch], client_key)

    try:
        await security_messaging.check_batch_status(
            request.app.config.INVESTIGATOR_VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())


# Used
@INVESTIGATORS_BP.get('investigators/request_inform_consent/<patient_pkey>')
async def request_inform_consent(request, patient_pkey):
    """Updates auth information for the authorized account"""
    client_key = general.get_request_key_header(request)
    client_signer = general.get_signer(request, client_key)
    grant_read_ehr_permission_txn = consent_transaction.request_inform_document_consent(
        txn_signer=client_signer,
        batch_signer=client_signer,
        patient_pkey=patient_pkey)

    batch, batch_id = trial_transaction.make_batch_and_id([grant_read_ehr_permission_txn], client_signer)

    await security_messaging.request_inform_document_consent(
        request.app.config.CONSENT_VAL_CONN,
        request.app.config.TIMEOUT,
        [batch], client_key)

    try:
        await security_messaging.check_batch_status(
            request.app.config.CONSENT_VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())


# Used
@INVESTIGATORS_BP.post('investigators/data/eligible')
async def set_eligible(request):
    client_key = general.get_request_key_header(request)
    required_fields = ['id', 'eligible']
    general.validate_fields(required_fields, request.json)

    uid = request.json.get('id')
    eligible = bool(request.json.get('eligible'))

    client_signer = request.app.config.SIGNER_INVESTIGATOR  # .get_public_key().as_hex()

    client_txn = trial_transaction.set_eligible(
        txn_signer=client_signer,
        batch_signer=client_signer,
        uid=uid,
        eligible=eligible)

    batch, batch_id = trial_transaction.make_batch_and_id([client_txn], client_signer)

    await security_messaging.set_eligible(
        request.app.config.INVESTIGATOR_VAL_CONN,
        request.app.config.CONSENT_VAL_CONN,
        request.app.config.TIMEOUT,
        [batch], client_key)

    try:
        await security_messaging.check_batch_status(
            request.app.config.INVESTIGATOR_VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())
