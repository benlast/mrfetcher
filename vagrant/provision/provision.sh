#!/bin/bash -eu

set -o pipefail

echo "Running provision script as `whoami`"
sleep 2

# Configure APT to use Canadian mirror
sed -i -e 's/us.archive.ubuntu.com/ca.archive.ubuntu.com/' /etc/apt/sources.list
sed -i -e 's/security.ubuntu.com/security.ca.archive.ubuntu.com/' /etc/apt/sources.list

# Update the APT cache now that all the PPAs have been configured
sudo apt-get update

# Utilities
sudo apt-get -y install htop wget curl apt-file

# Install heroku toolbelt PPA
sudo apt-get install -y python-software-properties
sudo apt-add-repository 'deb http://toolbelt.herokuapp.com/ubuntu ./'
wget --quiet -O - https://toolbelt.herokuapp.com/apt/release.key | sudo apt-key add -

# Python 2.7.* backports
sudo apt-add-repository 'ppa:fkrull/deadsnakes-python2.7'

# Update the APT cache now that all the PPAs have been configured
sudo apt-get update

# Install key packages for development
sudo apt-get install -y git python2.7 \
    python-virtualenv python-dev build-essential libcurl4-gnutls-dev \
    zlib1g-dev libssl-dev \
    libsasl2-2 sasl2-bin libsasl2-dev libsasl2-modules \
    fontconfig heroku-toolbelt libffi-dev

# Move to the sync'd project directory
cd /vagrant

# Run installations
sudo -u vagrant -Hi /vagrant/vagrant/provision/setup_python.sh

# Set up privileged files
sudo cp vagrant/provision/files/sync-clock.sh /etc/cron.hourly/sync-clock.sh
sudo chmod +x /etc/cron.hourly/sync-clock.sh

echo "Provisioning script is done"
