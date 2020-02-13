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

from rest_api import general

CLIENTS_BP = Blueprint('clients')


@CLIENTS_BP.get('clients')
async def get_all_clients(request):
    """Fetches complete details of all Accounts in state"""
    hospital_pkey = request.app.config.SIGNER_HOSPITAL.get_public_key().as_hex()
    # doctor_pkey = request.app.config.SIGNER_DOCTOR.get_public_key().as_hex()
    patient_pkey = request.app.config.SIGNER_PATIENT.get_public_key().as_hex()
    # lab_pkey = request.app.config.SIGNER_LAB.get_public_key().as_hex()
    # insurance_pkey = request.app.config.SIGNER_INSURANCE.get_public_key().as_hex()
    investigator_pkey = request.app.config.SIGNER_INVESTIGATOR.get_public_key().as_hex()
    clients = {'hospital': hospital_pkey, 'patient': patient_pkey, 'investigator': investigator_pkey}
    return response.json(body={'data': clients},
                         headers=general.get_response_headers())
