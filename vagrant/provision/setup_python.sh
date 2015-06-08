#!/usr/bin/env bash

cd /vagrant

# Create and configure virtualenv
VENV=/home/vagrant/venv
if [ -d ${VENV} ] ; then
    echo "Removing stale virtualenv"
    sudo rm -rf ${VENV}
fi

echo "Creating virtualenv"
virtualenv ${VENV}

set +o nounset
echo "Activating virtualenv"
source ${VENV}/bin/activate

pip install --upgrade setuptools
pip install --upgrade `fgrep pip== requirements.txt`

pip -q install --cache-dir .pipcache -r requirements.txt
