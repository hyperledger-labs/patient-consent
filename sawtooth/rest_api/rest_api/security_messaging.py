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
# import base64

# from sawtooth_sdk.protobuf import client_batch_submit_pb2
import logging

from sawtooth_rest_api.protobuf import client_state_pb2
from sawtooth_rest_api.protobuf import validator_pb2

# from rest_api.common.protobuf import payload_pb2
from rest_api.ehr_common import helper as ehr_helper
from rest_api.ehr_common.protobuf.trial_payload_pb2 import Hospital, Patient, EHRWithUser

# from rest_api.insurance_common import helper as insurance_helper
# from rest_api.insurance_common.protobuf.insurance_payload_pb2 import Insurance, ContractWithUser
#
# from rest_api.payment_common import helper as payment_helper
# from rest_api.payment_common.protobuf.payment_payload_pb2 import Payment

from rest_api.consent_common import helper as consent_helper
from rest_api.consent_common.protobuf.consent_payload_pb2 import Client, Permission, ActionOnAccess

from rest_api import messaging
from rest_api.errors import ApiForbidden, ApiUnauthorized, ApiBadRequest

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

    # batch_status = status_response.batch_statuses[0].status
    # if batch_status == client_batch_submit_pb2.ClientBatchStatus.INVALID:
    #     invalid = status_response.batch_statuses[0].invalid_transactions[0]
    #     raise ApiBadRequest(invalid.message)
    # elif batch_status == client_batch_submit_pb2.ClientBatchStatus.PENDING:
    #     raise ApiInternalError("Transaction submitted but timed out")
    # elif batch_status == client_batch_submit_pb2.ClientBatchStatus.UNKNOWN:
    #     raise ApiInternalError("Something went wrong. Try again later")


async def add_hospital(conn, timeout, batches):
    await _send(conn, timeout, batches)


async def get_hospitals(conn, client_key):
    client = await get_client(conn, client_key)
    hospital_list = {}
    if Permission(type=Permission.READ_HOSPITAL) in client.permissions:
        list_hospital_address = ehr_helper.make_hospital_list_address()
        list_hospital_resources = await messaging.get_state_by_address(conn, list_hospital_address)
        for entity in list_hospital_resources.entries:
            hp = Hospital()
            hp.ParseFromString(entity.data)
            LOGGER.debug('hospital: ' + str(hp))
            hospital_list[entity.address] = hp
        return hospital_list
    raise ApiForbidden("Insufficient permission")


# async def add_doctor(conn, timeout, batches):
#     await _send(conn, timeout, batches)
#
#
# async def add_insurance(conn, timeout, batches):
#     await _send(conn, timeout, batches)
#
#
# async def get_doctors(conn, client_key):
#     client = await get_client(conn, client_key)
#     doctors = {}
#     if Permission(type=Permission.READ_DOCTOR) in client.permissions:
#         list_doctors_address = helper.make_doctor_list_address()
#         doctor_resources = await messaging.get_state_by_address(conn, list_doctors_address)
#         for entity in doctor_resources.entries:
#             doc = CreateDoctor()
#             doc.ParseFromString(entity.data)
#             doctors[entity.address] = doc
#         return doctors
#     raise ApiForbidden("Insufficient permission")


async def add_patient(conn, timeout, batches):
    await _send(conn, timeout, batches)


# async def get_patients(conn, client_key):
#     client = await get_client(conn, client_key)
#     if Permission(type=Permission.READ_PATIENT) in client.permissions:
#         list_patient_address = helper.make_patient_list_address()
#         return await messaging.get_state_by_address(conn, list_patient_address)
#     raise ApiForbidden("Insufficient permission")

