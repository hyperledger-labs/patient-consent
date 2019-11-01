import hashlib
import random
import logging

from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader, Batch
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction, TransactionHeader

from . import helper as helper
from .protobuf.consent_payload_pb2 import Permission, ConsentTransactionPayload, Client, ActionOnAccess

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


def _make_transaction(payload, inputs, outputs, txn_signer, batch_signer):
    txn_header_bytes, signature = _transaction_header(txn_signer, batch_signer, inputs, outputs, payload)

    txn = Transaction(
        header=txn_header_bytes,
        header_signature=signature,
        payload=payload.SerializeToString()
    )

    return txn


def make_batch_and_id(transactions, batch_signer):
    batch_header_bytes, signature = _batch_header(batch_signer, transactions)

    batch = Batch(
        header=batch_header_bytes,
        header_signature=signature,
        transactions=transactions
    )

    return batch, batch.header_signature


def _make_header_and_batch(payload, inputs, outputs, txn_signer, batch_signer):
    txn_header_bytes, signature = _transaction_header(txn_signer, batch_signer, inputs, outputs, payload)

    txn = Transaction(
        header=txn_header_bytes,
        header_signature=signature,
        payload=payload.SerializeToString()
    )

    transactions = [txn]

    batch_header_bytes, signature = _batch_header(batch_signer, transactions)

    batch = Batch(
        header=batch_header_bytes,
        header_signature=signature,
        transactions=transactions
    )

    return batch, batch.header_signature


def _transaction_header(txn_signer, batch_signer, inputs, outputs, payload):
    txn_header_bytes = TransactionHeader(
        family_name=helper.TP_FAMILYNAME,
        family_version=helper.TP_VERSION,
        inputs=inputs,
        outputs=outputs,
        signer_public_key=txn_signer.get_public_key().as_hex(),  # signer.get_public_key().as_hex(),
        # In this example, we're signing the batch with the same private key,
        # but the batch can be signed by another party, in which case, the
        # public key will need to be associated with that key.
        batcher_public_key=batch_signer.get_public_key().as_hex(),  # signer.get_public_key().as_hex(),
        # In this example, there are no dependencies.  This list should include
        # an previous transaction header signatures that must be applied for
        # this transaction to successfully commit.
        # For example,
        # dependencies=['540a6803971d1880ec73a96cb97815a95d374cbad5d865925e5aa0432fcf1931539afe10310c122c5eaae15df61236079abbf4f258889359c4d175516934484a'],
        dependencies=[],
        nonce=random.random().hex().encode(),
        payload_sha512=hashlib.sha512(payload.SerializeToString()).hexdigest()
    ).SerializeToString()

    signature = txn_signer.sign(txn_header_bytes)
    return txn_header_bytes, signature


def _batch_header(batch_signer, transactions):
    batch_header_bytes = BatchHeader(
        signer_public_key=batch_signer.get_public_key().as_hex(),
        transaction_ids=[txn.header_signature for txn in transactions],
    ).SerializeToString()

    signature = batch_signer.sign(batch_header_bytes)

    return batch_header_bytes, signature


def create_hospital_client(txn_signer, batch_signer):
    permissions = [Permission(type=Permission.READ_HOSPITAL),
                   Permission(type=Permission.READ_OWN_HOSPITAL),
                   Permission(type=Permission.READ_EHR),
                   Permission(type=Permission.READ_OWN_EHR),
                   Permission(type=Permission.WRITE_EHR)
                   ]
    return create_client(txn_signer, batch_signer, permissions)


def create_patient_client(txn_signer, batch_signer):
    permissions = [Permission(type=Permission.READ_HOSPITAL),
                   Permission(type=Permission.READ_PATIENT),
                   Permission(type=Permission.READ_OWN_PATIENT),
                   Permission(type=Permission.REVOKE_WRITE_EHR_ACCESS),
                   Permission(type=Permission.GRANT_WRITE_EHR_ACCESS),
                   Permission(type=Permission.READ_OWN_EHR),
                   Permission(type=Permission.GRANT_READ_EHR_ACCESS),
                   Permission(type=Permission.REVOKE_READ_EHR_ACCESS)
                   ]
    return create_client(txn_signer, batch_signer, permissions)


