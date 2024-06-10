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

def openFileAsTable(filename):
    with open(filename) as table_in:
        table_data = [[str(col).rstrip() for col in row.split('\t')] for row in table_in]
    return table_data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strain', dest='strain', help='strain name')
    parser.add_argument('--librarytype', dest='librarytype', help='library type')
    parser.add_argument('--region', dest='region', help='region')
    parser.add_argument('--year', dest='year', help='year')
    parser.add_argument('--irma_json', dest='irma_json', help='irma json')
    parser.add_argument('--clade', dest='clade', help='nextclade clade')
    parser.add_argument('--clade_json', dest='clade_json', help='clade json')
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

        if os.path.getsize(args.clade) != 0:
            nextclade_result = openFileAsTable(args.clade)
            for i in range(40):
                if nextclade_result[0][i] == "clade":
                    report_data["clade"] = nextclade_result[1][i]
                if nextclade_result[0][i] == "aaSubstitutions":
                    report_data["aa_mut"] = nextclade_result[1][i]
                if nextclade_result[0][i] == "frameShifts":
                    report_data["frame_shift"] = nextclade_result[1][i]

        irma_data = """{"sequenced_region": "ND", "h_subtype": "H", "n_subtype": "N", "influenza_type": "ND"}"""
        if os.path.getsize(args.irma_json) != 0:
            with open(args.irma_json, "rb") as irma_infile:
                irma_data = json.load(irma_infile)
        clade_data = """{"ha_reference": "ND", "h_subtype": "H", "influenza_type": "ND"}"""
        if os.path.getsize(args.clade_json) != 0:
            with open(args.clade_json, "rb") as clade_infile:
                clade_data = json.load(clade_infile)
        report_data["sequenced_region"] = irma_data["sequenced_region"]
        report_data["n_subtype"] = irma_data["n_subtype"]
        report_data["ha_reference"] = clade_data["ha_reference"]
        if irma_data["influenza_type"] == 'A' or irma_data["influenza_type"] == 'B':
            report_data["influenza_type"] = irma_data["influenza_type"]
        else:
            report_data["influenza_type"] = clade_data["influenza_type"]
        if irma_data["h_subtype"] != 'H':
            report_data["h_subtype"] = irma_data["h_subtype"]
        else:
            report_data["h_subtype"] = clade_data["h_subtype"]
        if report_data["sequenced_region"] != 'ALL':
            report_data["qc_status"] = 'Failed'
        else:
            report_data["qc_status"] = 'Passed'

        report_data["notifica"] = '-'
        if clade_data["h_subtype"] == 'H':
            report_data["notifica"] = 'BLAST senza risultato'
        elif clade_data["h_subtype"] == 'H_yam':
            report_data["notifica"] = 'H_yam'

    finally:
        report = open(args.flu_json, 'w')
        report.write("[" + json.dumps(report_data) + "]")
        report.close()

if __name__ == "__main__":
    main()
