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

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))

def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument('--irma', dest='irma', help='irma command')
    parser.add_argument('--sequenced_region', dest='sequenced_region', help='sequenced_region')
    parser.add_argument('--consensus_HA', dest='consensus_HA', help='consensus_HA')
    parser.add_argument('--consensus_NA', dest='consensus_NA', help='consensus_NA')
    parser.add_argument('--consensus_MP', dest='consensus_MP', help='consensus_MP')
    parser.add_argument('--consensus_PB1', dest='consensus_PB1', help='consensus_PB1')
    parser.add_argument('--consensus_PB2', dest='consensus_PB2', help='consensus_PB2')
    parser.add_argument('--consensus_PA', dest='consensus_PA', help='consensus_PA')
    parser.add_argument('--consensus_NP', dest='consensus_NP', help='consensus_NP')
    parser.add_argument('--consensus_NS', dest='consensus_NS', help='consensus_NS')

    args = parser.parse_args()
    subprocess.run(args.irma, shell=True)

    # copy fasta files and create the sequenced_region string
    sequenced_region_list = []
    if os.path.isfile('outdir/A_HA_H3.fasta'):
        sequenced_region_list.append('HA')
        shutil.copy('outdir/A_HA_H3.fasta', args.consensus_HA)
    if os.path.isfile('outdir/A_NA_N2.fasta'):
        sequenced_region_list.append('NA')
        shutil.copy('outdir/A_NA_N2.fasta', args.consensus_NA)
    if os.path.isfile('outdir/A_MP.fasta'):
        sequenced_region_list.append('MP')
        shutil.copy('outdir/A_MP.fasta', args.consensus_MP)
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
    if os.path.isfile('outdir/B_HA_H3.fasta'):
        sequenced_region_list.append('HA')
        shutil.copy('outdir/B_HA_H3.fasta', args.consensus_HA)
    if os.path.isfile('outdir/B_NA_N2.fasta'):
        sequenced_region_list.append('NA')
        shutil.copy('outdir/B_NA_N2.fasta', args.consensus_NA)
    if os.path.isfile('outdir/B_MP.fasta'):
        sequenced_region_list.append('MP')
        shutil.copy('outdir/B_MP.fasta', args.consensus_MP)
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
        sequenced_region_str = "-"
    else:
        sequenced_region_str = ','.join(sequenced_region_list)
    with open(args.sequenced_region, "w") as sequenced_region_file:
        sequenced_region_file.write(sequenced_region_str)

if __name__ == "__main__":
    __main__()
