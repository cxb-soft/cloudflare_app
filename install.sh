#!/bin/bash

source /etc/os-release
case $ID in
	debian|ubuntu|devuan)
		sudo apt-get install python3-pip
		sudo pip3 install flask
		pip3 install psutil
		python3 install.py
		;;
	centos|fedora|rhel)
		sudo yum install python3-pip
		sudo pip3 install flask
		pip3 install psutil
		python3 install.py
		;;
	*)
esac
