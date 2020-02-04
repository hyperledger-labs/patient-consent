import hashlib
import time

DISTRIBUTION_NAME = 'patient-consen'

DEFAULT_URL = 'http://127.0.0.1:8008'

TP_FAMILYNAME = 'ehr'
TP_VERSION = '1.0'
# CLINIC_ENTITY_NAME = 'clinic'
# DOCTOR_ENTITY_NAME = 'doctor'
# PATIENT_ENTITY_NAME = 'patient'
# CLAIM_ENTITY_NAME = 'claim'
# EVENT_ENTITY_NAME = 'event'
# LAB_TEST_ENTITY_NAME = 'lab_test'
# PULSE_ENTITY_NAME = 'pulse'
#
# CLAIM_ENTITY_HEX6 = hashlib.sha512(CLAIM_ENTITY_NAME.encode("utf-8")).hexdigest()[0:6]
# CLINIC_ENTITY_HEX64 = hashlib.sha512(CLINIC_ENTITY_NAME.encode("utf-8")).hexdigest()[0:64]

HOSPITAL_ENTITY_CODE = '01'
# DOCTOR_ENTITY_CODE = '02'
PATIENT_ENTITY_CODE = '03'
EHR_ENTITY_CODE = '04'
INVESTIGATOR_ENTITY_CODE = '05'
INVESTIGATOR_DATA_ENTITY_CODE = '06'

PATIENT_EHR__RELATION_CODE = "71"
EHR_PATIENT__RELATION_CODE = "72"

HOSPITAL_EHR__RELATION_CODE = "81"
EHR_HOSPITAL__RELATION_CODE = "82"

INVESTIGATOR_DATA__RELATION_CODE = "91"
DATA_INVESTIGATOR__RELATION_CODE = "92"


def _hash(identifier):
    return hashlib.sha512(identifier.encode('utf-8')).hexdigest()


TP_PREFFIX_HEX6 = _hash(TP_FAMILYNAME)[0:6]


def make_hospital_address(hospital_pkey):
    return TP_PREFFIX_HEX6 + HOSPITAL_ENTITY_CODE + _hash(hospital_pkey)[:62]


def make_hospital_list_address():
    return TP_PREFFIX_HEX6 + HOSPITAL_ENTITY_CODE


def make_investigator_data_address(data_id):
    return TP_PREFFIX_HEX6 + INVESTIGATOR_DATA_ENTITY_CODE + _hash(data_id)[:62]


def make_investigator_address(investigator_pkey):
    return TP_PREFFIX_HEX6 + INVESTIGATOR_ENTITY_CODE + _hash(investigator_pkey)[:62]


def make_investigator_data_list_address():
    return TP_PREFFIX_HEX6 + INVESTIGATOR_DATA_ENTITY_CODE


def make_investigator_list_address():
    return TP_PREFFIX_HEX6 + INVESTIGATOR_ENTITY_CODE


# Investigator <-> Data relation
def make_data_investigator__relation_address(data_id, client_pkey):
    return TP_PREFFIX_HEX6 + DATA_INVESTIGATOR__RELATION_CODE + \
           INVESTIGATOR_DATA_ENTITY_CODE + _hash(data_id)[:30] + \
           INVESTIGATOR_ENTITY_CODE + _hash(client_pkey)[:28]


# Data <-> Investigator relation
def make_investigator_data__relation_address(client_pkey, data_id):
    return TP_PREFFIX_HEX6 + INVESTIGATOR_DATA__RELATION_CODE + \
           INVESTIGATOR_ENTITY_CODE + _hash(client_pkey)[:30] + \
           INVESTIGATOR_DATA_ENTITY_CODE + _hash(data_id)[:28]

# def make_doctor_address(doctor_pkey):
#     return TP_PREFFIX_HEX6 + DOCTOR_ENTITY_CODE + _hash(doctor_pkey)[:62]
#
#
# def make_doctor_list_address():
#     return TP_PREFFIX_HEX6 + DOCTOR_ENTITY_CODE


def make_patient_address(patient_pkey):
    return TP_PREFFIX_HEX6 + PATIENT_ENTITY_CODE + _hash(patient_pkey)[:62]