async def get_patients(conn, client_key):
    client = await get_client(conn, client_key)
    patient_list = {}
    if Permission(type=Permission.READ_PATIENT) in client.permissions:
        list_patient_address = ehr_helper.make_patient_list_address()
        LOGGER.debug('has READ_PATIENT permission: ' + str(client_key))
        # Get Consent
        consent = await get_read_ehr_consent(conn, client_key)
        consent_list = {}
        for address, pt in consent.items():
            LOGGER.debug('consent: ' + str(pt))
            patient = await get_patient(conn, pt.patient_pkey)
            consent_list[pt.patient_pkey] = patient
        #
        patient_list_resources = await messaging.get_state_by_address(conn, list_patient_address)
        for entity in patient_list_resources.entries:
            pat = Patient()
            pat.ParseFromString(entity.data)

            patient_list[entity.address] = pat
            LOGGER.debug('patient: ' + str(pat))
        # Apply Consent
        for patient_address, pt in patient_list.items():
            LOGGER.debug('patient: ' + str(pt))
            if Permission(type=Permission.READ_OWN_PATIENT) in client.permissions and pt.public_key == client_key:
                pass
            elif pt.public_key not in consent_list:
                pat2 = Patient()
                patient_list[patient_address] = pat2
        return patient_list
    raise ApiForbidden("Insufficient permission")


# async def get_insurances(conn, client_key):
#     client = await get_client(conn, client_key)
#     insurances = {}
#     if Permission(type=Permission.READ_INSURANCE_COMPANY) in client.permissions:
#         list_insurance_address = insurance_helper.make_insurance_list_address()
#         insurance_resources = await messaging.get_state_by_address(conn, list_insurance_address)
#         for entity in insurance_resources.entries:
#             ins = Insurance()
#             ins.ParseFromString(entity.data)
#             insurances[entity.address] = ins
#         return insurances
#     raise ApiForbidden("Insufficient permission")


async def get_patient(conn, patient_key):
    list_patient_address = ehr_helper.make_patient_address(patient_key)
    patient_resources = await messaging.get_state_by_address(conn, list_patient_address)
    for entity in patient_resources.entries:
        pat = Patient()
        pat.ParseFromString(entity.data)
        return pat
    raise ApiBadRequest("No such patient exist: " + str(patient_key))


# async def add_lab(conn, timeout, batches):
#     await _send(conn, timeout, batches)
#
#
# async def add_lab_test(conn, timeout, batches, client_key):
#     client = await get_client(conn, client_key)
#     if Permission(type=Permission.WRITE_LAB_TEST) in client.permissions:
#         LOGGER.debug('has permission: True')
#         await _send(conn, timeout, batches)
#         return
#     else:
#         LOGGER.debug('has permission: False')
#     raise ApiForbidden("Insufficient permission")
#
#
# async def create_payment(conn, timeout, batches, client_key):
#     client = await get_client(conn, client_key)
#     if Permission(type=Permission.WRITE_PAYMENT) in client.permissions:
#         LOGGER.debug('has permission: True')
#         await _send(conn, timeout, batches)
#         return
#     else:
#         LOGGER.debug('has permission: False')
#     raise ApiForbidden("Insufficient permission")
#
#
# async def add_pulse(conn, timeout, batches, client_key):
#     client = await get_client(conn, client_key)
#     if Permission(type=Permission.WRITE_PULSE) in client.permissions:
#         LOGGER.debug('has permission: True')
#         await _send(conn, timeout, batches)
#         return
#     else:
#         LOGGER.debug('has permission: False')
#     raise ApiForbidden("Insufficient permission")


async def add_ehr(conn, timeout, batches, dest_pkey, src_pkey):
    client = await get_client(conn, dest_pkey)
    if Permission(type=Permission.WRITE_EHR) in client.permissions:
        LOGGER.debug('has WRITE_EHR permission: True')
        # Has consent from patient
        consent = await has_write_ehr_consent(conn, dest_pkey, src_pkey)
        if not consent:
            LOGGER.debug('no consent from patient')
            raise ApiForbidden("Insufficient permission")
        #
        await _send(conn, timeout, batches)
        return
        # LOGGER.debug('has permission: True')
        # await _send(conn, timeout, batches)
        # return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


