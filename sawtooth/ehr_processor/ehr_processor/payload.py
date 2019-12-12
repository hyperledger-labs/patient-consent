from ehr_processor.ehr_common.protobuf.trial_payload_pb2 import TrialTransactionPayload


class EHRPayload(object):

    def __init__(self, payload):
        self._transaction = TrialTransactionPayload()
        self._transaction.ParseFromString(payload)

    def create_hospital(self):
        return self._transaction.create_hospital

    def create_investigator(self):
        return self._transaction.create_investigator

    def create_patient(self):
        return self._transaction.create_patient

    # def create_lab(self):
    #     return self._transaction.create_lab
    #
    # def create_claim(self):
    #     return self._transaction.create_claim
    #
    # def update_claim(self):
    #     return self._transaction.update_claim
    #
    # def close_claim(self):
    #     return self._transaction.close_claim
    #
    # def assign_doctor(self):
    #     return self._transaction.assign_doctor
    #
    # def first_visit(self):
    #     return self._transaction.first_visit
    #
    # def pass_tests(self):
    #     return self._transaction.pass_tests
    #
    # def attend_procedures(self):
    #     return self._transaction.attend_procedures
    #
    def set_eligible(self):
        return self._transaction.set_eligible

    def update_data(self):
        return self._transaction.update_data

    def create_ehr(self):
        return self._transaction.create_ehr

    def import_data(self):
        return self._transaction.import_data

    def is_create_hospital(self):
        return self._transaction.payload_type == TrialTransactionPayload.CREATE_HOSPITAL

    def is_create_investigator(self):
        return self._transaction.payload_type == TrialTransactionPayload.CREATE_INVESTIGATOR

    def is_create_patient(self):
        return self._transaction.payload_type == TrialTransactionPayload.CREATE_PATIENT

    def is_create_ehr(self):
        return self._transaction.payload_type == TrialTransactionPayload.CREATE_EHR

    def is_import_data(self):
        return self._transaction.payload_type == TrialTransactionPayload.IMPORT_DATA

    def is_update_data(self):
        return self._transaction.payload_type == TrialTransactionPayload.UPDATE_DATA

    def is_set_eligible(self):
        return self._transaction.payload_type == TrialTransactionPayload.SET_ELIGIBLE
    #
    # def is_assign_doctor(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.ASSIGN_DOCTOR
    #
    # def is_first_visit(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.FIRST_VISIT
    #
    # def is_pass_tests(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.PASS_TESTS
    #
    # def is_attend_procedures(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.ATTEND_PROCEDURES
    #
    # def is_eat_pills(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.EAT_PILLS
    #
    # def is_next_visit(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.NEXT_VISIT
    #
    # def is_lab_test(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.ADD_LAB_TEST
    #
    # def is_pulse(self):
    #     return self._transaction.payload_type == payload_pb2.TransactionPayload.ADD_PULSE

    def transaction_type(self):
        return self._transaction.payload_type
