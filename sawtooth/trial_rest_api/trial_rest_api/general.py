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
import getpass
import os
import requests as req
from sawtooth_signing import ParseError
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from trial_rest_api.trial_common.exceptions import TrialException
from trial_rest_api.errors import ApiBadRequest, ApiForbidden
import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


DONE = 'DONE'


def get_response_headers():
    return {
        # 'Access-Control-Allow-Credentials': True,
        # 'Access-Control-Allow-Origin': origin,
        'Connection': 'keep-alive'}


def get_response_from_ehr(request, uri):
    client_key = get_request_key_header(request)
    url = request.app.config.EHR_BACKEND_URL + uri
    LOGGER.debug('Request started: ' + str(url))
    res = req.get(request.app.config.EHR_BACKEND_URL + uri, headers={'ClientKey': client_key})
    LOGGER.debug('Request finished: ' + str(url))
    try:
        res.raise_for_status()
    except Exception as e:
        raise TrialException('get_response_from_ehr failed: {}'.format(str(e)))
    res_content = res.content
    res_json = res.json()
    LOGGER.debug('res_content: ' + str(res_content))
    LOGGER.debug('res_json: ' + str(res_json))
    return res_json


def get_request_key_header(request):
    if 'ClientKey' not in request.headers:
        raise ApiForbidden('Client key not specified')
    return request.headers['ClientKey']


def validate_fields(required_fields, request_json):
    try:
        for field in required_fields:
            if request_json.get(field) is None:
                raise ApiBadRequest("{} is required".format(field))
    except (ValueError, AttributeError):
        raise ApiBadRequest("Improper JSON format")


def get_keyfile(user):
    username = getpass.getuser() if user is None else user
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")

    return '{}/{}.priv'.format(key_dir, username)


def get_signer_from_file(keyfile):
    try:
        with open(keyfile) as fd:
            private_key_str = fd.read().strip()
    except OSError as err:
        raise TrialException(
            'Failed to read private key {}: {}'.format(
                keyfile, str(err)))

    try:
        private_key = Secp256k1PrivateKey.from_hex(private_key_str)
    except ParseError as e:
        raise TrialException(
            'Unable to load private key: {}'.format(str(e)))

    return private_key


def get_signer(request, client_key):
    if request.app.config.SIGNER_INVESTIGATOR.get_public_key().as_hex() == client_key:
        client_signer = request.app.config.SIGNER_INVESTIGATOR
    else:
        raise TrialException(
            'Unable to load private key for client_key: {}'.format(str(client_key)))
    return client_signer