# async def add_contract(conn, timeout, batches, client_key):
#     # LOGGER.debug('add_contract')
#     # await _send(conn, timeout, batches)
#     client = await get_client(conn, client_key)
#     if Permission(type=Permission.WRITE_CONTRACT) in client.permissions:
#         LOGGER.debug('has permission: True')
#         await _send(conn, timeout, batches)
#         return
#     else:
#         LOGGER.debug('has permission: False')
#     raise ApiForbidden("Insufficient permission")


async def revoke_read_ehr_access(conn, timeout, batches, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.REVOKE_READ_EHR_ACCESS) in client.permissions:
        LOGGER.debug('has permission: True')
        await _send(conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


async def grant_read_ehr_access(conn, timeout, batches, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.GRANT_READ_EHR_ACCESS) in client.permissions:
        LOGGER.debug('has permission: True')
        await _send(conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


async def revoke_write_ehr_access(conn, timeout, batches, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.REVOKE_WRITE_EHR_ACCESS) in client.permissions:
        LOGGER.debug('has permission: True')
        await _send(conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


async def grant_write_ehr_access(conn, timeout, batches, client_key):
    client = await get_client(conn, client_key)
    if Permission(type=Permission.GRANT_WRITE_EHR_ACCESS) in client.permissions:
        LOGGER.debug('has permission: True')
        await _send(conn, timeout, batches)
        return
    else:
        LOGGER.debug('has permission: False')
    raise ApiForbidden("Insufficient permission")


# async def get_labs(conn, client_key):
#     # client_address = consent_helper.make_client_address(client_key)
#     # LOGGER.debug('client_address: ' + str(client_address))
#     # client_resources = await messaging.get_state_by_address(conn, client_address)
#     # LOGGER.debug('client_resources: ' + str(client_resources))
#     # for entity in client_resources.entries:
#     #     cl = Client()
#     #     cl.ParseFromString(entity.data)
#     #     LOGGER.debug('client: ' + str(cl))
#     #     if Permission(type=Permission.READ_LAB) in cl.permissions:
#     #         return await messaging.get_state_by_address(conn, address_suffix)
#     client = await get_client(conn, client_key)
#     if Permission(type=Permission.READ_LAB) in client.permissions:
#         LOGGER.debug('has permission: True')
#         list_lab_address = helper.make_lab_list_address()
#         return await messaging.get_state_by_address(conn, list_lab_address)
#     else:
#         LOGGER.debug('has permission: False')
#     raise ApiForbidden("Insufficient permission")


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


async def has_read_ehr_consent(conn, dest_pkey, src_pkey):  # dest_pkey - doctor, src_pkey - patient
    consent_list = await get_read_ehr_consent(conn, dest_pkey)
    for address, data in consent_list.items():
        LOGGER.debug('consent_address: data -> ' + str(data) + '; src_key -> ' + str(src_pkey))
        if data.patient_pkey == src_pkey:
            LOGGER.debug('has consent!')
            return True
    return False


async def has_write_ehr_consent(conn, dest_pkey, src_pkey):  # dest_pkey - doctor, src_pkey - patient
    consent_list = await get_write_ehr_consent(conn, dest_pkey)
    for address, data in consent_list.items():
        LOGGER.debug('consent_address: data -> ' + str(data) + '; src_key -> ' + str(src_pkey))
        if data.patient_pkey == src_pkey:
            LOGGER.debug('has consent!')
            return True
    return False


async def get_read_ehr_consent(conn, client_key):
    consent_address = consent_helper.make_consent_read_ehr_list_address_by_destination_client(client_key)
    LOGGER.debug('consent_address: ' + str(consent_address))
    consent_resources = await messaging.get_state_by_address(conn, consent_address)
    LOGGER.debug('consent_resources: ' + str(consent_resources))
    consent_list = {}
    for entity in consent_resources.entries:
        aoa = ActionOnAccess()
        aoa.ParseFromString(entity.data)
        consent_list[entity.address] = aoa
        LOGGER.debug('consent: ' + str(aoa))
    return consent_list


async def get_write_ehr_consent(conn, client_key):
    consent_address = consent_helper.make_consent_write_ehr_list_address_by_destination_client(client_key)
    LOGGER.debug('consent_address: ' + str(consent_address))
    consent_resources = await messaging.get_state_by_address(conn, consent_address)
    LOGGER.debug('consent_resources: ' + str(consent_resources))
    consent_list = {}
    for entity in consent_resources.entries:
        aoa = ActionOnAccess()
        aoa.ParseFromString(entity.data)
        consent_list[entity.address] = aoa
        LOGGER.debug('consent: ' + str(aoa))
    return consent_list


# async def get_lab_tests(conn, client_key):
#     client = await get_client(conn, client_key)
#     lab_tests = {}
#     if Permission(type=Permission.READ_LAB_TEST) in client.permissions:
#         lab_tests_address = helper.make_lab_test_list_address()
#         LOGGER.debug('has READ_LAB_TEST permission: ' + str(client_key))
#         #
#         consent = await get_consent(conn, client_key)
#         patient_list = {}
#         for address, pt in consent.items():
#             LOGGER.debug('patient consent: ' + str(pt))
#             patient = await get_patient(conn, pt.patient_pkey)
#             patient_list[pt.patient_pkey] = patient
#         #
#         lab_test_resources = await messaging.get_state_by_address(conn, lab_tests_address)
#         for entity in lab_test_resources.entries:
#             lt = AddLabTestWithUser()
#             lt.ParseFromString(entity.data)
#             lab_tests[entity.address] = lt
#             LOGGER.debug('lab_test: ' + str(lt))
#         for patient_address, pt in patient_list.items():
#             LOGGER.debug('patient: ' + str(pt))
#             for pulse_address, lt in lab_tests.items():
#                 LOGGER.debug('lab_test: ' + str(lt))
#                 if patient_address == lt.client_pkey:
#                     LOGGER.debug('match!')
#                     pt_local = patient_list[patient_address]
#                     lt.name = pt_local.name
#                     lt.surname = pt_local.surname
#                     lab_tests[pulse_address] = lt
#         return lab_tests
#     elif Permission(type=Permission.READ_OWN_LAB_TEST) in client.permissions:
#         lab_test_ids_address = helper.make_lab_test_list_by_patient_address(client_key)
#         LOGGER.debug('has READ_OWN_LAB_TEST permission: ' + str(lab_test_ids_address))
#         lab_test_ids = await messaging.get_state_by_address(conn, lab_test_ids_address)
#         for entity in lab_test_ids.entries:
#             lab_test_id = entity.data.decode()
#             lab_test_address = helper.make_lab_test_address(lab_test_id)
#             LOGGER.debug('get lab test: ' + str(lab_test_address))
#             lab_test_resources = await messaging.get_state_by_address(conn, lab_test_address)
#             for entity2 in lab_test_resources.entries:
#                 LOGGER.debug('get lab test entity2: ' + str(entity2.address))
#                 lt = AddLabTestWithUser()
#                 lt.ParseFromString(entity2.data)
#                 lab_tests[entity2.address] = lt
#         return lab_tests
#     else:
#         LOGGER.debug('neither READ_OWN_LAB_TEST nor READ_LAB_TEST permissions')
#     raise ApiForbidden("Insufficient permission")
#
#
# async def get_pulse_list(conn, client_key):
#     client = await get_client(conn, client_key)
#     pulse_list = {}
#     if Permission(type=Permission.READ_PULSE) in client.permissions:
#         pulse_list_address = helper.make_pulse_list_address()
#         LOGGER.debug('has READ_PULSE permission: ' + str(client_key))
#         consent = await get_consent(conn, client_key)
#         patient_list = {}
#         for address, pt in consent.items():
#             LOGGER.debug('patient consent: ' + str(pt))
#             patient = await get_patient(conn, pt.patient_pkey)
#             patient_list[pt.patient_pkey] = patient
#         pulse_list_resources = await messaging.get_state_by_address(conn, pulse_list_address)
#         for entity in pulse_list_resources.entries:
#             pl = AddPulseWithUser()
#             pl.ParseFromString(entity.data)
#             pulse_list[entity.address] = pl
#             LOGGER.debug('pulse: ' + str(pl))
#         for patient_address, pt in patient_list.items():
#             LOGGER.debug('patient: ' + str(pt))
#             for pulse_address, pl in pulse_list.items():
#                 LOGGER.debug('pulse: ' + str(pl))
#                 if patient_address == pl.client_pkey:
#                     LOGGER.debug('match!')
#                     pt_local = patient_list[patient_address]
#                     pl.name = pt_local.name
#                     pl.surname = pt_local.surname
#                     pulse_list[pulse_address] = pl
#         return pulse_list
#     elif Permission(type=Permission.READ_OWN_PULSE) in client.permissions:
#         pulse_list_ids_address = helper.make_pulse_list_by_patient_address(client_key)
#         LOGGER.debug('has READ_OWN_PULSE permission: ' + str(pulse_list_ids_address))
#         pulse_list_ids = await messaging.get_state_by_address(conn, pulse_list_ids_address)
#         for entity in pulse_list_ids.entries:
#             pulse_id = entity.data.decode()
#             pulse_address = helper.make_pulse_address(pulse_id)
#             LOGGER.debug('get pulse: ' + str(pulse_address))
#             pulse_resources = await messaging.get_state_by_address(conn, pulse_address)
#             for entity2 in pulse_resources.entries:
#                 LOGGER.debug('get pulse entity2: ' + str(entity2.address))
#                 pl = AddPulseWithUser()
#                 pl.ParseFromString(entity2.data)
#                 pulse_list[entity2.address] = pl
#         return pulse_list
#     else:
#         LOGGER.debug('neither READ_OWN_PULSE nor READ_PULSE permissions')
#     raise ApiForbidden("Insufficient permission")
#
#
# async def close_claim(conn, timeout, batches, dest_pkey, src_pkey):
#     client = await get_client(conn, dest_pkey)
#     if Permission(type=Permission.READ_CLAIM) in client.permissions \
#             and Permission(type=Permission.CLOSE_CLAIM) in client.permissions:
#         LOGGER.debug('has READ_CLAIM and CLOSE_CLAIM permission: True')
#         # Has consent from patient
#         consent = await has_consent(conn, dest_pkey, src_pkey)
#         if not consent:
#             LOGGER.debug('no consent from patient')
#             raise ApiForbidden("Insufficient permission")
#         #
#         await _send(conn, timeout, batches)
#         return
#     else:
#         LOGGER.debug('has permission: False')
#     raise ApiForbidden("Insufficient permission")
#
#
# async def update_claim(conn, timeout, batches, dest_pkey, src_pkey):
#     client = await get_client(conn, dest_pkey)
#     if Permission(type=Permission.READ_CLAIM) in client.permissions \
#             and Permission(type=Permission.UPDATE_CLAIM) in client.permissions:
#         LOGGER.debug('has READ_CLAIM and UPDATE_CLAIM permission: True')
#         # Has consent from patient
#         consent = await has_consent(conn, dest_pkey, src_pkey)
#         if not consent:
#             LOGGER.debug('no consent from patient')
#             raise ApiForbidden("Insufficient permission")
#         #
#         await _send(conn, timeout, batches)
#         return
#     else:
#         LOGGER.debug('has permission: False')
#     raise ApiForbidden("Insufficient permission")
#
#
# async def get_claim(claim_id, doctor_pkey):
#     claim_list = await get_claims(claim_id, doctor_pkey)
#     for claim in claim_list:
#         if claim.id == claim_id:
#             return claim
#     return None


async def get_ehrs(conn, client_key):
    client = await get_client(conn, client_key)
    ehr_list = {}
    if Permission(type=Permission.READ_EHR) in client.permissions:
        ehr_list_address = ehr_helper.make_ehr_list_address()
        LOGGER.debug('has READ_EHR permission: ' + str(client_key))
        # Get Consent
        consent = await get_read_ehr_consent(conn, client_key)
        patient_list = {}
        for address, pt in consent.items():
            LOGGER.debug('patient consent: ' + str(pt))
            patient = await get_patient(conn, pt.patient_pkey)
            patient_list[pt.patient_pkey] = patient
        #
        ehr_list_resources = await messaging.get_state_by_address(conn, ehr_list_address)
        for entity in ehr_list_resources.entries:
            cl = EHRWithUser()
            cl.ParseFromString(entity.data)

            ehr_list[entity.address] = cl
            LOGGER.debug('ehr: ' + str(cl))
        # Apply Consent
        for patient_address, pt in patient_list.items():
            LOGGER.debug('patient: ' + str(pt))
            for claim_address, e in ehr_list.items():
                LOGGER.debug('ehr: ' + str(e))
                if patient_address == e.client_pkey:
                    LOGGER.debug('match!')
                    pt_local = patient_list[patient_address]
                    e.name = pt_local.name
                    e.surname = pt_local.surname
                    ehr_list[claim_address] = e
        return ehr_list
    elif Permission(type=Permission.READ_OWN_EHR) in client.permissions:
        ehr_list_ids_address = ehr_helper.make_ehr_list_by_patient_address(client_key)
        LOGGER.debug('has READ_OWN_EHR permission: ' + str(ehr_list_ids_address))
        ehr_list_ids = await messaging.get_state_by_address(conn, ehr_list_ids_address)
        for entity in ehr_list_ids.entries:
            ehr_id = entity.data.decode()
            ehr_address = ehr_helper.make_ehr_address(ehr_id)
            LOGGER.debug('get ehr: ' + str(ehr_address))
            ehr_resources = await messaging.get_state_by_address(conn, ehr_address)
            for entity2 in ehr_resources.entries:
                LOGGER.debug('get ehr entity2: ' + str(entity2.address))
                e = EHRWithUser()
                e.ParseFromString(entity2.data)
                ehr_list[entity2.address] = e
        return ehr_list
    else:
        LOGGER.debug('neither READ_OWN_EHR nor READ_EHR permissions')
    raise ApiForbidden("Insufficient permission")


# async def valid_contracts(conn, client_key, contract_id):
#     contract_list = await get_contracts(conn, client_key)
#     for address, con in contract_list.items():
#         if con.id == contract_id:
#             return True
#     return False
#
#
# async def get_contracts(conn, client_key):
#     client = await get_client(conn, client_key)
#     contract_list = {}
#     if Permission(type=Permission.READ_CONTRACT) in client.permissions:
#         contract_list_address = insurance_helper.make_contract_list_address()
#         LOGGER.debug('has READ_CONTRACT permission: ' + str(client_key))
#         contract_list_ids = await messaging.get_state_by_address(conn, contract_list_address)
#         for entity in contract_list_ids.entries:
#             con = ContractWithUser()
#             con.ParseFromString(entity.data)
#             contract_list[entity.address] = con
#             LOGGER.debug('contract: ' + str(con))
#         return contract_list
#     elif Permission(type=Permission.READ_OWN_CONTRACT) in client.permissions:
#         # As Insurance
#         contract_list_ids_address = insurance_helper.make_contract_list_by_insurance_address(client_key)
#         LOGGER.debug('has READ_OWN_CONTRACT permission: ' + str(contract_list_ids_address))
#         contract_list_ids = await messaging.get_state_by_address(conn, contract_list_ids_address)
#         for entity in contract_list_ids.entries:
#             contract_id = entity.data.decode()
#             contract_address = insurance_helper.make_contract_address(contract_id)
#             LOGGER.debug('get contract: ' + str(contract_address))
#             contract_resources = await messaging.get_state_by_address(conn, contract_address)
#             for entity2 in contract_resources.entries:
#                 LOGGER.debug('get contract entity2: ' + str(entity2.address))
#                 con = ContractWithUser()
#                 con.ParseFromString(entity2.data)
#                 contract_list[entity2.address] = con
#         # As Patient
#         contract_list_ids2_address = insurance_helper.make_contract_list_by_patient_address(client_key)
#         LOGGER.debug('has READ_OWN_CONTRACT permission (as patient): ' + str(contract_list_ids2_address))
#         contract_list_ids2 = await messaging.get_state_by_address(conn, contract_list_ids2_address)
#         for entity in contract_list_ids2.entries:
#             contract_id = entity.data.decode()
#             contract_address = insurance_helper.make_contract_address(contract_id)
#             LOGGER.debug('get contract: ' + str(contract_address))
#             contract_resources = await messaging.get_state_by_address(conn, contract_address)
#             for entity2 in contract_resources.entries:
#                 LOGGER.debug('get contract entity2: ' + str(entity2.address))
#                 con = ContractWithUser()
#                 con.ParseFromString(entity2.data)
#                 contract_list[entity2.address] = con
#         return contract_list
#     else:
#         LOGGER.debug('neither READ_CONTRACT or READ_OWN_CONTRACT permissions')
#     raise ApiForbidden("Insufficient permission")
#
#
# async def get_payments(conn, client_key):
#     client = await get_client(conn, client_key)
#     payment_list = {}
#     if Permission(type=Permission.READ_PAYMENT) in client.permissions:
#         payment_list_address = payment_helper.make_payment_list_address()
#         LOGGER.debug('has READ_PAYMENT permission: ' + str(client_key))
#         payment_resources_ids = await messaging.get_state_by_address(conn, payment_list_address)
#         for entity in payment_resources_ids.entries:
#             LOGGER.debug('get payment entity: ' + str(entity.address))
#             pay = Payment()
#             pay.ParseFromString(entity.data)
#             payment_list[entity.address] = pay
#             LOGGER.debug('payment: ' + str(pay))
#         return payment_list
#     elif Permission(type=Permission.READ_OWN_PAYMENT) in client.permissions:
#         # As Patient
#         payment_list_ids_address = payment_helper.make_payment_list_by_patient_address(client_key)
#         LOGGER.debug('has READ_OWN_PAYMENT permission: ' + str(payment_list_ids_address))
#         payment_list_ids = await messaging.get_state_by_address(conn, payment_list_ids_address)
#         for entity in payment_list_ids.entries:
#             payment_id = entity.data.decode()
#             payment_address = payment_helper.make_payment_address(payment_id)
#             LOGGER.debug('get payment entity: ' + str(payment_address))
#             payment_resources = await messaging.get_state_by_address(conn, payment_address)
#             for entity2 in payment_resources.entries:
#                 LOGGER.debug('get payment entity2: ' + str(entity2.address))
#                 pay = Payment()
#                 pay.ParseFromString(entity2.data)
#                 if pay.contract_id is not None and pay.contract_id != '':
#                     timestamp = pay.timestamp
#                     pay = Payment()
#                     pay.timestamp = timestamp
#                 payment_list[entity2.address] = pay
#
#         return payment_list
#     else:
#         LOGGER.debug('neither READ_PAYMENT or READ_OWN_PAYMENT permissions')
#     raise ApiForbidden("Insufficient permission")
