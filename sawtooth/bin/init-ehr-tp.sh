#!/usr/bin/env bash
bin/healthcare-protogen make_ehr_protobuf
cp -R ehr_common ehr_processor/ehr_processor
cd ehr_processor || exit
python3 setup.py clean --all
python3 setup.py build
python3 setup.py install