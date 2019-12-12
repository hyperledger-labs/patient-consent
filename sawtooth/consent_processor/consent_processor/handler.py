import logging

from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.handler import TransactionHandler

import consent_processor.consent_common.helper as helper
from consent_processor.payload import ConsentPayload
from consent_processor.state import ConsentState

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class ConsentTransactionHandler(TransactionHandler):
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

            # header = transaction.header
            # signer = header.signer_public_key
            LOGGER.debug("transaction payload: " + str(transaction.payload))
            consent_payload = ConsentPayload(payload=transaction.payload)

            consent_state = ConsentState(context)

            # if consent_payload.is_revoke_read_ehr_access():
            #     LOGGER.debug("Revoke Read EHR Access")
            #     access = consent_payload.revoke_read_ehr_access()
            #     consent_state.revoke_read_ehr_access(dest_pkey=access.dest_pkey, src_pkey=access.src_pkey)
            # elif consent_payload.is_grant_read_ehr_access():
            #     LOGGER.debug("Grant Read EHR Access")
            #     access = consent_payload.grant_read_ehr_access()
            #     consent_state.grant_read_ehr_access(dest_pkey=access.dest_pkey, src_pkey=access.src_pkey)
            if consent_payload.is_grant_investigator_access():
                LOGGER.debug("is_grant_investigator_access")
                access = consent_payload.grant_investigator_access()
                consent_state.grant_investigator_access(dest_pkey=access.dest_pkey, src_pkey=access.src_pkey)
            elif consent_payload.is_revoke_investigator_access():
                LOGGER.debug("is_revoke_investigator_access")
                access = consent_payload.revoke_investigator_access()
                consent_state.revoke_investigator_access(dest_pkey=access.dest_pkey, src_pkey=access.src_pkey)
            elif consent_payload.is_grant_data_processing_access():
                LOGGER.debug("is_grant_data_processing_access")
                access = consent_payload.grant_data_processing_access()
                consent_state.grant_data_processing_access(dest_pkey=access.dest_pkey, src_pkey=access.src_pkey)
            elif consent_payload.is_revoke_data_processing_access():
                LOGGER.debug("is_revoke_data_processing_access")
                access = consent_payload.revoke_data_processing_access()
                consent_state.revoke_data_processing_access(dest_pkey=access.dest_pkey, src_pkey=access.src_pkey)
            elif consent_payload.is_sign_inform_consent():
                LOGGER.debug("is_sign_inform_consent")
                access = consent_payload.sign_inform_consent()
                consent_state.sign_inform_document_consent(dest_pkey=access.dest_pkey, src_pkey=access.src_pkey)
            elif consent_payload.is_decline_inform_consent():
                LOGGER.debug("is_decline_inform_consent")
                access = consent_payload.decline_inform_consent()
                consent_state.decline_inform_consent(dest_pkey=access.dest_pkey, src_pkey=access.src_pkey)
            elif consent_payload.is_request_inform_consent():
                LOGGER.debug("is_request_inform_consent")
                access = consent_payload.request_inform_consent()
                consent_state.request_inform_document_consent(dest_pkey=access.dest_pkey, src_pkey=access.src_pkey)
            elif consent_payload.is_create_client():
                LOGGER.debug("is_create_client")
                client = consent_payload.create_client()
                consent_state.create_client(client)
            else:
                raise InvalidTransaction('Unhandled action: {}'.format(consent_payload.transaction_type()))
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