def make_patient_list_address():
    return TP_PREFFIX_HEX6 + PATIENT_ENTITY_CODE


# def make_lab_address(lab_pkey):
#     return TP_PREFFIX_HEX6 + LAB_ENTITY_CODE + _hash(lab_pkey)[:62]
#
#
# def make_lab_list_address():
#     return TP_PREFFIX_HEX6 + LAB_ENTITY_CODE


# def make_claim_address(claim_id, clinic_pkey):
#     return TP_PREFFIX_HEX6 + CLAIM_ENTITY_CODE + _hash(claim_id)[:16] + \
#            CLINIC_ENTITY_CODE + _hash(clinic_pkey)[:44]
#
#
# def make_claim_list_address():
#     return TP_PREFFIX_HEX6 + CLAIM_ENTITY_CODE


# EHR entity
def make_ehr_address(ehr_id):
    return TP_PREFFIX_HEX6 + EHR_ENTITY_CODE + _hash(ehr_id)[:62]


def make_ehr_list_address():
    return TP_PREFFIX_HEX6 + EHR_ENTITY_CODE


# EHR <-> Patient relation
def make_ehr_patient__relation_address(ehr_id, client_pkey):
    return TP_PREFFIX_HEX6 + EHR_PATIENT__RELATION_CODE + \
        EHR_ENTITY_CODE + _hash(ehr_id)[:30] + \
        PATIENT_ENTITY_CODE + _hash(client_pkey)[:28]


def make_patient_list_by_ehr_address(claim_id):
    return TP_PREFFIX_HEX6 + EHR_PATIENT__RELATION_CODE + EHR_ENTITY_CODE + _hash(claim_id)[:30]


# Patient <-> EHR relation
def make_patient_ehr__relation_address(client_pkey, ehr_id):
    return TP_PREFFIX_HEX6 + PATIENT_EHR__RELATION_CODE + \
        PATIENT_ENTITY_CODE + _hash(client_pkey)[:30] + \
        EHR_ENTITY_CODE + _hash(ehr_id)[:28]


def make_ehr_list_by_patient_address(client_pkey):
    return TP_PREFFIX_HEX6 + PATIENT_EHR__RELATION_CODE + PATIENT_ENTITY_CODE + _hash(client_pkey)[:30]


# EHR <-> Hospital relation
def make_ehr_hospital__relation_address(ehr_id, client_pkey):
    return TP_PREFFIX_HEX6 + EHR_HOSPITAL__RELATION_CODE + \
        EHR_ENTITY_CODE + _hash(ehr_id)[:30] + \
        HOSPITAL_ENTITY_CODE + _hash(client_pkey)[:28]


def make_hospital_list_by_ehr_address(ehr_id):
    return TP_PREFFIX_HEX6 + EHR_HOSPITAL__RELATION_CODE + EHR_ENTITY_CODE + _hash(ehr_id)[:30]


# Hospital <-> EHR relation
def make_hospital_ehr__relation_address(client_pkey, ehr_id):
    return TP_PREFFIX_HEX6 + HOSPITAL_EHR__RELATION_CODE + \
        HOSPITAL_ENTITY_CODE + _hash(client_pkey)[:30] + \
        EHR_ENTITY_CODE + _hash(ehr_id)[:28]


def make_ehr_list_by_hospital_address(client_pkey):
    return TP_PREFFIX_HEX6 + HOSPITAL_EHR__RELATION_CODE + HOSPITAL_ENTITY_CODE + _hash(client_pkey)[:30]


# def make_event_address(ehr_id, clinic_pkey, event_time):
#     return TP_PREFFIX_HEX6 + EVENT_ENTITY_CODE + _hash(ehr_id)[:12] + \
#            HOSPITAL_ENTITY_CODE + _hash(clinic_pkey)[:10] + \
#            _hash(event_time)[:38]
#
#
# def make_event_list_address(ehr_id, hospital_pkey):
#     return TP_PREFFIX_HEX6 + EVENT_ENTITY_CODE + _hash(claim_id)[:12] + \
#            CLINIC_ENTITY_CODE + _hash(clinic_pkey)[:10]


