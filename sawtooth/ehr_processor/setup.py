from __future__ import print_function
from setuptools import setup, find_packages  # , Command

conf_dir = "/etc/sawtooth"

# data_files = [
#     (conf_dir, ['packaging/healthcare.toml'])
# ]

# if os.path.exists("/etc/default"):
#     data_files.append(
#         ('/etc/default', ['packaging/systemd/sawtooth-healthcare-tp-python']))

# if os.path.exists("/lib/systemd/system"):
#     data_files.append(('/lib/systemd/system',
#                        ['packaging/systemd/sawtooth-healthcare-tp-python.service']))

setup(
    name='ehr-processor',
    version='0.1',
    description='Sawtooth Consent Processor Example',
    author='Hyperledger Sawtooth',
    url='https://github.com/hyperledger/sawtooth-core',
    packages=find_packages(),
    install_requires=[
        # 'aiohttp',
        'colorlog',
        'protobuf',
        'sawtooth-sdk',
        # 'sawtooth-signing',
        # 'PyYAML',
    ],
    # data_files=data_files,
    entry_points={
        'console_scripts': [
            'ehr-tp = ehr_processor.main:main',
        ]
    })
