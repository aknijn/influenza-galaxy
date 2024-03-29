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
import json

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
  
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strain', dest='strain', help='strain name')
    parser.add_argument('--librarytype', dest='librarytype', help='library type')
    parser.add_argument('--region', dest='region', help='region')
    parser.add_argument('--year', dest='year', help='year')
    parser.add_argument('--irma_json', dest='irma_json', help='irma json')
    parser.add_argument('--flu_json', dest='flu_json', help='output json')
    
    args = parser.parse_args()
    try:
        report_data = {}
        # prepare JSON output file
        report_data["information_name"] = args.strain
        report_data["region"] = args.region
        report_data["year"] = args.year
        # library type
        library = open(args.librarytype).readline().rstrip()
        if library == 'iont':
            report_data["sequence"] = "Ion Torrent"
        elif library == 'illu':
            report_data["sequence"] = "Illumina"
        elif library == 'nano':
            report_data["sequence"] = "Nanopore"
        elif library == 'sang':
            report_data["sequence"] = "Sanger"
        elif library == 'cons':
            report_data["sequence"] = "Consensus"

        if os.path.getsize(args.irma_json) != 0:
            with open(args.irma_json, "rb") as irma_infile:
                report_data.update(json.load(irma_infile))
        if report_data["sequenced_region"] != 'ALL':
            report_data["qc_status"] = 'Failed'
        else:
            report_data["qc_status"] = 'Passed'
        report_data["notifica"] = '-'

    finally:
        report = open(args.flu_json, 'w')
        report.write("[" + json.dumps(report_data) + "]")
        report.close()

if __name__ == "__main__":
    main()
