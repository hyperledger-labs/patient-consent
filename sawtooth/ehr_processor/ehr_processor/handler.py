import logging

from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.handler import TransactionHandler

import ehr_processor.ehr_common.helper as helper
from ehr_processor.payload import EHRPayload
from ehr_processor.state import EHRState
# from ehr_processor.common.protobuf.payload_pb2 import EHR

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class EHRTransactionHandler(TransactionHandler):
    def __init__(self, namespace_prefix):
        self._namespace_prefix = namespace_prefix

    @property
    def family_name(self):
        return helper.TP_FAMILYNAME

    @property
    def family_versions(self):
        return [helper.TP_VERSION]

    @property
    def namespaces(self):
        return [self._namespace_prefix]

    def apply(self, transaction, context):
        try:

            _display("i'm inside handler _display")
            print("i'm inside handler print")

            header = transaction.header
            signer = header.signer_public_key
            LOGGER.debug("signer_public_key: " + str(signer))
            LOGGER.debug("transaction payload: " + str(transaction.payload))
            payload = EHRPayload(payload=transaction.payload)

            state = EHRState(context)

            if payload.is_create_hospital():
                hospital = payload.create_hospital()

                hp = state.get_hospital(signer)
                if hp is not None:
                    raise InvalidTransaction(
                        'Invalid action: Hospital already exists: ' + hospital.name)

                state.create_hospital(hospital)
            elif payload.is_create_data_provider():
                data_provider = payload.create_data_provider()

                dp = state.get_data_provider(data_provider.public_key)
                if dp is not None:
                    raise InvalidTransaction(
                        'Invalid action: Data Provider already exists: ' + data_provider.name)

                state.create_data_provider(data_provider)
            elif payload.is_create_patient():
                patient = payload.create_patient()

                pat = state.get_patient(signer)
                if pat is not None:
                    raise InvalidTransaction(
                        'Invalid action: Patient already exists: ' + patient.name)

                state.create_patient(patient)
            # elif healthcare_payload.is_create_lab():
            #     lab = healthcare_payload.create_lab()
            #
            #     lb = healthcare_state.get_lab(signer)
            #     if lb is not None:
            #         raise InvalidTransaction(
            #             'Invalid action: Lab already exists: ' + lb.name)
            #
            #     healthcare_state.create_lab(lab)
            # elif healthcare_payload.is_create_claim():
            #
            #     claim = healthcare_payload.create_claim()
            #     cl = healthcare_state.get_claim2(claim.id)
            #     if cl is not None:
            #         raise InvalidTransaction(
            #             'Invalid action: Claim already exist: ' + cl.id)
            #
            #     healthcare_state.create_claim(claim)
            # elif healthcare_payload.is_close_claim():
            #
            #     claim = healthcare_payload.close_claim()
            #     original_claim = healthcare_state.get_claim2(claim.id)
            #     if original_claim is None:
            #         raise InvalidTransaction(
            #             'Invalid action: Claim does not exist: ' + claim.id)
            #     if original_claim.state == Claim.CLOSED:
            #         raise InvalidTransaction(
            #             'Invalid action: Claim already closed: ' + claim.id)
            #     original_claim.provided_service = claim.provided_service
            #     original_claim.state = Claim.CLOSED
            #     healthcare_state.close_claim(original_claim)
            # elif healthcare_payload.is_update_claim():
            #
            #     claim = healthcare_payload.update_claim()
            #     original_claim = healthcare_state.get_claim2(claim.id)
            #     if original_claim is None:
            #         raise InvalidTransaction(
            #             'Invalid action: Claim does not exist: ' + claim.id)
            #     if original_claim.state == Claim.CLOSED:
            #         raise InvalidTransaction(
            #             'Invalid action: Can not update closed claim: ' + claim.id)
            #     original_claim.provided_service = claim.provided_service
            #     # original_claim.state = Claim.CLOSED
            #     healthcare_state.update_claim(original_claim)
            # elif healthcare_payload.is_assign_doctor():
            #     assign = healthcare_payload.assign_doctor()
            #
            #     clinic = healthcare_state.get_clinic(signer)
            #     if clinic is None:
            #         raise InvalidTransaction(
            #             'Invalid action: Clinic does not exist: ' + signer)
            #
            #     cl = healthcare_state.get_claim(assign.claim_id, assign.clinic_pkey)
            #     if cl is None:
            #         raise InvalidTransaction(
            #             'Invalid action: Claim does not exist: ' + assign.claim_id + '; clinic: ' + clinic.public_key)
            #
            #     healthcare_state.assign_doctor(assign.claim_id, assign.clinic_pkey, assign.description,
            #                                    assign.event_time)
            # elif healthcare_payload.is_first_visit():
            #     visit = healthcare_payload.first_visit()
            #
            #     clinic = healthcare_state.get_clinic(signer)
            #     if clinic is None:
            #         raise InvalidTransaction(
            #             'Invalid action: Clinic does not exist: ' + signer)
            #
            #     cl = healthcare_state.get_claim(visit.claim_id, visit.clinic_pkey)
            #     if cl is None:
            #         raise InvalidTransaction(
            #             'Invalid action: Claim does not exist: ' + visit.claim_id)
            #
            #     healthcare_state.first_visit(visit.claim_id, visit.clinic_pkey,
            #                                  visit.description, visit.event_time)
            # elif healthcare_payload.is_pass_tests():
            #     tests = healthcare_payload.pass_tests()
            #
            #     clinic = healthcare_state.get_clinic(signer)
            #     if clinic is None:
            #         raise InvalidTransaction(
            #             'Invalid action: Clinic does not exist: ' + signer)
            #
            #     cl = healthcare_state.get_claim(tests.claim_id, tests.clinic_pkey)
            #     if cl is None:
            #         raise InvalidTransaction(
            #             'Invalid action: Claim does not exist: ' + tests.claim_id)
            #
            #     healthcare_state.pass_tests(tests.claim_id, tests.clinic_pkey, tests.description, tests.event_time)
            # elif healthcare_payload.is_attend_procedures():
            #     procedures = healthcare_payload.attend_procedures()
            #
            #     clinic = healthcare_state.get_clinic(signer)
            #     if clinic is None:
            #         raise InvalidTransaction(
            #             'Invalid action: Clinic does not exist: ' + signer)
            #
            #     cl = healthcare_state.get_claim(procedures.claim_id, procedures.clinic_pkey)
            #     if cl is None:
            #         raise InvalidTransaction(
            #             'Invalid action: Claim does not exist: ' + procedures.claim_id)
            #
            # healthcare_state.attend_procedures(procedures.claim_id, procedures.clinic_pkey, procedures.description,
            # procedures.event_time) elif healthcare_payload.is_eat_pills(): pills = healthcare_payload.eat_pills()
            #
            #     clinic = healthcare_state.get_clinic(signer)
            #     if clinic is None:
            #         raise InvalidTransaction(
            #             'Invalid action: Clinic does not exist: ' + signer)
            #
            #     cl = healthcare_state.get_claim(pills.claim_id, pills.clinic_pkey)
            #     if cl is None:
            #         raise InvalidTransaction(
            #             'Invalid action: Claim does not exist: ' + pills.claim_id)
            #
            #     healthcare_state.eat_pills(pills.claim_id, pills.clinic_pkey, pills.description,
            #                                pills.event_time)
            # elif healthcare_payload.is_next_visit():
            #     examination = healthcare_payload.next_visit()
            #
            #     clinic = healthcare_state.get_clinic(signer)
            #     if clinic is None:
            #         raise InvalidTransaction(
            #             'Invalid action: Clinic does not exist: ' + signer)
            #
            #     cl = healthcare_state.get_claim(examination.claim_id, examination.clinic_pkey)
            #     if cl is None:
            #         raise InvalidTransaction(
            #             'Invalid action: Claim does not exist: ' + examination.claim_id)
            #
            #     healthcare_state.next_visit(examination.claim_id, examination.clinic_pkey,
            #                                 examination.description,
            #                                 examination.event_time)
            # elif healthcare_payload.is_lab_test():
            #     lab_test = healthcare_payload.lab_test()
            #
            #     # clinic = healthcare_state.get_clinic(signer)
            #     # if clinic is None:
            #     #     raise InvalidTransaction(
            #     #         'Invalid action: Clinic does not exist: ' + signer)
            #
            #     # healthcare_state.add_lab_test(signer, lab_test.height, lab_test.weight, lab_test.gender,
            #     #                               lab_test.a_g_ratio, lab_test.albumin, lab_test.alkaline_phosphatase,
            #     #                               lab_test.appearance, lab_test.bilirubin, lab_test.casts,
            #     #                               lab_test.color, lab_test.event_time)
            #     healthcare_state.add_lab_test(lab_test)
            elif payload.is_create_ehr():
                ehr = payload.create_ehr()

                # patient = healthcare_state.get_patient(signer)
                # if patient is None:
                #     raise InvalidTransaction(
                #         'Invalid action: Patient does not exist: ' + signer)

                state.create_ehr(signer, ehr)
            else:
                raise InvalidTransaction('Unhandled action: {}'.format(payload.transaction_type()))
        except Exception as e:
            print("Error: {}".format(e))
            logging.exception(e)
            raise InvalidTransaction(repr(e))


def _display(msg):
    n = msg.count("\n")

    if n > 0:
        msg = msg.split("\n")
        length = max(len(line) for line in msg)
    else:
        length = len(msg)
        msg = [msg]

    # pylint: disable=logging-not-lazy
    LOGGER.debug("+" + (length + 2) * "-" + "+")
    for line in msg:
        LOGGER.debug("+ " + line.center(length) + " +")
    LOGGER.debug("+" + (length + 2) * "-" + "+")
