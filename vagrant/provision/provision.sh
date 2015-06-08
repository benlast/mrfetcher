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

# Python 2.7.9 backports
sudo apt-add-repository 'ppa:fkrull/deadsnakes-python2.7'

# Update the APT cache now that all the PPAs have been configured
sudo apt-get update

# Install key packages for development
sudo apt-get install -y git python2.7 \
    python-virtualenv python-dev build-essential libcurl4-gnutls-dev \
    libmemcached-dev zlib1g-dev libssl-dev memcached \
    libsasl2-2 sasl2-bin libsasl2-dev libsasl2-modules \
    postgresql-common libpq-dev postgresql-9.3 postgresql-contrib \
    fontconfig heroku-toolbelt nodejs npm libffi-dev openjdk-7-jre-headless

# Configure Postgres directories
mkdir -p /var/lib/postgresql/9.3/main
if [ -z "$(fgrep postgres /etc/passwd)" ] ; then
  useradd -d /var/lib/postgresql -m -g postgres -s /bin/bash
fi
chown -R postgres.postgres /var/lib/postgresql/9.3/main
chmod 0700 /var/lib/postgresql/9.3/main

sudo dpkg-reconfigure locales
mkdir -p /etc/postgresql/9.3/main/
sudo cp /vagrant/vagrant/provision/files/postgresql.conf /vagrant/vagrant/provision/files/pg_hba.conf /etc/postgresql/9.3/main/
chown -R postgres.postgres /etc/postgresql/9.3/main/

# Restart Postgres now that the config has been installed
sudo service postgresql restart

# Create databases & owners
echo "Creating databases and roles - ignore error messages about them already existing"
set +e
sudo -u postgres createuser pusheen
sudo -u postgres createdb pusheen -T template0 -l en_US.utf8 -E UTF-8 --no-password --owner=pusheen
sudo -u postgres createdb test -T template0 -l en_US.utf8 -E UTF-8 --no-password --owner=pusheen
sudo -u postgres createuser ubuntu
sudo -u postgres createdb circle_test -T template0 -l en_US.utf8 -E UTF-8 --no-password --owner=ubuntu
set -e

# Move to the sync'd project directory
cd /vagrant

# Run installations
sudo -u vagrant -Hi /vagrant/vagrant/provision/setup_python.sh

# Set up privileged files
sudo cp vagrant/provision/files/sync-clock.sh /etc/cron.hourly/sync-clock.sh
sudo chmod +x /etc/cron.hourly/sync-clock.sh

echo "Provisioning script is done"
