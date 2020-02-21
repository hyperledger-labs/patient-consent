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
from trial_rest_api import general
import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


EHRS_BP = Blueprint('ehrs')


@EHRS_BP.get('pre_screening_data')
async def get_screening_data(request):
    """Updates auth information for the authorized account"""
    inc_excl_criteria = '?'

    for criteria, value in request.raw_args.items():
        LOGGER.debug('_match_incl_excl_criteria -> criteria: ' + criteria + '; value: ' + value + ';')
        inc_excl_criteria = inc_excl_criteria + criteria + "=" + value + '&'

    res_json = general.get_response_from_ehr(request, "/ehrs/pre_screening_data" + inc_excl_criteria)
    # investigator_pkey = general.get_request_key_header(request)
    # ehr_list = await security_messaging.get_pre_screening_data(request.app.config.EHR_VAL_CONN,
    #                                                            investigator_pkey, request.raw_args)

    ehr_list_json = []
    for entity in res_json['data']:
        ehr_list_json.append({
            'id': entity['id'],
            'client_pkey': entity['client_pkey'],
            'height': entity['height'],
            'weight': entity['weight'],
            'A1C': entity['A1C'],
            'FPG': entity['FPG'],
            'OGTT': entity['OGTT'],
            'RPGT': entity['RPGT'],
            'event_time': entity['event_time'],
            'name': entity['name'],
            'surname': entity['surname']
        })

    return response.json(body={'data': ehr_list_json},
                         headers=general.get_response_headers())
