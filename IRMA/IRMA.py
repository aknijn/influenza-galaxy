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

def get_subtype(input_file, in_subtype):
    subtype = in_subtype
    if os.stat(input_file).st_size > 0:
        with open(input_file) as infile:
            firstline = infile.readline().strip()
            subtype_fasta = firstline[-3:]
            subtype_fasta = subtype_fasta.replace("_", "")
            subtype_letter = subtype_fasta[0:1]
            subtype_number = subtype_fasta[1:]
            if (subtype_letter == in_subtype) and subtype_number.isnumeric():
                subtype = subtype_fasta
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
        subprocess.run("tr -d '\r' < " + args.consensus + " > clean.fasta", shell=True)
        subprocess.run("awk '/^>/ {out = \"outdir/\" substr($1, 2) \".fasta\"; print > out} !/^>/ {print >> out}' clean.fasta", shell=True)
    else:
        subprocess.run(args.irma, shell=True)

    # copy fasta files and create the irma_json file
    influenza_type_str = 'ND'
    sequenced_region_list = []
    h_subtype_str = 'H'
    n_subtype_str = 'N'
    consensus_HA = glob.glob('outdir/*HA*.fasta')
    if consensus_HA:
        if os.path.isfile(consensus_HA[0]):
            sequenced_region_list.append('HA')
            shutil.copy(consensus_HA[0], args.consensus_HA)
            h_subtype_str = get_subtype(consensus_HA[0], 'H')
        consensus_NA = glob.glob('outdir/*NA*.fasta')
        if consensus_NA and os.path.isfile(consensus_NA[0]):
            sequenced_region_list.append('NA')
            shutil.copy(consensus_NA[0], args.consensus_NA)
            n_subtype_str = get_subtype(consensus_NA[0], 'N')
        consensus_MP = glob.glob('outdir/*MP*.fasta')
        if consensus_MP and os.path.isfile(consensus_MP[0]):
            sequenced_region_list.append('MP')
            shutil.copy(consensus_MP[0], args.consensus_MP)
        consensus_PB1 = glob.glob('outdir/*PB1*.fasta')
        if consensus_PB1 and os.path.isfile(consensus_PB1[0]):
            sequenced_region_list.append('PB1')
            shutil.copy(consensus_PB1[0], args.consensus_PB1)
        consensus_PB2 = glob.glob('outdir/*PB2*.fasta')
        if consensus_PB2 and os.path.isfile(consensus_PB2[0]):
            sequenced_region_list.append('PB2')
            shutil.copy(consensus_PB2[0], args.consensus_PB2)
        consensus_PA = glob.glob('outdir/*PA*.fasta')
        if consensus_PA and os.path.isfile(consensus_PA[0]):
            sequenced_region_list.append('PA')
            shutil.copy(consensus_PA[0], args.consensus_PA)
        consensus_NP = glob.glob('outdir/*NP*.fasta')
        if consensus_NP and os.path.isfile(consensus_NP[0]):
            sequenced_region_list.append('NP')
            shutil.copy(consensus_NP[0], args.consensus_NP)
        consensus_NS = glob.glob('outdir/*NS*.fasta')
        if consensus_NS and os.path.isfile(consensus_NS[0]):
            sequenced_region_list.append('NS')
            shutil.copy(consensus_NS[0], args.consensus_NS)
        if os.path.isfile('outdir/A_MP.fasta'):
            influenza_type_str = 'A'
        if os.path.isfile('outdir/B_MP.fasta'):
            influenza_type_str = 'B'

    if len(sequenced_region_list) == 8:
        sequenced_region_str = "ALL"
    elif len(sequenced_region_list) == 0:
        sequenced_region_str = "ND"
    else:
        sequenced_region_str = ','.join(sequenced_region_list)
   
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
