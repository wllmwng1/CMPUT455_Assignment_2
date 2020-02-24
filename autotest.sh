#!/bin/bash

echo "Testing on assignment2-public-tests.gtp"
gogui-regress ./assignment2/Nogo.py ./assignment2/assignment2-public-tests.gtp

echo "Testing on a2-sample.gtp"
gogui-regress ./assignment2/Nogo.py ./assignment2/a2-sample.gtp


