#!/bin/sh

# Minimal install for server setup

source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
sudo apt-get update -y
sudo apt-get dist-upgrade -y
sudo apt-get autoremove -y
sudo apt-get install -y \
    vim tree htop dfc rethinkdb npm silversearcher-ag \
    python libyaml-dev libxml2-dev libxslt-dev zlib1g-dev

sudo ln -s /usr/bin/nodejs /usr/bin/node

curl -s https://bootstrap.pypa.io/get-pip.py > /tmp/get-pip.py
python /tmp/get-pip.py --user
~/.local/bin/pip install --user -U flask flask-cache pyyaml requests rethinkdb

cat >> ~/.bashrc <<LINES
# Will be sourced in addition to bashrc each login
export PATH=~/.local/bin:/vagrant/bin:\$PATH
alias pipi='pip install --user'
cd /vagrant
LINES
