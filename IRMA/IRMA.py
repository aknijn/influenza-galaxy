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
import sys
import os
import shutil
import subprocess
import json
import glob

def get_subtype(input_file):
    subtype = "ND"
    if os.stat(input_file).st_size > 0:
        with open(input_file) as infile:
            firstline = infile.readline().strip()
            subtype = firstline[-2:]
            if subtype == 'NA':
                if firstline[1] == 'A':
                    subtype = 'N?'
                else:
                    subtype = 'N'
            elif subtype == 'HA':
                if firstline[1] == 'A':
                    subtype = 'H?'
                else:
                    subtype = 'H'
    return subtype

def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument('--irma', dest='irma', help='irma command')
    parser.add_argument('--consensus', dest='consensus', help='consensus')
    parser.add_argument('--irma_json', dest='irma_json', help='irma_json')
    parser.add_argument('--consensus_HA', dest='consensus_HA', help='consensus_HA')
    parser.add_argument('--consensus_NA', dest='consensus_NA', help='consensus_NA')
    parser.add_argument('--consensus_MP', dest='consensus_MP', help='consensus_MP')
    parser.add_argument('--consensus_PB1', dest='consensus_PB1', help='consensus_PB1')
    parser.add_argument('--consensus_PB2', dest='consensus_PB2', help='consensus_PB2')
    parser.add_argument('--consensus_PA', dest='consensus_PA', help='consensus_PA')
    parser.add_argument('--consensus_NP', dest='consensus_NP', help='consensus_NP')
    parser.add_argument('--consensus_NS', dest='consensus_NS', help='consensus_NS')

    args = parser.parse_args()
    if "NO_IRMA" in args.irma:
        os.mkdir("outdir")
        subprocess.run("awk '/^>/ {out = ""outdir/"" substr($1, 2) "".fasta""; print > out} !/^>/ {print >> out}' " + args.consensus, shell=True)
    else:
        subprocess.run(args.irma, shell=True)

    # copy fasta files and create the irma_json file
    influenza_type_str = 'ND'
    sequenced_region_list = []

    consensus_HA = glob.glob('outdir/?_HA*.fasta')
    if os.path.isfile(consensus_HA[0]):
        sequenced_region_list.append('HA')
        shutil.copy(consensus_HA[0], args.consensus_HA)
    consensus_NA = glob.glob('outdir/?_NA*.fasta')
    if os.path.isfile(consensus_NA[0]):
        sequenced_region_list.append('NA')
        shutil.copy(consensus_NA[0], args.consensus_NA)
    if os.path.isfile('outdir/A_MP.fasta'):
        sequenced_region_list.append('MP')
        shutil.copy('outdir/A_MP.fasta', args.consensus_MP)
        influenza_type_str = 'A'
    if os.path.isfile('outdir/A_PB1.fasta'):
        sequenced_region_list.append('PB1')
        shutil.copy('outdir/A_PB1.fasta', args.consensus_PB1)
    if os.path.isfile('outdir/A_PB2.fasta'):
        sequenced_region_list.append('PB2')
        shutil.copy('outdir/A_PB2.fasta', args.consensus_PB2)
    if os.path.isfile('outdir/A_PA.fasta'):
        sequenced_region_list.append('PA')
        shutil.copy('outdir/A_PA.fasta', args.consensus_PA)
    if os.path.isfile('outdir/A_NP.fasta'):
        sequenced_region_list.append('NP')
        shutil.copy('outdir/A_NP.fasta', args.consensus_NP)
    if os.path.isfile('outdir/A_NS.fasta'):
        sequenced_region_list.append('NS')
        shutil.copy('outdir/A_NS.fasta', args.consensus_NS)
    if os.path.isfile('outdir/B_MP.fasta'):
        sequenced_region_list.append('MP')
        shutil.copy('outdir/B_MP.fasta', args.consensus_MP)
        influenza_type_str = 'B'
    if os.path.isfile('outdir/B_PB1.fasta'):
        sequenced_region_list.append('PB1')
        shutil.copy('outdir/B_PB1.fasta', args.consensus_PB1)
    if os.path.isfile('outdir/B_PB2.fasta'):
        sequenced_region_list.append('PB2')
        shutil.copy('outdir/B_PB2.fasta', args.consensus_PB2)
    if os.path.isfile('outdir/B_PA.fasta'):
        sequenced_region_list.append('PA')
        shutil.copy('outdir/B_PA.fasta', args.consensus_PA)
    if os.path.isfile('outdir/B_NP.fasta'):
        sequenced_region_list.append('NP')
        shutil.copy('outdir/B_NP.fasta', args.consensus_NP)
    if os.path.isfile('outdir/B_NS.fasta'):
        sequenced_region_list.append('NS')
        shutil.copy('outdir/B_NS.fasta', args.consensus_NS)

    if len(sequenced_region_list) == 8:
        sequenced_region_str = "ALL"
    elif len(sequenced_region_list) == 0:
        sequenced_region_str = "ND"
    else:
        sequenced_region_str = ','.join(sequenced_region_list)
    h_subtype_str = get_subtype(args.consensus_HA)
    n_subtype_str = get_subtype(args.consensus_NA)
   
    try:
        report_data = {}
        # prepare JSON output file
        report_data["sequenced_region"] = sequenced_region_str
        report_data["influenza_type"] = influenza_type_str
        report_data["h_subtype"] = h_subtype_str
        report_data["n_subtype"] = n_subtype_str
    finally:
        report = open(args.irma_json, 'w')
        report.write(json.dumps(report_data))
        report.close()

if __name__ == "__main__":
    __main__()
