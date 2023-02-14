import sys
import os
import re


def print_ips(file):
    expr = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    f = open(file, "r").read()
    for line in f.splitlines():
        try:
            print(expr.findall(line)[0])
        except:
            pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python print_ips.py file")
        sys.exit(1)

    print_ips(sys.argv[1])
