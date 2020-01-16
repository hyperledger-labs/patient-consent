from consent_processor.consent_common import helper
from consent_processor.consent_common.protobuf import consent_payload_pb2


class ConsentState(object):
    TIMEOUT = 3

    def __init__(self, context):
        """Constructor.
        Args:
            context (sawtooth_sdk.processor.context.Context): Access to
                validator state from within the transaction processor.
        """

        self._context = context

    def grant_read_ehr_access(self, dest_pkey, src_pkey):
        self._store_read_ehr_access(dest_pkey, src_pkey)

    def revoke_read_ehr_access(self, dest_pkey, src_pkey):
        self._revoke_read_ehr_access(dest_pkey, src_pkey)

    def grant_write_ehr_access(self, dest_pkey, src_pkey):
        self._store_write_ehr_access(dest_pkey, src_pkey)

    def revoke_write_ehr_access(self, dest_pkey, src_pkey):
        self._revoke_write_ehr_access(dest_pkey, src_pkey)

    def grant_share_ehr_access(self, dest_pkey, src_pkey):
        self._store_share_ehr_access(dest_pkey, src_pkey)

    def revoke_share_ehr_access(self, dest_pkey, src_pkey):
        self._revoke_share_ehr_access(dest_pkey, src_pkey)

    def grant_share_shared_ehr_access(self, dest_pkey, src_pkey):
        self._store_share_shared_ehr_access(dest_pkey, src_pkey)

    def revoke_share_shared_ehr_access(self, dest_pkey, src_pkey):
        self._revoke_share_shared_ehr_access(dest_pkey, src_pkey)

    def has_read_ehr_access(self, dest_pkey, src_pkey):
        return self._load_read_ehr_access(dest_pkey=dest_pkey, src_pkey=src_pkey)

    def has_write_ehr_access(self, dest_pkey, src_pkey):
        return self._load_write_ehr_access(dest_pkey=dest_pkey, src_pkey=src_pkey)

    def has_share_ehr_access(self, dest_pkey, src_pkey):
        return self._load_share_ehr_access(dest_pkey=dest_pkey, src_pkey=src_pkey)

    def has_share_shared_ehr_access(self, dest_pkey, src_pkey):
        return self._load_share_shared_ehr_access(dest_pkey=dest_pkey, src_pkey=src_pkey)

    def get_read_ehr_access_by_destination(self, dest_pkey):
        return self._load_read_ehr_access_by_destination(dest_pkey=dest_pkey)

    def get_write_ehr_access_by_destination(self, dest_pkey):
        return self._load_write_ehr_access_by_destination(dest_pkey=dest_pkey)

    def get_share_ehr_access_by_destination(self, dest_pkey):
        return self._load_share_ehr_access_by_destination(dest_pkey=dest_pkey)

    def get_share_shared_ehr_access_by_destination(self, dest_pkey):
        return self._load_share_shared_ehr_access_by_destination(dest_pkey=dest_pkey)

    def _load_read_ehr_access(self, dest_pkey, src_pkey):
        access_hex = [helper.make_consent_read_ehr_address(dest_pkey=dest_pkey, src_pkey=src_pkey)]
        state_entries = self._context.get_state(
            access_hex,
            timeout=self.TIMEOUT)
        if state_entries:
            access = consent_payload_pb2.ActionOnAccess()
            access.ParseFromString(state_entries[0].data)
            return access
        return None

    def _load_write_ehr_access(self, dest_pkey, src_pkey):
        access_hex = [helper.make_consent_write_ehr_address(dest_pkey=dest_pkey, src_pkey=src_pkey)]
        state_entries = self._context.get_state(
            access_hex,
            timeout=self.TIMEOUT)
        if state_entries:
            access = consent_payload_pb2.ActionOnAccess()
            access.ParseFromString(state_entries[0].data)
            return access
        return None

    def _load_share_ehr_access(self, dest_pkey, src_pkey):
        access_hex = [helper.make_consent_share_ehr_address(dest_pkey=dest_pkey, src_pkey=src_pkey)]
        state_entries = self._context.get_state(
            access_hex,
            timeout=self.TIMEOUT)
        if state_entries:
            access = consent_payload_pb2.ActionOnAccess()
            access.ParseFromString(state_entries[0].data)
            return access
        return None

    def _load_share_shared_ehr_access(self, dest_pkey, src_pkey):
        access_hex = [helper.make_consent_share_shared_ehr_address(dest_pkey=dest_pkey, src_pkey=src_pkey)]
        state_entries = self._context.get_state(
            access_hex,
            timeout=self.TIMEOUT)
        if state_entries:
            access = consent_payload_pb2.ActionOnAccess()
            access.ParseFromString(state_entries[0].data)
            return access
        return None

    def _load_read_ehr_access_by_destination(self, dest_pkey):
        access_hex = [helper.make_consent_read_ehr_list_address_by_destination_client(dest_pkey=dest_pkey)]
        state_entries = self._context.get_state(
            access_hex,
            timeout=self.TIMEOUT)
        if state_entries:
            access = consent_payload_pb2.ActionOnAccess()
            access.ParseFromString(state_entries[0].data)
            return access
        return None

    def _load_write_ehr_access_by_destination(self, dest_pkey):
        access_hex = [helper.make_consent_write_ehr_list_address_by_destination_client(dest_pkey=dest_pkey)]
        state_entries = self._context.get_state(
            access_hex,
            timeout=self.TIMEOUT)
        if state_entries:
            access = consent_payload_pb2.ActionOnAccess()
            access.ParseFromString(state_entries[0].data)
            return access
        return None

    def _load_share_ehr_access_by_destination(self, dest_pkey):
        access_hex = [helper.make_consent_share_ehr_list_address_by_destination_client(dest_pkey=dest_pkey)]
        state_entries = self._context.get_state(
            access_hex,
            timeout=self.TIMEOUT)
        if state_entries:
            access = consent_payload_pb2.ActionOnAccess()
            access.ParseFromString(state_entries[0].data)
            return access
        return None

    def _load_share_shared_ehr_access_by_destination(self, dest_pkey):
        access_hex = [helper.make_consent_share_shared_ehr_list_address_by_destination_client(dest_pkey=dest_pkey)]
        state_entries = self._context.get_state(
            access_hex,
            timeout=self.TIMEOUT)
        if state_entries:
            access = consent_payload_pb2.ActionOnAccess()
            access.ParseFromString(state_entries[0].data)
            return access
        return None

    def _store_read_ehr_access(self, dest_pkey, src_pkey):
        address = helper.make_consent_read_ehr_address(dest_pkey=dest_pkey, src_pkey=src_pkey)

        access = consent_payload_pb2.ActionOnAccess()
        access.dest_pkey = dest_pkey
        access.src_pkey = src_pkey

        state_data = access.SerializeToString()
        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)

    def _store_write_ehr_access(self, dest_pkey, src_pkey):
        address = helper.make_consent_write_ehr_address(dest_pkey=dest_pkey, src_pkey=src_pkey)

        access = consent_payload_pb2.ActionOnAccess()
        access.dest_pkey = dest_pkey
        access.src_pkey = src_pkey

        state_data = access.SerializeToString()
        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)

    def _store_share_ehr_access(self, dest_pkey, src_pkey):
        address = helper.make_consent_share_ehr_address(dest_pkey=dest_pkey, src_pkey=src_pkey)

        access = consent_payload_pb2.ActionOnAccess()
        access.dest_pkey = dest_pkey
        access.src_pkey = src_pkey

        state_data = access.SerializeToString()
        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)

    def _store_share_shared_ehr_access(self, dest_pkey, src_pkey):
        address = helper.make_consent_share_shared_ehr_address(dest_pkey=dest_pkey, src_pkey=src_pkey)

        access = consent_payload_pb2.ActionOnAccess()
        access.dest_pkey = dest_pkey
        access.src_pkey = src_pkey

        state_data = access.SerializeToString()
        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)

    def _revoke_read_ehr_access(self, dest_pkey, src_pkey):
        address = helper.make_consent_read_ehr_address(dest_pkey=dest_pkey, src_pkey=src_pkey)

        self._context.delete_state(
            [address],
            timeout=self.TIMEOUT)

    def _revoke_write_ehr_access(self, dest_pkey, src_pkey):
        address = helper.make_consent_write_ehr_address(dest_pkey=dest_pkey, src_pkey=src_pkey)

        self._context.delete_state(
            [address],
            timeout=self.TIMEOUT)

    def _revoke_share_ehr_access(self, dest_pkey, src_pkey):
        address = helper.make_consent_share_ehr_address(dest_pkey=dest_pkey, src_pkey=src_pkey)

        self._context.delete_state(
            [address],
            timeout=self.TIMEOUT)

    def _revoke_share_shared_ehr_access(self, dest_pkey, src_pkey):
        address = helper.make_consent_share_shared_ehr_address(dest_pkey=dest_pkey, src_pkey=src_pkey)

        self._context.delete_state(
            [address],
            timeout=self.TIMEOUT)

    def create_client(self, client):
        address = helper.make_client_address(public_key=client.public_key)

        # access = consent_payload_pb2.ActionOnAccess()
        # access.doctor_pkey = doctor_key
        # access.patient_pkey = patient_pkey

        state_data = client.SerializeToString()
        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)
