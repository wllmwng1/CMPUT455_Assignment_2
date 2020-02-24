#!/bin/bash

# Filename: autopasta_presubmission.sh
# Purpose: Automatic 'pasta' script for presubmission.log

script presubmission.log
rm -rdf test_session_A2/
mkdir test_session_A2
cp assignment2.tgz test_session_A1/assignment2.tgz
cd test_session_A1/
tar -xf assignment2.tgz
cd assignment2
gogui-regress ./Nogo.py assignment2-public-tests.gtp
# gogui-regress ./Nogo.py a2-sample.gtp
exit

#



