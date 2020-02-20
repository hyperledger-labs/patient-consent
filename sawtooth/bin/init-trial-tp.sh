#!/usr/bin/env bash
bin/healthcare-protogen make_trial_protobuf
cp -R trial_common trial_processor/trial_processor
cd trial_processor || exit
python3 setup.py clean --all
python3 setup.py build
python3 setup.py install