#!/usr/bin/env python

# Load CQGI
import cadquery.cqgi as cqgi
import cadquery as cq
import os
import argparse
import sys

parser = argparse.ArgumentParser(prog='plate-case-export')
parser.add_argument('--feature', '-f', action='append', choices=['base', 'logo', 'button_cutouts'])
parser.add_argument('version', choices=['10u', '12u'])

args = parser.parse_args(sys.argv[1:])

# load the cadquery script
model = cqgi.parse(open("plate-case.py").read())

opts = {
        'design_size': args.version,
        'assembly_generation': False,
        'feature_button_cutouts': (not args.feature or "button_cutouts" in args.feature),
        'feature_logo': (not args.feature or "logo" in args.feature),
}

# run the script and store the result (from the show_object call in the script)
build_result = model.build(build_parameters = opts)

# test to ensure the process worked.
if build_result.success:
    item = next(filter(lambda res: res.options['case'], build_result.results))

    base_name = f"revxlp_case_{args.version}_{'_'.join(args.feature or ['all'])}"
    cq.exporters.export(item.shape, f"{base_name}.step")
    cq.exporters.export(item.shape, f"{base_name}.stl")
else:
    print(f"BUILD FAILED: {build_result.exception}")
