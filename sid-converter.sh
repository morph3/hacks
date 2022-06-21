#!/bin/bash

# Base-64 encoded objectSid
OBJECT_ID="foobar"

# Decode it, hex-dump it and store it in an array
G=($(echo -n $OBJECT_ID | base64 -d -i | hexdump -v -e '1/1 " %02X"'))

# SID in HEX
# SID_HEX=${G[0]}-${G[1]}-${G[2]}${G[3]}${G[4]}${G[5]}${G[6]}${G[7]}-${G[8]}${G[9]}${G[10]}${G[11]}-${G[12]}${G[13]}${G[14]}${G[15]}-${G[16]}${G[17]}${G[18]}${G[19]}-${G[20]}${G[21]}${G[22]}${G[23]}-${G[24]}${G[25]}${G[26]}${G[27]}${G[28]}

# SID Structure: https://technet.microsoft.com/en-us/library/cc962011.aspx
# LESA = Little Endian Sub Authority
# BESA = Big Endian Sub Authority
# LERID = Little Endian Relative ID
# BERID = Big Endian Relative ID

BESA2=${G[8]}${G[9]}${G[10]}${G[11]}
BESA3=${G[12]}${G[13]}${G[14]}${G[15]}
BESA4=${G[16]}${G[17]}${G[18]}${G[19]}
BESA5=${G[20]}${G[21]}${G[22]}${G[23]}
BERID=${G[24]}${G[25]}${G[26]}${G[27]}${G[28]}

LESA1=${G[2]}${G[3]}${G[4]}${G[5]}${G[6]}${G[7]}
LESA2=${BESA2:6:2}${BESA2:4:2}${BESA2:2:2}${BESA2:0:2}
LESA3=${BESA3:6:2}${BESA3:4:2}${BESA3:2:2}${BESA3:0:2}
LESA4=${BESA4:6:2}${BESA4:4:2}${BESA4:2:2}${BESA4:0:2}
LESA5=${BESA5:6:2}${BESA5:4:2}${BESA5:2:2}${BESA5:0:2}
LERID=${BERID:6:2}${BERID:4:2}${BERID:2:2}${BERID:0:2}

LE_SID_HEX=${LESA1}-${LESA2}-${LESA3}-${LESA4}-${LESA5}-${LERID}

# Initial SID value which is used to construct actual SID
SID="S-1"

# Convert LE_SID_HEX to decimal values and append it to SID as a string
IFS='-' read -ra ADDR <<< "${LE_SID_HEX}"
for OBJECT in "${ADDR[@]}"; do
  SID=${SID}-$((16#${OBJECT}))
done

echo ${SID}
