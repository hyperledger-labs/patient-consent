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

DATA_PROVIDERS_BP = Blueprint('data_providers')


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

