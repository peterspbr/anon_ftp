#!/usr/bin/python

'''
+------------------------------------------+
| Automatic FTP anonymous login tool V1    |
|     Coded By CrashBloodborn              |
|     GitHub: https://github.com/peterspbr |
+------------------------------------------+

That code simply verify if an ftp application have anonymous login and try to connect with random password
'''

import socket
import sys
import re
import time
import os
import termcolor
import string
import random

def banner():
    os.system("clear")
    print "Started at " + time.ctime() + "\n"
    print '''
+------------------------------------------+
| Automatic FTP anonymous login tool V1    |
|     Coded By CrashBloodborn              |
|     GitHub: https://github.com/peterspbr |
+------------------------------------------+
    '''

if len(sys.argv) < 2:
    banner()
    print "Usage: anon_ftp.py <host_addr>\n"
    exit()
elif len(sys.argv) > 2:
    banner()
    print "Too many arguments...\n"
    print "Usage: anon_ftp.py <host_addr>\n"
    exit()

host_addr = sys.argv[1]

def shell_exec(s):
    command_shell = raw_input("FTP > ")
    s.send(command_shell + "\r\n")
    shell_response = s.recv(1024)

    if command_shell == "exit" or command_shell == "quit" or command_shell == "bye":
        s.send("EXIT\r\n")
        print "Bye!\n"
        exit()

    if re.search("500", shell_response):
        print "[-] Wrong command!\n"
    else:
        print shell_response
    shell_exec(s)

try:
    banner()
    random_pass = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(100))
    print "[*] Trying to connect to the host %s\n" % host_addr
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host_addr, 21))
    ftp_banner = sock.recv(1024)

    if re.search("vsFTPd 2.3.4", ftp_banner):
        print termcolor.colored("[*] That FTP version seems to be vulnerable! For further informations search for OSVDB-73573\n", "green")

    sock.send("USER anonymous\r\n")
    sock.recv(1024)
    sock.send("PASS " + random_pass + "\r\n")
    response = sock.recv(1024)

    if re.search("230", response):
        print termcolor.colored("[+] Connected! Dropping shell\n", "green")
        shell_exec(sock)
    else:
        print termcolor.colored("[-] Ftp server does not accept anonymous login... Exiting\n", "red")

    sock.close()
except socket.error:
    os.system("clear")
    print termcolor.colored("[-] Something wrong...\n", "red")
    print "[*] Cannot connect to the host %s\n" % host_addr
    print "[*] Please verify if the address is correct.\n"
    exit(1)
except KeyboardInterrupt:
    print "\nCTRL+C pressed... Exiting\n"
    print "Next time type exit\n"
    exit(1)