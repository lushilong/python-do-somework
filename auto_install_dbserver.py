#!/usr/bin/python
#-*-coding=utf-8
# 

import os, sys, re
from ftplib import FTP
import socket
import commands
import subprocess

http_port = 80
https_port = 443
mysql_port = 3306
mysql_passwd = "dingjia"
ftp_ip = "192.168.88.10"
ftp_user = "scutech"
ftp_passwd = "dingjia"
ftp_dir = "/ftp_product_installer/wddps/2013/2.2.17/"


# This function try to connect the FTP
def ConnectFtp():
    try:
        socket.gethostbyname("baidu.com")
    except:
        print "Can not connect to internet !!!"
        sys.exit(0)

    try:
        ftp = FTP(ftp_ip)
    except:
        print "Cna not connect to Ftp Server !!!"
        sys.exit(0)
    try:
        ftp.login(ftp_user, ftp_passwd)
    except:
        print "Can not login to Ftp Server !!!"
        sys.exit(0)
    try:
        ftp.cwd(ftp_dir)
    except:
        print "Can not open Ftp directory !!!"
        ftp.quit()
        sys.exit(0)

    return ftp


# This function get the last version package
def GetLastVsersion():

    searchftp = ConnectFtp()
    package_list = searchftp.nlst()
    pattern = r'dbackup-server-2.2-([0-9]{4,5}).([0-9]{2}).noarch.el6.run'
    handle = re.compile(pattern)
    package_version = 0
    last_version_package = ''
    for i in package_list:
        match_package = handle.match(i)

        if match_package != None:
            getversion = int(match_package.group(1))
            
            if package_version < getversion:
                package_version = getversion
                last_version_package = i

    if package_version == 0:
        print "Can not match any packages......"
        sys.exit(0)
    else:
        return last_version_package

    searchftp.quit()


# define function download last version of Dbackup Agent Package from Ftp
def AutoDownPackage(package_name):

    print "Downloading Dbackup Server......"
    downloadftp = ConnectFtp() 
    localfile = "/home/serverpackage/" + package_name
    try:
        downloadftp.retrbinary('RETR ' + package_name, open(localfile, 'wb').write)
        print "Download Dbackup Server successful !!!"
    except:
        print "Download Dbackup Server fail........"
        sys.exit(0)

    downloadftp.quit()


# define function autoinstall DbackupServer
def AutoInstallServer(package_name):
    
    install = 'sh /home/serverpackage/' + package_name
    p = subprocess.Popen(install, shell=True, stdout=subprocess.PIPE,\
            stdin=subprocess.PIPE, stderr=subprocess.PIPE, cwd='/home/serverpackage/')
    p.stdin.write(str(http_port) + '\n')
    p.stdin.write(str(https_port) + '\n')
    p.stdin.write(str(mysql_port) + '\n')
    p.stdin.write(mysql_passwd + '\n')
    p.stdin.write(mysql_passwd + '\n') 

    while 1:
        buff = p.stdout.readline()
        if buff == '' and p.poll != None:
            return 0 
            break
        else:
            print buff,


# define function autouninstall DbackupServer
def AutoUninstallServer():

    try:
        os.system('rpm -e dbackup-server')
        os.system('rpm -e dbackup-lic')
        os.system('rpm -e scutech-php')
        os.system('rpm -e scutech-apache')
        os.system('rpm -e scutech-mysql')
        return 0
    except:
        return 1


# define function check if install Dbserver
def CheckInfo():

    result = commands.getoutput('rpm -q dbackup-server')
    return result


if __name__ == '__main__':
   
    os.system('rm -rf /home/serverpackage')
    os.system('mkdir /home/serverpackage')
    last_package = GetLastVsersion()
    get_current = CheckInfo() 
    newestversion = re.findall(r'(?<=-).{11,12}?(?=\.)', last_package)
    if get_current == "package dbackup-server is not installed":
        print "This System has not installed Dbackup Server!"
        print "The last version is [ %s ]" % newestversion[0]
        ips = raw_input('Press "ENTER" to install newest Dbackup Server: ')
        downloads = AutoDownPackage(last_package)
        if AutoInstallServer(last_package) == 0:
            print "Install Dbackup Server successful !!!"
        else:
            print "Install Dbackup Server fail......"
    else:
        currentversion = re.findall(r'(?<=-).{11,12}?(?=\.)', get_current)
        print "There is aready installed [ %s ]" % currentversion[0]
        print "And the newest version is [ %s ]" % newestversion[0]
        print "You can do:"
        print "Press '1' --will uninstall Dbackup Server"
        print "Press '2' --will remove and install newest Dbackup Server"
        print "Press '0' --exit"
        while 1:
            try:
                get_input = int(raw_input("Please choose one: "))
                if get_input in [0, 1, 2]:
                    break
                else:
                    continue
            except BaseException:
                print "Please entry a number !"
        if get_input == 0:
            sys.exit(0)
        elif get_input in [1, 2]: 
            print "Uninstalling Dbackup Server......"
            if AutoUninstallServer() == 0:
                print "Dbackup Server uninstall successful !!!"
            else:
                print "Dbackup Server uninstall fail......"
                sys.exit(0)
            if get_input == 2:
                downloads = AutoDownPackage(last_package)
                print "Installing Dbackup Server......"
                if AutoInstallServer(last_package) == 0:
                    print "Dbackup Server install successful !!!"
                else:
                    print "Dbackup Server install fail......"
        
        else:
            print "Something ERROR........"
