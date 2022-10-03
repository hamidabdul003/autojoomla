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
install = os.system("apt update && apt upgrade -y && apt-get install apache2 mariadb-server php libapache2-mod-php php-cli php-mysql php-json php-opcache php-mbstring php-intl php-xml php-gd php-zip php-curl php-xmlrpc unzip -y")
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

print(""" \033[1;36m
┌══════════════════════════════════════════════════════════════┐
█                                                              █
█             LAMP has been successfuly installed              █
█                                                              █
└══════════════════════════════════════════════════════════════┘     \033[1;m""")

# file
path = '/etc/apache2/sites-available/wp.conf'

# Check whether the
# specified path is
# an existing file
isFile = os.path.isfile(path)

if isFile:
	print("File is Already Exist!")
else:
	f = open("/etc/apache2/sites-available/wp.conf", "a")
	f.write("<VirtualHost *:80> \n")
	f.write("  ServerName starbhak.com\n")
	f.write("  DirectoryIndex index.html index.php\n")
	f.write("  DocumentRoot /var/www/html/wp\n")
	f.write(" \n")
	f.write("  ErrorLog ${APACHE_LOG_DIR}/wp-error.log\n")
	f.write("  CustomLog ${APACHE_LOG_DIR}/wp-access.log combined\n")
	f.write(" \n")
	f.write("  <Directory /var/www/html/wp>\n")
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
install = os.system("a2ensite wp.conf")
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
child.sendline('CREATE DATABASE dbwordpress CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;\n')
child.sendline("GRANT ALL ON dbwordpress.* TO 'wpuser'@'localhost' IDENTIFIED BY 'password';")
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
	install = os.system("cd /opt/ && curl -O https://wordpress.org/latest.tar.gz")
				    
# Directory
path = '/var/www/html/wp'

# Check whether the
# specified path is an
# existing directory or not
isdir = os.path.isdir(path)
if isFile:
	print("Folder is Already Exist!")
else:
	install = os.system("cd /opt/ && tar xzvf latest.tar.gz -d /var/www/html/wp")
	install = os.system("chown -R www-data:www-data /var/www/html/wp")

print(""" \033[1;36m
┌══════════════════════════════════════════════════════════════┐
█                                                              █
█                   WORDPRESS HAS BEEN INSTALL                    █
█                                                              █
└══════════════════════════════════════════════════════════════┘     \033[1;m""")
