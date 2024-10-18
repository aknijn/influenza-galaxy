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
import subprocess
import json

clademap = {
    "HA|A|H1|Wisconsin|MW626062.1|A/Wisconsin/588/2019(H1N1)":"nextstrain/flu/h1n1pdm/ha/MW626062",
    "HA|A|H3|Darwin|EPI_ISL_1563628|A/Darwin/6/2021(H3N2)":"nextstrain/flu/h3n2/ha/EPI1857216",
    "HA|B|H_vic|Brisbane|KX058884.1|B/Brisbane/60/2008(B_vic)":"nextstrain/flu/vic/ha/KX058884",
    "HA|B|H_yam|Wisconsin|JN993010.1|B/Wisconsin/01/2010(B_yam)":"nextstrain/flu/yam/ha/JN993010",
    "HA|A|H5|Guangdong|AF144305.1|A/Goose/Guangdong/1/96(H5N1)":"community/moncla-lab/iav-h5/ha/all-clades",
    "HA|H5|2.3.2.1|EPI_ISL_136169|A/duck/Vietnam/NCVD-1584/2012|Jang,_Yunho(H5N1)":"community/moncla-lab/iav-h5/ha/2.3.2.1",
    "HA|A|H5|2.3.4.4|EPI_ISL_1038924|A/Astrakhan/3212/2020|Susloparov,_Ivan(H5N8)":"community/moncla-lab/iav-h5/ha/2.3.4.4"}

refmap = {
    "HA|A|H1|Wisconsin|MW626062.1|A/Wisconsin/588/2019(H1N1)":"MW626062.1",
    "HA|A|H3|Darwin|EPI_ISL_1563628|A/Darwin/6/2021(H3N2)":"EPI_ISL_1563628",
    "HA|B|H_vic|Brisbane|KX058884.1|B/Brisbane/60/2008(B_vic)":"KX058884.1",
    "HA|B|H_yam|Wisconsin|JN993010.1|B/Wisconsin/01/2010(B_yam)":"JN993010.1",
    "HA|A|H5|Guangdong|AF144305.1|A/Goose/Guangdong/1/96(H5N1)":"AF144305.1",
    "HA|H5|2.3.2.1|EPI_ISL_136169|A/duck/Vietnam/NCVD-1584/2012|Jang,_Yunho(H5N1)":"EPI_ISL_424984",
    "HA|A|H5|2.3.4.4|EPI_ISL_1038924|A/Astrakhan/3212/2020|Susloparov,_Ivan(H5N8)":"EPI_ISL_1846961"}

typemap = {
    "HA|A|H1|Wisconsin|MW626062.1|A/Wisconsin/588/2019(H1N1)":"A",
    "HA|A|H3|Darwin|EPI_ISL_1563628|A/Darwin/6/2021(H3N2)":"A",
    "HA|B|H_vic|Brisbane|KX058884.1|B/Brisbane/60/2008(B_vic)":"B",
    "HA|B|H_yam|Wisconsin|JN993010.1|B/Wisconsin/01/2010(B_yam)":"B",
    "HA|A|H5|Guangdong|AF144305.1|A/Goose/Guangdong/1/96(H5N1)":"A",
    "HA|H5|2.3.2.1|EPI_ISL_136169|A/duck/Vietnam/NCVD-1584/2012|Jang,_Yunho(H5N1)":"A",
    "HA|A|H5|2.3.4.4|EPI_ISL_1038924|A/Astrakhan/3212/2020|Susloparov,_Ivan(H5N8)":"A"}

subtypemap = {
    "HA|A|H1|Wisconsin|MW626062.1|A/Wisconsin/588/2019(H1N1)":"H1",
    "HA|A|H3|Darwin|EPI_ISL_1563628|A/Darwin/6/2021(H3N2)":"H3",
    "HA|B|H_vic|Brisbane|KX058884.1|B/Brisbane/60/2008(B_vic)":"H_vic",
    "HA|B|H_yam|Wisconsin|JN993010.1|B/Wisconsin/01/2010(B_yam)":"H_yam",
    "HA|A|H5|Guangdong|AF144305.1|A/Goose/Guangdong/1/96(H5N1)":"H5",
    "HA|H5|2.3.2.1|EPI_ISL_136169|A/duck/Vietnam/NCVD-1584/2012|Jang,_Yunho(H5N1)":"H5",
    "HA|A|H5|2.3.4.4|EPI_ISL_1038924|A/Astrakhan/3212/2020|Susloparov,_Ivan(H5N8)":"H5"}

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
  
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ha_consensus', dest='ha_consensus', help='ha consensus fasta')
    parser.add_argument('--clade', dest='clade', help='nextclade result')
    parser.add_argument('--clade_json', dest='clade_json', help='nextclade reference')
    args = parser.parse_args()

    matching_shortref = 'ND'
    matching_type = 'ND'
    matching_subtype = 'H'
    subprocess.run("blastn -query " + args.ha_consensus + " -db " + TOOL_DIR + "/data/HA_Flu -task blastn -evalue 0.001 -out blast_ha -outfmt '6 sseqid' -strand both -dust yes -max_target_seqs 1 -perc_identity 95.0", shell=True)
    if os.path.getsize('blast_ha') != 0:
        with open('blast_ha', 'r') as blast_file:
            matching_ref = next(blast_file).strip()
            matching_shortref = refmap.get(matching_ref)
            matching_type = typemap.get(matching_ref)
            matching_subtype = subtypemap.get(matching_ref)
            matching_dataset = clademap.get(matching_ref)
            subprocess.run("nextclade dataset get --name=" + matching_dataset + " --output-dir=data", shell=True)
            subprocess.run("nextclade run " + args.ha_consensus + " --input-dataset=data --output-tsv=" + args.clade + " --output-all=nextclade/", shell=True)

    try:
        report_data = {}
        # prepare JSON output file
        report_data["ha_reference"] = matching_shortref
        report_data["influenza_type"] = matching_type
        report_data["h_subtype"] = matching_subtype
    finally:
        report = open(args.clade_json, 'w')
        report.write(json.dumps(report_data))
        report.close()

if __name__ == "__main__":
    main()
