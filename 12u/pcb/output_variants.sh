#!/usr/bin/env bash

for i in top bottom 10u 10u-top 10u-bottom; do 
    kibot -d variants -s erc,drc -g variant=${i} JLCPCB
done
mv variants/JLCPCB/*.zip variants/
rm -r variants/JLCPCB