from ehr_processor.ehr_common import helper
from ehr_processor.ehr_common.protobuf.trial_payload_pb2 import Hospital, Patient, EHR
import logging

# from processor.common.protobuf.payload_pb2 import Claim

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class EHRState(object):
    TIMEOUT = 3

    def __init__(self, context):
        """Constructor.
        Args:
            context (sawtooth_sdk.processor.context.Context): Access to
                validator state from within the transaction processor.
        """

        self._context = context

    def create_hospital(self, hospital):
        hp = self._load_hospital(public_key=hospital.public_key)

        if hp is None:
            self._store_hospital(hospital)

    # def create_doctor(self, doctor):
    #     op = self._load_doctor(public_key=doctor.public_key)
    #
    #     if op is None:
    #         self._store_doctor(doctor)

    def create_patient(self, patient):
        pat = self._load_patient(public_key=patient.public_key)

        if pat is None:
            self._store_patient(patient)

    # def create_claim(self, claim_id, clinic_pkey, patient_pkey):
    #     od = self._load_claim(clinic_pkey=clinic_pkey, claim_id=claim_id)
    #
    #     if od is None:
    #         self._store_claim(clinic_pkey=clinic_pkey, claim_id=claim_id,
    #                           patient_pkey=patient_pkey)

    # def assign_doctor(self, claim_id, clinic_pkey, description, event_time):
    #     self._store_event(claim_id=claim_id, clinic_pkey=clinic_pkey, description=description,
    #                       event_time=event_time, event=payload_pb2.ActionOnClaim.ASSIGN)
    #
    # def first_visit(self, claim_id, clinic_pkey, description, event_time):
    #     self._store_event(claim_id=claim_id, clinic_pkey=clinic_pkey, description=description,
    #                       event_time=event_time, event=payload_pb2.ActionOnClaim.FIRST_VISIT)
    #
    # def pass_tests(self, claim_id, clinic_pkey, description, event_time):
    #     self._store_event(claim_id=claim_id, clinic_pkey=clinic_pkey, description=description,
    #                       event_time=event_time, event=payload_pb2.ActionOnClaim.PASS_TEST)
    #
    # def attend_procedures(self, claim_id, clinic_pkey, description, event_time):
    #     self._store_event(claim_id=claim_id, clinic_pkey=clinic_pkey, description=description,
    #                       event_time=event_time, event=payload_pb2.ActionOnClaim.PASS_PROCEDURE)
    #
    # def eat_pills(self, claim_id, clinic_pkey, description, event_time):
    #     self._store_event(claim_id=claim_id, clinic_pkey=clinic_pkey, description=description,
    #                       event_time=event_time, event=payload_pb2.ActionOnClaim.EAT_PILLS)
    #
    # def next_visit(self, claim_id, clinic_pkey, description, event_time):
    #     self._store_event(claim_id=claim_id, clinic_pkey=clinic_pkey, description=description,
    #                       event_time=event_time, event=payload_pb2.ActionOnClaim.NEXT_VISIT)

    def add_ehr(self, signer, ehr):
        ehr_obj = self._load_ehr(ehr.id)
        if ehr_obj is None:
            self._store_ehr(signer=signer, ehr=ehr)

    # def add_pulse(self, pulse):
    #     self._store_pulse(pulse=pulse)
    #
    # def create_claim(self, claim):
    #     self._store_claim(claim=claim)
    #
    # def update_claim(self, claim):
    #     self._update_claim(claim=claim)
    #
    # def close_claim(self, claim):
    #     self._close_claim(claim=claim)

    def get_hospital(self, public_key):
        hospital = self._load_hospital(public_key=public_key)
        return hospital

    # def get_doctor(self, public_key):
    #     doctor = self._load_doctor(public_key=public_key)
    #     return doctor

    def get_patient(self, public_key):
        patient = self._load_patient(public_key=public_key)
        return patient

    def get_ehr(self, ehr_id):
        lab = self._load_ehr(ehr_id=ehr_id)
        return lab

    # def get_claim(self, claim_id, clinic_pkey):
    #     od = self._load_claim(claim_id=claim_id, clinic_pkey=clinic_pkey)
    #     return od
    #
    # def get_claim2(self, claim_id):
    #     od = self._load_claim2(claim_id=claim_id)
    #     return od

    # def get_claim_hex(self, claim_hex):
    #     claim_hex = self._load_claim_hex(claim_hex=claim_hex)
    #     return claim_hex

    # def get_clinics(self):
    #     clinic = self._load_clinic()
    #     return clinic

    # def get_doctors(self):
    #     doctors = self._load_doctor()
    #     return doctors

    # def get_patients(self):
    #     patient = self._load_patient()
    #     return patient

    # def get_lab_tests(self):
    #     lab_tests = self._load_lab_tests()
    #     return lab_tests

    # def get_lab_tests_by_clinic(self, clinic_pkey):
    #     lab_tests = self._load_lab_tests(clinic_pkey=clinic_pkey)
    #     return lab_tests

    # def get_pulse(self):
    #     pulse_list = self._load_pulse()
    #     return pulse_list

    # def get_pulse_by_patient(self, patient_pkey):
    #     pulse_list = self._load_pulse(patient_pkey=patient_pkey)
    #     return pulse_list

    def _load_hospital(self, public_key):
        hospital = None
        hospital_hex = helper.make_hospital_address(public_key)
        state_entries = self._context.get_state(
            [hospital_hex],
            timeout=self.TIMEOUT)
        if state_entries:
            hospital = Hospital()
            hospital.ParseFromString(state_entries[0].data)
        return hospital

    # def _load_doctor(self, public_key):
    #     doctor = None
    #     doctor_hex = helper.make_doctor_address(public_key)
    #     state_entries = self._context.get_state(
    #         [doctor_hex],
    #         timeout=self.TIMEOUT)
    #     if state_entries:
    #         doctor = payload_pb2.CreateDoctor()
    #         doctor.ParseFromString(state_entries[0].data)
    #     return doctor
    #
    # def _load_lab(self, public_key):
    #     lab = None
    #     lab_hex = helper.make_lab_address(public_key)
    #     state_entries = self._context.get_state(
    #         [lab_hex],
    #         timeout=self.TIMEOUT)
    #     if state_entries:
    #         lab = payload_pb2.CreateLab()
    #         lab.ParseFromString(state_entries[0].data)
    #     return lab

    def _load_patient(self, public_key):
        patient = None
        patient_hex = helper.make_patient_address(public_key)
        state_entries = self._context.get_state(
            [patient_hex],
            timeout=self.TIMEOUT)
        if state_entries:
            patient = Patient()
            patient.ParseFromString(state_entries[0].data)
        return patient

    # def _load_claim_hex(self, claim_hex):
    #     claim = None
    #     state_entries = self._context.get_state(
    #         [claim_hex],
    #         timeout=self.TIMEOUT)
    #     if state_entries:
    #         claim = payload_pb2.CreateClaim()
    #         claim.ParseFromString(state_entries[0].data)
    #     return claim

    def _load_ehr(self, ehr_id):
        ehr = None
        ehr_hex = helper.make_ehr_address(ehr_id)
        state_entries = self._context.get_state(
            [ehr_hex],
            timeout=self.TIMEOUT)
        if state_entries:
            ehr = EHR()
            ehr.ParseFromString(state_entries[0].data)
        return ehr

    # def _load_claim(self, claim_id, clinic_pkey):
    #     claim = None
    #     claim_hex = [] if clinic_pkey is None and claim_id is None \
    #         else [helper.make_claim_address(claim_id, clinic_pkey)]
    #     state_entries = self._context.get_state(
    #         claim_hex,
    #         timeout=self.TIMEOUT)
    #     if state_entries:
    #         claim = payload_pb2.CreateClaim()
    #         claim.ParseFromString(state_entries[0].data)
    #     return claim

    # def _load_lab_tests(self):
    #     lab_test = None
    #     lab_test_hex = []
    #     # lab_test_hex = [] if clinic_pkey is None \
    #     #     else [helper.make_lab_test_list_by_clinic_address(clinic_pkey=clinic_pkey)]
    #     state_entries = self._context.get_state(
    #         lab_test_hex,
    #         timeout=self.TIMEOUT)
    #     if state_entries:
    #         lab_test = payload_pb2.AddLabTest()
    #         lab_test.ParseFromString(state_entries[0].data)
    #     return lab_test

    # def _load_pulse(self, patient_pkey=None):
    #     pulse = None
    #     pulse_hex = [] if patient_pkey is None \
    #         else [helper.make_pulse_list_by_patient_address(public_key=patient_pkey)]
    #     state_entries = self._context.get_state(
    #         pulse_hex,
    #         timeout=self.TIMEOUT)
    #     if state_entries:
    #         pulse = payload_pb2.AddPulse()
    #         pulse.ParseFromString(state_entries[0].data)
    #     return pulse

    def _store_hospital(self, hospital):
        address = helper.make_hospital_address(hospital.public_key)

        # clinic = payload_pb2.CreateClinic()
        # clinic.public_key = public_key
        # clinic.name = name

        state_data = hospital.SerializeToString()
        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)

    # def _store_doctor(self, doctor):
    #     address = helper.make_doctor_address(doctor.public_key)
    #
    #     # doctor = payload_pb2.CreateDoctor()
    #     # doctor.public_key = public_key
    #     # doctor.name = name
    #     # doctor.surname = surname
    #
    #     state_data = doctor.SerializeToString()
    #     self._context.set_state(
    #         {address: state_data},
    #         timeout=self.TIMEOUT)

    def _store_patient(self, patient):
        address = helper.make_patient_address(patient.public_key)

        state_data = patient.SerializeToString()
        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)

    # def _store_lab(self, lab):
    #     address = helper.make_lab_address(lab.public_key)
    #     state_data = lab.SerializeToString()
    #     self._context.set_state(
    #         {address: state_data},
    #         timeout=self.TIMEOUT)

    # def _store_claim(self, claim_id, clinic_pkey, patient_pkey):
    #     claim_hex = helper.make_claim_address(claim_id, clinic_pkey)
    #     claim = payload_pb2.CreateClaim()
    #     claim.claim_id = claim_id
    #     claim.clinic_pkey = clinic_pkey
    #     claim.patient_pkey = patient_pkey
    #
    #     state_data = claim.SerializeToString()
    #     self._context.set_state(
    #         {claim_hex: state_data},
    #         timeout=self.TIMEOUT)

    # def _store_event(self, claim_id, clinic_pkey, description, event_time, event):
    #     address = helper.make_event_address(claim_id, clinic_pkey, event_time)
    #     ev = payload_pb2.ActionOnClaim()
    #     ev.claim_id = claim_id
    #     ev.clinic_pkey = clinic_pkey
    #     ev.description = description
    #     ev.event_time = event_time
    #     ev.event = event
    #
    #     state_data = ev.SerializeToString()
    #     self._context.set_state(
    #         {address: state_data},
    #         timeout=self.TIMEOUT)
    #
    # def _store_lab_test(self, lab_test):
    #     lab_test_address = helper.make_lab_test_address(lab_test.id)
    #     lab_test_patient_relation_address = helper.make_lab_test_patient__relation_address(lab_test.id,
    #                                                                                        lab_test.client_pkey)
    #     patient_lab_test_relation_address = helper.make_patient_lab_test__relation_address(lab_test.client_pkey,
    #                                                                                        lab_test.id)
    #
    #     lab_test_data = lab_test.SerializeToString()
    #     states = {
    #         lab_test_address: lab_test_data,
    #         lab_test_patient_relation_address: str.encode(lab_test.client_pkey),
    #         patient_lab_test_relation_address: str.encode(lab_test.id)
    #     }
    #     LOGGER.debug("_store_lab_test: " + str(states))
    #     self._context.set_state(
    #         states,
    #         timeout=self.TIMEOUT)
    #
    # def _update_claim(self, claim):
    #     claim_address = helper.make_claim_address(claim.id)
    #     claim_data = claim.SerializeToString()
    #     states = {
    #         claim_address: claim_data
    #     }
    #     LOGGER.debug("_update_claim: " + str(states))
    #     self._context.set_state(
    #         states,
    #         timeout=self.TIMEOUT)
    #
    # def _close_claim(self, claim):
    #     claim_address = helper.make_claim_address(claim.id)
    #     claim_data = claim.SerializeToString()
    #     states = {
    #         claim_address: claim_data
    #     }
    #     LOGGER.debug("_close_claim: " + str(states))
    #     self._context.set_state(
    #         states,
    #         timeout=self.TIMEOUT)

    def _store_ehr(self, signer, ehr):
        ehr_address = helper.make_ehr_address(ehr.id)
        ehr_patient_relation_address = helper.make_ehr_patient__relation_address(ehr.id,
                                                                                 ehr.client_pkey)
        patient_ehr_relation_address = helper.make_patient_ehr__relation_address(ehr.client_pkey,
                                                                                 ehr.id)

        ehr_hospital_relation_address = helper.make_ehr_hospital__relation_address(ehr.id,
                                                                                   signer)
        hospital_ehr_relation_address = helper.make_hospital_ehr__relation_address(signer,
                                                                                   ehr.id)
        ehr_data = ehr.SerializeToString()
        states = {
            ehr_address: ehr_data,

            ehr_hospital_relation_address: str.encode(signer),
            hospital_ehr_relation_address: str.encode(ehr.id),

            ehr_patient_relation_address: str.encode(ehr.client_pkey),
            patient_ehr_relation_address: str.encode(ehr.id)
        }
        LOGGER.debug("_store_ehr: " + str(states))
        self._context.set_state(
            states,
            timeout=self.TIMEOUT)

    # def _store_pulse(self, pulse):
    #     pulse_address = helper.make_pulse_address(pulse.id)
    #     pulse_patient_relation_address = helper.make_pulse_patient__relation_address(pulse.id,
    #                                                                                  pulse.client_pkey)
    #     patient_pulse_relation_address = helper.make_patient_pulse__relation_address(pulse.client_pkey,
    #                                                                                  pulse.id)
    #
    #     pulse_data = pulse.SerializeToString()
    #     states = {
    #         pulse_address: pulse_data,
    #         pulse_patient_relation_address: str.encode(pulse.client_pkey),
    #         patient_pulse_relation_address: str.encode(pulse.id)
    #     }
    #     LOGGER.debug("_store_pulse: " + str(states))
    #     # state_data = p.SerializeToString()
    #     self._context.set_state(
    #         states,
    #         timeout=self.TIMEOUT)
