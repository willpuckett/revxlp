#!/usr/bin/env python

import ezdxf
from ezdxf.addons import Importer

def merge(source, target):
    importer = Importer(source, target)
    # import all entities from source modelspace into target modelspace
    importer.import_modelspace()
    # import all required resources and dependencies
    importer.finalize()

base_dxf = ezdxf.readfile('bottom/revxlp_bottom-Edge_Cuts.dxf')

for filename in ['pcb/revxlp-User_Eco1.dxf']:
    merge_dxf = ezdxf.readfile(filename)
    merge(merge_dxf, base_dxf)

base_dxf.saveas('revxlp-case-foam.dxf')

