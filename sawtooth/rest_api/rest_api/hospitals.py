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
from sanic import Blueprint
from sanic import response

from rest_api.ehr_common import transaction as ehr_transaction
from rest_api.consent_common import transaction as consent_transaction
from rest_api import general, security_messaging
from rest_api.errors import ApiBadRequest, ApiInternalError

HOSPITALS_BP = Blueprint('hospitals')


@HOSPITALS_BP.get('hospitals')
async def get_all_hospitals(request):
    """Fetches complete details of all Accounts in state"""
    client_key = general.get_request_key_header(request)
    hospital_list = await security_messaging.get_hospitals(request.app.config.VAL_CONN, client_key)

    hospital_list_json = []
    for address, hp in hospital_list.items():
        hospital_list_json.append({
            'public_key': hp.public_key,
            'name': hp.name
        })
    return response.json(body={'data': hospital_list_json},
                         headers=general.get_response_headers())


@HOSPITALS_BP.post('hospitals')
async def register_hospital(request):
    """Updates auth information for the authorized account"""
    required_fields = ['name']
    general.validate_fields(required_fields, request.json)

    name = request.json.get('name')

    clinic_signer = request.app.config.SIGNER_HOSPITAL  # .get_public_key().as_hex()

    client_txn = consent_transaction.create_hospital_client(
        txn_signer=clinic_signer,
        batch_signer=clinic_signer
    )
    clinic_txn = ehr_transaction.create_hospital(
        txn_signer=clinic_signer,
        batch_signer=clinic_signer,
        name=name
    )
    batch, batch_id = ehr_transaction.make_batch_and_id([client_txn, clinic_txn], clinic_signer)

    await security_messaging.add_hospital(
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


# @HOSPITALS_BP.get('hospitals/get_shared_data/<hospital_pkey>')
# async def get_data(request, hospital_pkey):
#     """Updates auth information for the authorized account"""
#     investigator_pkey = general.get_request_key_header(request)
#     data_list = await security_messaging.get_shared_data(request.app.config.VAL_CONN,
#                                                          hospital_pkey, investigator_pkey)
#
#     data_list_json = []
#     for address, data in data_list.items():
#         data_list_json.append({
#             'id': data.id,
#             'height': data.height,
#             'weight': data.weight,
#             'A1C': data.A1C,
#             'FPG': data.FPG,
#             'OGTT': data.OGTT,
#             'RPGT': data.RPGT,
#             'event_time': data.event_time
#         })
#
#     return response.json(body={'data': data_list_json},
#                          headers=general.get_response_headers())
#
#
# @HOSPITALS_BP.get('hospitals/screening_data/<hospital_pkey>')
# async def get_data(request, hospital_pkey):
#     """Updates auth information for the authorized account"""
#     investigator_pkey = general.get_request_key_header(request)
#     data_list = await security_messaging.get_screening_data(request.app.config.VAL_CONN,
#                                                             hospital_pkey, investigator_pkey, request.raw_args)
#
#     data_list_json = []
#     for address, data in data_list.items():
#         data_list_json.append({
#             'id': data.id,
#             'height': data.height,
#             'weight': data.weight,
#             'A1C': data.A1C,
#             'FPG': data.FPG,
#             'OGTT': data.OGTT,
#             'RPGT': data.RPGT,
#             'event_time': data.event_time
#         })
#
#     return response.json(body={'data': data_list_json},
#                          headers=general.get_response_headers())


@HOSPITALS_BP.get('hospitals/grant_investigator_access/<investigator_pkey>')
async def grant_investigator_access(request, investigator_pkey):
    """Updates auth information for the authorized account"""
    hospital_key = general.get_request_key_header(request)
    client_signer = general.get_signer(request, hospital_key)
    grant_investigator_access_txn = consent_transaction.grant_investigator_access(
        txn_signer=client_signer,
        batch_signer=client_signer,
        dest_pkey=investigator_pkey)

    batch, batch_id = ehr_transaction.make_batch_and_id([grant_investigator_access_txn], client_signer)

    await security_messaging.grant_investigator_access(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        [batch], hospital_key)

    try:
        await security_messaging.check_batch_status(
            request.app.config.VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())


@HOSPITALS_BP.get('hospitals/revoke_investigator_access/<investigator_pkey>')
async def revoke_investigator_access(request, investigator_pkey):
    """Updates auth information for the authorized account"""
    hospital_key = general.get_request_key_header(request)
    client_signer = general.get_signer(request, hospital_key)
    revoke_access_to_share_data_txn = consent_transaction.revoke_investigator_access(
        txn_signer=client_signer,
        batch_signer=client_signer,
        dest_pkey=investigator_pkey)

    batch, batch_id = ehr_transaction.make_batch_and_id([revoke_access_to_share_data_txn], client_signer)

    await security_messaging.revoke_investigator_access(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        [batch], hospital_key)

    try:
        await security_messaging.check_batch_status(
            request.app.config.VAL_CONN, [batch_id])
    except (ApiBadRequest, ApiInternalError) as err:
        # await auth_query.remove_auth_entry(
        #     request.app.config.DB_CONN, request.json.get('email'))
        raise err

    return response.json(body={'status': general.DONE},
                         headers=general.get_response_headers())
