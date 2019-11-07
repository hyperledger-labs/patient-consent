from consent_processor.consent_common.protobuf import consent_payload_pb2


class ConsentPayload(object):

    def __init__(self, payload):
        self._transaction = consent_payload_pb2.ConsentTransactionPayload()
        self._transaction.ParseFromString(payload)

    def grant_read_ehr_access(self):
        return self._transaction.grant_read_ehr_access

    def revoke_read_ehr_access(self):
        return self._transaction.revoke_read_ehr_access

    def is_grant_read_ehr_access(self):
        return self._transaction.payload_type == consent_payload_pb2.ConsentTransactionPayload.GRANT_READ_EHR_ACCESS

    def is_revoke_read_ehr_access(self):
        return self._transaction.payload_type == consent_payload_pb2.ConsentTransactionPayload.REVOKE_READ_EHR_ACCESS

    def grant_write_ehr_access(self):
        return self._transaction.grant_write_ehr_access

    def revoke_write_ehr_access(self):
        return self._transaction.revoke_write_ehr_access

    def is_grant_write_ehr_access(self):
        return self._transaction.payload_type == consent_payload_pb2.ConsentTransactionPayload.GRANT_WRITE_EHR_ACCESS

    def is_revoke_write_ehr_access(self):
        return self._transaction.payload_type == consent_payload_pb2.ConsentTransactionPayload.REVOKE_WRITE_EHR_ACCESS

    def grant_share_ehr_access(self):
        return self._transaction.grant_share_ehr_access

    def revoke_share_ehr_access(self):
        return self._transaction.revoke_share_ehr_access

    def is_grant_share_ehr_access(self):
        return self._transaction.payload_type == consent_payload_pb2.ConsentTransactionPayload.GRANT_SHARE_EHR_ACCESS

    def is_revoke_share_ehr_access(self):
        return self._transaction.payload_type == consent_payload_pb2.ConsentTransactionPayload.REVOKE_SHARE_EHR_ACCESS

    def grant_share_shared_ehr_access(self):
        return self._transaction.grant_share_shared_ehr_access

    def revoke_share_shared_ehr_access(self):
        return self._transaction.revoke_share_shared_ehr_access

    def is_grant_share_shared_ehr_access(self):
        return self._transaction.payload_type == \
               consent_payload_pb2.ConsentTransactionPayload.GRANT_SHARE_SHARED_EHR_ACCESS

    def is_revoke_share_shared_ehr_access(self):
        return self._transaction.payload_type == \
               consent_payload_pb2.ConsentTransactionPayload.REVOKE_SHARE_SHARED_EHR_ACCESS

    def transaction_type(self):
        return self._transaction.payload_type

    def is_create_client(self):
        return self._transaction.payload_type == consent_payload_pb2.ConsentTransactionPayload.ADD_CLIENT

    def create_client(self):
        return self._transaction.create_client
