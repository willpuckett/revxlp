#!/usr/bin/env python

import os
import argparse
import sys

import ezdxf
from ezdxf.addons import Importer

def merge(source, target):
    importer = Importer(source, target)
    # import all entities from source modelspace into target modelspace
    importer.import_modelspace()
    # import all required resources and dependencies
    importer.finalize()

parser = argparse.ArgumentParser(prog='case-foam-dxf-merge')
parser.add_argument('version', choices=['10u', '12u'])

args = parser.parse_args(sys.argv[1:])

base_dxf = ezdxf.readfile(f'{args.version}/bottom/revxlp_bottom-Edge_Cuts.dxf')

for filename in [f'{args.version}/pcb/revxlp-User_Eco1.dxf']:
    merge_dxf = ezdxf.readfile(filename)
    merge(merge_dxf, base_dxf)

base_dxf.saveas(f'revxlp-{args.version}-case-foam.dxf')

