#!/usr/bin/python2
# -*- coding: utf-8 -*-
import os
import sys
import mysql.connector as mysql


#---------------------------------------------------------------------------#
# This file is part of Joomla with Apache2.                                 #
# Joomla is an open-source cms used for publishing applications and websites#
# it It is written in PHP and uses MySQL/MariaDB as a database back-end.    #
# simple, user-friendly and built on a mobile-ready model–view–controller   #
# web application framework                                                 #
#                                                                           #
# In this Script, we will show you how to install Joomla CMS with Apache    #
# and secure with Let's Encrypt SSL on Ubuntu.                              # 
#                                                                           #
#---------------------------------------------------------------------------#
# Prerequisites                                                             #
# A server running Ubuntu 20.04 with 2 GB of RAM.                           #
# A valid domain name pointed with your server.                             #
# A root password is configured on your server.                             #
#---------------------------------------------------------------------------#
#                                                                           #
#        Copyright © 2020 Aham                                              #
#                                                                           #
#---------------------------------------------------------------------------#

if not os.geteuid() == 0:
    sys.exit("""\033[1;91m\n[!] Lamp installer must be run as root. ¯\_(ツ)_/¯\n\033[1;m""")

print(""" \033[1;36m
┌══════════════════════════════════════════════════════════════┐
█                                                              █
█                     Install LAMP Server                      █
█                                                              █
└══════════════════════════════════════════════════════════════┘     \033[1;m""")

#Username and password

#starting Install
print("\033[1;34m\n[++] Installing Lamp ... \033[1;m")
#update and install package
install = os.system("apt update && apt upgrade -y && apt-get install apache2 mariadb-server php7.4 libapache2-mod-php7.4 php7.4-cli php7.4-mysql php7.4-json php7.4-opcache php7.4-mbstring php7.4-intl php7.4-xml php7.4-gd php7.4-zip php7.4-curl php7.4-xmlrpc unzip -y")
install = os.system("apt update && apt autoremove -y")
# check file if available
path = 'get-pip.py'

# Check whether the
# specified path is
# an existing file
isFile = os.path.isfile(path)

if isFile:
	print("File is Already Exist!")
else:
	install = os.system("add-apt-repository universe && sudo apt update && curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py")
install = os.system("python2 get-pip.py && pip install mysql.connector && pip install pexpect")

import pexpect
#read input file
fin = open("/etc/php/7.4/apache2/php.ini", "rt")
#read file contents to string
data = fin.read()
#replace all occurrences of the required string
data = data.replace('memory_limit = 128M', 'memory_limit = 512M')
data = data.replace('upload_max_filesize = 2M', 'upload_max_filesize = 256M')
data = data.replace('post_max_size = 8M', 'post_max_size = 256M')
data = data.replace('output_buffering = 4096', 'output_buffering = Off')
data = data.replace('max_execution_time = 30', 'max_execution_time = 300')
data = data.replace(';date.timezone = ', 'date.timezone = Asia/Jakarta')
#close the input file
fin.close()
#open the input file in write mode
fin = open("/etc/php/7.4/apache2/php.ini", "wt")
#overrite the input file with the resulting data
fin.write(data)
#close the file
fin.close()

print(""" \033[1;36m
┌══════════════════════════════════════════════════════════════┐
█                                                              █
█             LAMP has been successfuly installed              █
█                                                              █
└══════════════════════════════════════════════════════════════┘     \033[1;m""")

# file
path = '/etc/apache2/sites-available/joomla.conf'

# Check whether the
# specified path is
# an existing file
isFile = os.path.isfile(path)

if isFile:
	print("File is Already Exist!")
else:
	f = open("/etc/apache2/sites-available/joomla.conf", "a")
	f.write("<VirtualHost *:80> \n")
	f.write("  ServerName starbhak.com\n")
	f.write("  DirectoryIndex index.html index.php\n")
	f.write("  DocumentRoot /var/www/html/joomla\n")
	f.write(" \n")
	f.write("  ErrorLog ${APACHE_LOG_DIR}/joomla-error.log\n")
	f.write("  CustomLog ${APACHE_LOG_DIR}/joomla-access.log combined\n")
	f.write(" \n")
	f.write("  <Directory /var/www/html/joomla>\n")
	f.write("      Options FollowSymLinks\n")
	f.write("      AllowOverride All\n")
	f.write("      Require all granted\n")
	f.write("  </Directory>\n")
	f.write(" \n")
	f.write("</VirtualHost>\n")
	f.close()

print(""" \033[1;36m
┌══════════════════════════════════════════════════════════════┐
█                                                              █
█          Apache2 has been successfuly config.                █
█                                                              █
└══════════════════════════════════════════════════════════════┘     \033[1;m""")

install = os.system("a2dissite 000-default.conf")
install = os.system("a2ensite joomla.conf")
install = os.system("systemctl reload apache2")

child = pexpect.spawnu('mysql_secure_installation')
child.sendline('\n')
child.sendline('y\n')
child.sendline('password')
child.sendline('password')
child.sendline('y\n')
child.sendline('y\n')
child.sendline('y\n')
child.sendline('y\n')
sys.stdout.flush()
child.interact()
print('DONE.')
child = pexpect.spawnu('mysql -uroot -ppassword')
child.sendline('CREATE DATABASE joomladb CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;\n')
child.sendline("GRANT ALL ON joomladb.* TO 'joomla'@'localhost' IDENTIFIED BY 'password';")
child.sendline('FLUSH PRIVILEGES;')
child.sendline('EXIT;\n')
sys.stdout.flush()
child.interact()

print(""" \033[1;36m
┌══════════════════════════════════════════════════════════════┐
█                                                              █
█                     DATABASE SET.                            █
█                                                              █
└══════════════════════════════════════════════════════════════┘     \033[1;m""")

# file
path = '/opt/Joomla_3-9-18-Stable-Full_Package.zip'

# Check whether the
# specified path is
# an existing file
isFile = os.path.isfile(path)

if isFile:
	print("File is Already Exist!")
else:
	install = os.system("cd /opt/ && wget https://downloads.joomla.org/cms/joomla3/3-9-18/Joomla_3-9-18-Stable-Full_Package.zip")
				    
# Directory
path = '/var/www/html/joomla'

# Check whether the
# specified path is an
# existing directory or not
isdir = os.path.isdir(path)
if isFile:
	print("Folder is Already Exist!")
else:
	install = os.system("cd /opt/ && unzip Joomla_3-9-18-Stable-Full_Package.zip -d /var/www/html/joomla")
	install = os.system("chown -R www-data:www-data /var/www/html/joomla")

print(""" \033[1;36m
┌══════════════════════════════════════════════════════════════┐
█                                                              █
█                   JOOMLA HAS BEEN INSTALL                    █
█                                                              █
└══════════════════════════════════════════════════════════════┘     \033[1;m""")
