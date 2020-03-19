#!/bin/bash

cd ../playbook-minimizer/src
zip -r playbook-minimizer.zip ./*
cp playbook-minimizer.zip ../../
cd ../
cd ../
echo '#!/usr/bin/env python3' | cat - playbook-minimizer.zip > ./playbook-minimizer-build
chmod a+x ./playbook-minimizer-build