def create_data_provider_client(txn_signer, batch_signer):
    permissions = [Permission(type=Permission.READ_HOSPITAL),
                   Permission(type=Permission.READ_OWN_DATA_PROVIDER),
                   Permission(type=Permission.READ_FORMATTED_EHR),
                   Permission(type=Permission.WRITE_FORMATTED_EHR)
                   ]
    return create_client(txn_signer, batch_signer, permissions)


def create_sponsor_client(txn_signer, batch_signer):
    permissions = [Permission(type=Permission.READ_LAB),
                   Permission(type=Permission.READ_OWN_LAB),
                   Permission(type=Permission.READ_LAB_TEST)]
    return create_client(txn_signer, batch_signer, permissions)


def create_investigator_client(txn_signer, batch_signer):
    permissions = [Permission(type=Permission.READ_OWN_INVESTIGATOR),
                   Permission(type=Permission.READ_FORMATTED_EHR)
                   ]
    return create_client(txn_signer, batch_signer, permissions)


def create_client(txn_signer, batch_signer, permissions):
    client_pkey = txn_signer.get_public_key().as_hex()
    LOGGER.debug('client_pkey: ' + str(client_pkey))
    inputs = outputs = helper.make_client_address(public_key=client_pkey)
    LOGGER.debug('inputs: ' + str(inputs))
    client = Client(
        public_key=client_pkey,
        permissions=permissions)

    payload = ConsentTransactionPayload(
        payload_type=ConsentTransactionPayload.ADD_CLIENT,
        create_client=client)

    LOGGER.debug('payload: ' + str(payload))

    return _make_transaction(
        payload=payload,
        inputs=[inputs],
        outputs=[outputs],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def grant_read_ehr_permission(txn_signer, batch_signer, dest_pkey):
    patient_pkey = txn_signer.get_public_key().as_hex()
    consent_hex = helper.make_consent_read_ehr_address(dest_pkey=dest_pkey, src_pkey=patient_pkey)

    access = ActionOnAccess(
        dest_pkey=dest_pkey,
        src_pkey=patient_pkey
    )

    payload = ConsentTransactionPayload(
        payload_type=ConsentTransactionPayload.GRANT_READ_EHR_ACCESS,
        grant_read_ehr_access=access)

    return _make_transaction(
        payload=payload,
        inputs=[consent_hex],
        outputs=[consent_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def revoke_read_ehr_permission(txn_signer, batch_signer, dest_pkey):
    patient_pkey = txn_signer.get_public_key().as_hex()
    consent_hex = helper.make_consent_read_ehr_address(dest_pkey=dest_pkey, src_pkey=patient_pkey)

    access = ActionOnAccess(
        dest_pkey=dest_pkey,
        src_pkey=patient_pkey
    )

    payload = ConsentTransactionPayload(
        payload_type=ConsentTransactionPayload.REVOKE_READ_EHR_ACCESS,
        revoke_read_ehr_access=access)

    return _make_transaction(
        payload=payload,
        inputs=[consent_hex],
        outputs=[consent_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def grant_write_ehr_permission(txn_signer, batch_signer, dest_pkey):
    patient_pkey = txn_signer.get_public_key().as_hex()
    consent_hex = helper.make_consent_write_ehr_address(dest_pkey=dest_pkey, src_pkey=patient_pkey)

    access = ActionOnAccess(
        dest_pkey=dest_pkey,
        src_pkey=patient_pkey
    )

    payload = ConsentTransactionPayload(
        payload_type=ConsentTransactionPayload.GRANT_WRITE_EHR_ACCESS,
        grant_write_ehr_access=access)

    return _make_transaction(
        payload=payload,
        inputs=[consent_hex],
        outputs=[consent_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)


def revoke_write_ehr_permission(txn_signer, batch_signer, dest_pkey):
    patient_pkey = txn_signer.get_public_key().as_hex()
    consent_hex = helper.make_consent_write_ehr_address(dest_pkey=dest_pkey, src_pkey=patient_pkey)

    access = ActionOnAccess(
        dest_pkey=dest_pkey,
        src_pkey=patient_pkey
    )

    payload = ConsentTransactionPayload(
        payload_type=ConsentTransactionPayload.REVOKE_WRITE_EHR_ACCESS,
        revoke_write_ehr_access=access)

    return _make_transaction(
        payload=payload,
        inputs=[consent_hex],
        outputs=[consent_hex],
        txn_signer=txn_signer,
        batch_signer=batch_signer)
