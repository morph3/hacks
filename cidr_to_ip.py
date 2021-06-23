#! /usr/bin/python3

import ipaddress
import sys


if len(sys.argv) > 1:
    # there is an argument
    f = open(sys.argv[1])
    for line in f:
        for ip in ipaddress.IPv4Network(line.replace("\n","")):
            print(ip)

else:

    for line in sys.stdin:
        for ip in ipaddress.IPv4Network(line.replace("\n","")):
            print(ip)