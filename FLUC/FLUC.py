#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
############################################################################
# Istituto Superiore di Sanita'
# European Union Reference Laboratory (EU-RL) for Escherichia coli, including Verotoxigenic E. coli (VTEC)
# Developer: Arnold Knijn arnold.knijn@iss.it
############################################################################
"""

import argparse
import configparser
import sys
import os
import subprocess
import json

clademap = {
    "HA|A|H1|Wisconsin|MW626062.1|A/Wisconsin/588/2019(H1N1)":"nextstrain/flu/h1n1pdm/ha/MW626062",
    "HA|A|H3|Darwin|EPI_ISL_1563628|A/Darwin/6/2021(H3N2)":"nextstrain/flu/h3n2/ha/EPI1857216",
    "HA|B|H_vic|Brisbane|KX058884.1|B/Brisbane/60/2008(B_vic)":"nextstrain/flu/vic/ha/KX058884",
    "HA|B|H_yam|Wisconsin|JN993010.1|B/Wisconsin/01/2010(B_yam)":"nextstrain/flu/yam/ha/JN993010",
    "HA|A|H5|Guangdong|AF144305.1|A/Goose/Guangdong/1/96(H5N1)":"community/moncla-lab/iav-h5/ha/all-clades"}

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
  
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ha_consensus', dest='ha_consensus', help='ha consensus fasta')
    parser.add_argument('--clade', dest='clade', help='nextclade result')
    args = parser.parse_args()

    subprocess.run("blastn -query " + args.ha_consensus + " -db " + TOOL_DIR + "/data/HA_Flu -task blastn -evalue 0.001 -out blast_ha -outfmt '6 sseqid' -strand both -dust yes -max_target_seqs 1 -perc_identity 95.0", shell=True)
    with open('blast_ha', 'r') as blast_file:
        matching_ref = next(blast_file).strip()
    if len(matching_ref) > 0:
        matching_dataset = clademap.get(matching_ref)
        subprocess.run("nextclade dataset get --name=" + matching_dataset + " --output-dir=data", shell=True)
        subprocess.run("nextclade run " + args.ha_consensus + " --input-dataset=data --output-tsv=" + args.clade + " --output-all=nextclade/", shell=True)

if __name__ == "__main__":
    main()
