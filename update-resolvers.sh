#!/bin/bash
wget https://raw.githubusercontent.com/trickest/resolvers/main/resolvers-extended.txt -O /tmp/resolvers-extended.txt
cat /tmp/resolvers-extended.txt | cut -d ' ' -f1 > /tmp/resolvers.txt
sort -u /tmp/resolvers.txt -o /tmp/resolvers.txt
cp /tmp/resolvers.txt /opt/sectumsempra/wordlists/resolvers.txt
