# -*- mode: ruby -*-
# vi: set ft=ruby :

# Recommended pugins:
#   vagrant plugin install vagrant-cachier
# Caches package installation to a folder under ~/.vagrant.d
#
#   vagrant plugin install vagrant-faster
# Sets cpu/memory to a good value above default, speeds up VM.

$root = <<EOF
source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
apt-get update -y
apt-get dist-upgrade -y
apt-get autoremove -y
apt-get install -y \
    build-essential automake autopoint autoconf pkg-config cmake ninja ccache \
    git mercurial vim zip unzip unrar rar p7zip-full tree htop dfc \
    rethinkdb npm exuberant-ctags silversearcher-ag ack-grep \
    ruby ruby-dev python-dev pandoc sphinx-common \
    libyaml-dev libxml2-dev libxslt-dev zlib1g-dev
#   lubuntu-desktop
# lubuntu adds many packages, installs a small light gui you can use firefox from to see site

# Webpack expects node
ln -s /usr/bin/nodejs /usr/bin/node
EOF

$user = <<EOF
curl -s https://bootstrap.pypa.io/get-pip.py > /tmp/get-pip.py
python /tmp/get-pip.py --user
~/.local/bin/pip install --user -r /vagrant/requirements.txt -r /vagrant/test/requirements.txt

cat > ~/.lbashrc <<LINES
# Will be sourced in addition to bashrc each login
export PATH=~/.local/bin:/vagrant/bin:/vagrant/node_modules/.bin:\$PATH
export PYTHONPATH=/vagrant
alias pipi='pip install --user'
cd /vagrant
LINES

# Purely optional & slow, sets up a dev environment
if [ ! -e ~/.my_scripts ]; then
  git clone --depth 1 https://github.com/starcraftman/.my_scripts/ ~/.my_scripts
  rm ~/.bashrc
  python .my_scripts/SysInstall.py home_save home
  echo "vim +Bootstrap +qa >/dev/null 2>&1"
  vim +Bootstrap +qa >/dev/null 2>&1
  ln -s ~/.sync_plugged ~/.vim/plugged
fi
EOF

Vagrant.require_version ">= 1.5.0"

VAGRANTFILE_API_VERSION = 2
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "boxcutter-VAGRANTSLASH-ubuntu1510"

  config.vm.provider :virtualbox do |v|
    # You may want to modify these if you don't use vagrant-faster
    #v.cpus = 4
    #v.memory = 4096
    v.customize ["modifyvm", :id, '--chipset', 'ich9'] # solves kernel panic issue on some host machines
    v.customize ["modifyvm", :id, "--ioapic", "on"]
  end

  if Vagrant.has_plugin?("vagrant-cachier")
    # Configure cached packages to be shared between instances of the same base box.
    # More info on http://fgrehm.viewdocs.io/vagrant-cachier/usage
    config.cache.scope = :box
  end

  config.vm.network :forwarded_port, guest: 5001, host: 5002
  config.vm.provision :shell, :inline => $root
  config.vm.provision :shell, :inline => $user, privileged: false
  config.vm.provision "file", source: "~/.ssh/known_hosts", destination: "~/.ssh/known_hosts"
  config.vm.synced_folder "~/.vim/plugged", "/home/vagrant/.sync_plugged", type: "rsync"
end
