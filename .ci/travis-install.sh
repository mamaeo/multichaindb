#!/bin/bash
# Copyright © 2020 Interplanetary Database Association e.V.,
# BigchainDB and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0


set -e -x

pip install --upgrade pip

if [[ -n ${TOXENV} ]]; then
    pip install --upgrade tox
elif [[ ${MULTICHAINDB_CI_ABCI} == 'enable' ]]; then
    docker-compose build --no-cache --build-arg abci_status=enable multichaindb
elif [[ $MULTICHAINDB_INTEGRATION_TEST == 'enable' ]]; then
    docker-compose build multichaindb python-driver
else
    docker-compose build --no-cache multichaindb
    pip install --upgrade codecov
fi
