# Networking settings
HOST = 'localhost'
PORT = 8000
TIMEOUT = 500
KEEP_ALIVE = False

# Validator settings
TRIAL_VALIDATOR_HOST = 'localhost'
TRIAL_VALIDATOR_PORT = 6004

CONSENT_VALIDATOR_HOST = 'localhost'
CONSENT_VALIDATOR_PORT = 5004

# Database settings
DB_HOST = 'localhost'
DB_PORT = 28015
DB_NAME = 'marketplace'

# Runtime settings
DEBUG = True

# Secret keys
# WARNING! These defaults are insecure, and should be changed for deployment
SECRET_KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # any string
AES_KEY = 'ffffffffffffffffffffffffffffffff'  # 32 character hex string
BATCHER_PRIVATE_KEY = '1111111111111111111111111111111111111111111111111111111111111111'  # 64 character hex string
# BATCHER_PRIVATE_KEY_FILE_NAME_HOSPITAL = 'hospitalWEB'
# BATCHER_PRIVATE_KEY_FILE_NAME_DOCTOR = 'doctorWEB'
# BATCHER_PRIVATE_KEY_FILE_NAME_PATIENT = 'patientWEB'
BATCHER_PRIVATE_KEY_FILE_NAME_INVESTIGATOR = 'investigatorWEB'
# BATCHER_PRIVATE_KEY_FILE_NAME_INSURANCE = 'insuranceWEB'
