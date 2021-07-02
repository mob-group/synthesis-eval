# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "generic/ubuntu1804"

  config.vm.synced_folder ".", "/eval"

  config.vm.provider "virtualbox" do |vb|
    vb.cpus = 32
    vb.memory = 65536
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y \
      autoconf \
      bubblewrap \
      g++ \
      gcc \
      git \
      make \
      m4 \
      ocaml

    echo '/usr/bin' | sh <(curl -sL https://raw.githubusercontent.com/ocaml/opam/master/shell/install.sh)
  SHELL

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    cp -R /eval /home/vagrant/eval

    opam init
    eval `opam config env`

    cd /home/vagrant/eval
    echo ./get-simpl.sh
  SHELL
end
