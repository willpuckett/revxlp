#!/usr/bin/env python

# Load CQGI
import cadquery.cqgi as cqgi
import cadquery as cq
import os
import argparse
import sys

parser = argparse.ArgumentParser(prog='plate-case-export')
parser.add_argument('--feature', '-f', action='append', choices=['logo', 'button_cutouts'])

args = parser.parse_args(sys.argv[1:])

# load the cadquery script
model = cqgi.parse(open("plate-case.py").read())

opts = {
        'feature_button_cutouts': (not args.feature or "button_cutouts" in args.feature),
        'feature_logo': (not args.feature or "logo" in args.feature),
}

# run the script and store the result (from the show_object call in the script)
build_result = model.build(build_parameters = opts)

# test to ensure the process worked.
if build_result.success:
    *others,last = build_result.results

    base_name = f"revxlp_case_{'_'.join(args.feature or ['all'])}"
    cq.exporters.export(last.shape, f"{base_name}.step")
    cq.exporters.export(last.shape, f"{base_name}.stl")
else:
    print(f"BUILD FAILED: {build_result.exception}")