# # Lab Test entity
# def make_lab_test_address(lab_test_id):
#     return TP_PREFFIX_HEX6 + LAB_TEST_ENTITY_CODE + _hash(lab_test_id)[:62]
#
#
# def make_lab_test_list_address():
#     return TP_PREFFIX_HEX6 + LAB_TEST_ENTITY_CODE
#
#
# # Lab Test <-> Patient relation
# def make_lab_test_patient__relation_address(lab_test_id, client_pkey):
#     return TP_PREFFIX_HEX6 + LAB_TEST_PATIENT__RELATION_CODE + \
#         LAB_TEST_ENTITY_CODE + _hash(lab_test_id)[:30] + \
#         PATIENT_ENTITY_CODE + _hash(client_pkey)[:28]
#
#
# def make_patient_list_by_lab_test_address(lab_test_id):
#     return TP_PREFFIX_HEX6 + LAB_TEST_PATIENT__RELATION_CODE + LAB_TEST_ENTITY_CODE + _hash(lab_test_id)[:30]
#
#
# # Patient <-> Lab Test relation
# def make_patient_lab_test__relation_address(client_pkey, lab_test_id):
#     return TP_PREFFIX_HEX6 + PATIENT_LAB_TEST__RELATION_CODE + \
#         PATIENT_ENTITY_CODE + _hash(client_pkey)[:30] + \
#         LAB_TEST_ENTITY_CODE + _hash(lab_test_id)[:28]
#
#
# def make_lab_test_list_by_patient_address(client_pkey):
#     return TP_PREFFIX_HEX6 + PATIENT_LAB_TEST__RELATION_CODE + PATIENT_ENTITY_CODE + _hash(client_pkey)[:30]


# # Pulse entity
# def make_pulse_address(pulse_id):
#     return TP_PREFFIX_HEX6 + PULSE_ENTITY_CODE + _hash(pulse_id)[:62]
#
# # def make_pulse_address(public_key, timestamp):
# #     return TP_PREFFIX_HEX6 + PULSE_ENTITY_CODE + _hash(public_key)[:12] + \
# #            _hash(str(timestamp))[:50]
#
#
# def make_pulse_list_address():
#     return TP_PREFFIX_HEX6 + PULSE_ENTITY_CODE
#
#
# # Pulse <-> Patient relation
# def make_pulse_patient__relation_address(pulse_id, client_pkey):
#     return TP_PREFFIX_HEX6 + PULSE_PATIENT__RELATION_CODE + \
#         PULSE_ENTITY_CODE + _hash(pulse_id)[:30] + \
#         PATIENT_ENTITY_CODE + _hash(client_pkey)[:28]
#
#
# def make_patient_list_by_pulse_address(pulse_id):
#     return TP_PREFFIX_HEX6 + PULSE_PATIENT__RELATION_CODE + PULSE_ENTITY_CODE + _hash(pulse_id)[:30]
#
#
# # Patient <-> Pulse relation
# def make_patient_pulse__relation_address(client_pkey, pulse_id):
#     return TP_PREFFIX_HEX6 + PATIENT_PULSE__RELATION_CODE + \
#         PATIENT_ENTITY_CODE + _hash(client_pkey)[:30] + \
#         PULSE_ENTITY_CODE + _hash(pulse_id)[:28]
#
#
# def make_pulse_list_by_patient_address(client_pkey):
#     return TP_PREFFIX_HEX6 + PATIENT_PULSE__RELATION_CODE + PATIENT_ENTITY_CODE + _hash(client_pkey)[:30]


def get_current_timestamp():
    return int(round(time.time() * 1000))


# def get_signer(request, client_key):
#     if request.app.config.SIGNER_CLINIC.get_public_key().as_hex() == client_key:
#         client_signer = request.app.config.SIGNER_CLINIC
#     elif request.app.config.SIGNER_PATIENT.get_public_key().as_hex() == client_key:
#         client_signer = request.app.config.SIGNER_PATIENT
#     elif request.app.config.SIGNER_DOCTOR.get_public_key().as_hex() == client_key:
#         client_signer = request.app.config.SIGNER_DOCTOR
#     elif request.app.config.SIGNER_LAB.get_public_key().as_hex() == client_key:
#         client_signer = request.app.config.SIGNER_LAB
#     else:
#         client_signer = request.app.config.SIGNER_PATIENT
#     return client_signer
