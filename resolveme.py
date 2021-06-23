#! /usr/bin/python3
from concurrent.futures import thread
import socket
import sys
import concurrent.futures
import argparse
# i couldnt implement the go version well but here is a quick dirty python version

target = None
output_file = None
verbose = False

def check(host):
    try:
        host = host.replace("\n","")
        _ip = socket.gethostbyname(host)
        
        if verbose:
            print(f"{host},{_ip}")
        else:
            print(f"{host}")
        if output_file != "":
            if verbose:
                output_file.write(f"{host},{_ip}\n")
            else:
                output_file.write(f"{host}\n")
    except:
        pass
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--threads",type=int, dest="threads",help="threads", default=4)
    parser.add_argument("-v", "--verbose", dest="verbose",action="store_true", help="verbose")
    parser.add_argument("-l", "--list", dest="list",help="list", default="")
    parser.add_argument("-o", "--output", dest="output",help="output file", default="")
    
    args = parser.parse_args()
    verbose = args.verbose
    
    if args.list != "":
        # that means there is a list supplied 
        rf = open(args.list,"r")
        target = rf
    else:
        target = sys.stdin

    if args.output != "":
        output_file = open(args.output,"w")

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        res = executor.map(check, target)
    


