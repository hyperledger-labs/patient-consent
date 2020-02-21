from consent_processor.consent_common import helper
from consent_processor.consent_common.protobuf import consent_payload_pb2

import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class ConsentState(object):
    TIMEOUT = 3

    def __init__(self, context):
        """Constructor.
        Args:
            context (sawtooth_sdk.processor.context.Context): Access to
                validator state from within the transaction processor.
        """

        self._context = context

    def request_inform_document_consent(self, dest_pkey, src_pkey):
        self._store_request_inform_document_consent(dest_pkey, src_pkey)

    def sign_inform_document_consent(self, dest_pkey, src_pkey):
        self._store_sign_inform_consent(dest_pkey, src_pkey)

    def decline_inform_consent(self, dest_pkey, src_pkey):
        self._decline_sign_inform_consent(dest_pkey, src_pkey)

    def has_signed_inform_consent(self, dest_pkey, src_pkey):
        return self._load_inform_consent(dest_pkey=dest_pkey, src_pkey=src_pkey)

    def _load_inform_consent(self, dest_pkey, src_pkey):
        access_hex = [helper.make_sign_inform_document_consent_address(dest_pkey=dest_pkey, src_pkey=src_pkey)]
        state_entries = self._context.get_state(
            access_hex,
            timeout=self.TIMEOUT)
        if state_entries:
            access = consent_payload_pb2.ActionOnAccess()
            access.ParseFromString(state_entries[0].data)
            return access
        return None

    def _store_request_inform_document_consent(self, dest_pkey, src_pkey):
        address = helper.make_request_inform_document_consent_address(dest_pkey=dest_pkey, src_pkey=src_pkey)
        address_vice_versa = helper.make_request_inform_document_consent_address(dest_pkey=src_pkey, src_pkey=dest_pkey)

        access = consent_payload_pb2.ActionOnAccess()
        access.dest_pkey = dest_pkey
        access.src_pkey = src_pkey

        state_data = access.SerializeToString()
        self._context.set_state(
            {address: state_data,
             address_vice_versa: state_data},
            timeout=self.TIMEOUT)

    def _store_sign_inform_consent(self, dest_pkey, src_pkey):
        request_inform_consent_address = \
            helper.make_request_inform_document_consent_address(dest_pkey=dest_pkey, src_pkey=src_pkey)
        request_inform_consent_address_vice_versa = \
            helper.make_request_inform_document_consent_address(dest_pkey=src_pkey, src_pkey=dest_pkey)
        sign_inform_consent_address = \
            helper.make_sign_inform_document_consent_address(dest_pkey=dest_pkey, src_pkey=src_pkey)

        sign_inform_consent = consent_payload_pb2.ActionOnAccess()
        sign_inform_consent.dest_pkey = dest_pkey
        sign_inform_consent.src_pkey = src_pkey

        states = [request_inform_consent_address, request_inform_consent_address_vice_versa]
        LOGGER.debug("before delete_state: " + str(states))
        self._context.delete_state(
            states,
            timeout=self.TIMEOUT)
        LOGGER.debug("after delete_state: " + str(states))
        state_data = sign_inform_consent.SerializeToString()
        LOGGER.debug("before set_state")
        self._context.set_state(
            {sign_inform_consent_address: state_data},
            timeout=self.TIMEOUT)
        LOGGER.debug("after set_state")

    def _decline_sign_inform_consent(self, dest_pkey, src_pkey):
        request_inform_consent_address = \
            helper.make_request_inform_document_consent_address(dest_pkey=dest_pkey, src_pkey=src_pkey)

        request_inform_consent_address_vice_versa = \
            helper.make_request_inform_document_consent_address(dest_pkey=src_pkey, src_pkey=dest_pkey)

        sign_inform_consent_address = \
            helper.make_sign_inform_document_consent_address(dest_pkey=dest_pkey, src_pkey=src_pkey)

        self._context.delete_state(
            [request_inform_consent_address,
             request_inform_consent_address_vice_versa,
             sign_inform_consent_address],
            timeout=self.TIMEOUT)

    # def _store_data_processing_access(self, dest_pkey, src_pkey):
    #     address = helper.make_data_processing_access_address(dest_pkey=dest_pkey, src_pkey=src_pkey)
    #     access = consent_payload_pb2.ActionOnAccess()
    #     access.dest_pkey = dest_pkey
    #     access.src_pkey = src_pkey
    #
    #     state_data = access.SerializeToString()
    #     self._context.set_state(
    #         {address: state_data},
    #         timeout=self.TIMEOUT)
    #
    # def _revoke_investigator_access(self, dest_pkey, src_pkey):
    #     address = helper.make_investigator_access_address(dest_pkey=dest_pkey, src_pkey=src_pkey)
    #     self._context.delete_state(
    #         [address],
    #         timeout=self.TIMEOUT)
    #
    # def _revoke_data_processing_access(self, dest_pkey, src_pkey):
    #     address = helper.make_data_processing_access_address(dest_pkey=dest_pkey, src_pkey=src_pkey)
    #     self._context.delete_state(
    #         [address],
    #         timeout=self.TIMEOUT)

    # def _revoke_share_ehr_access(self, dest_pkey, src_pkey):
    #     address = helper.make_consent_share_ehr_address(dest_pkey=dest_pkey, src_pkey=src_pkey)
    #
    #     self._context.delete_state(
    #         [address],
    #         timeout=self.TIMEOUT)
    #
    # def _revoke_share_shared_ehr_access(self, dest_pkey, src_pkey):
    #     address = helper.make_consent_share_shared_ehr_address(dest_pkey=dest_pkey, src_pkey=src_pkey)
    #
    #     self._context.delete_state(
    #         [address],
    #         timeout=self.TIMEOUT)

    def create_client(self, client):
        address = helper.make_client_address(public_key=client.public_key)

        # access = consent_payload_pb2.ActionOnAccess()
        # access.doctor_pkey = doctor_key
        # access.patient_pkey = patient_pkey

        state_data = client.SerializeToString()
        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)
