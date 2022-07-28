import cadquery as cq
import os
import re
import csv

file_dir = os.environ.get("REVXLP_DIR") or os.getcwd()

plate_thickness = 2
pcb_wiggle_room = 0.25

pcb_thickness = 1.8
bottom_component_gap = 2
pcb_to_switch_plate_gap = 1
switch_plate_thickness = 1.2

interior_height = (
    bottom_component_gap +
    pcb_thickness +
    pcb_to_switch_plate_gap +
    switch_plate_thickness
)

screw_hole_diameter = 3.2

bottom_logo_depth = 0.5

# Possible optional features
feature_logo = True

feature_button_cutouts = True

feature_bottom_chamfer = False
chamfer_size = 1

feature_bottom_fillet = True
fillet_size = 1

def pnp_locations():
    with open(f"{file_dir}/pcb/revxlp_cpl_jlc.csv") as file:
        reader = csv.DictReader(file)
        return dict([(x['Designator'],x) for x in reader])
        
def drill_points():
    file = open(f"{file_dir}/bottom/JLCPCB/revxlp_bottom-NPTH.drl", 'r')
    regex = re.compile("^X(-?\d+.\d+)Y(-?\d+.\d+)")
    return [(float(m.group(1)), float(m.group(2))) for l in file.readlines() for m in [regex.search(l)] if m]

def edge_cut_sketch():
    return 

def edge_cuts():
    return (
        cq.importers.importDXF(f"{file_dir}/bottom/revxlp_bottom-Edge_Cuts.dxf", tol=0.05)
        .wires()
        .toPending()
    )

def logo_dxf():
    return (
        cq.importers.importDXF(f"{file_dir}/lpg-planet-logo.dxf", tol=0.01)
        .wires()
        .toPending()
    )


def logo_text_dxf():
    return (
        cq.importers.importDXF(f"{file_dir}/lpg-planet-logo-text.dxf", tol=0.01)
        .wires()
        .toPending()
    )
    
core_body = edge_cuts().offset2D(plate_thickness + pcb_wiggle_room, 'intersection').extrude(interior_height + plate_thickness)

hulled_body = core_body.cut(edge_cuts().offset2D(pcb_wiggle_room).extrude(interior_height).translate([0,0,plate_thickness]))

body = hulled_body

if feature_bottom_chamfer:
    body = body.faces("<Z").chamfer(chamfer_size)
elif feature_bottom_fillet:
    body = body.faces("<Z").fillet(fillet_size)

# Only drills from the bottom PCB design are for the screw holes, so use those to drill out screw hole spots as well
body = body.faces("<Z").pushPoints(drill_points()).circle(screw_hole_diameter / 2).cutThruAll()

if feature_button_cutouts:
    # Use the pick and place file generated by KiBot to find the locations of the two switches
    # We need holes in the case to reach.
    pnp = pnp_locations()
    
    reset_btn = pnp['SW2']
    reset_btn_point = (float(reset_btn['Mid X']), float(reset_btn['Mid Y']))
    
    power_switch = pnp['SW1']
    power_point = (float(power_switch['Mid X']), float(power_switch['Mid Y']))
    
    # Face selection is a bit fiddly, we need *almost* the farthest face w/ a positive Y normal.
    body = body.faces(">Y[-2]").workplane().pushPoints([(reset_btn_point[0],plate_thickness + bottom_component_gap), (power_point[0],plate_thickness + bottom_component_gap)]).rect(6,4).cutThruAll(True, -45)

if feature_logo:
    bottom_center = body.faces("<Z").val().Center()
    
    logo = logo_dxf().extrude(bottom_logo_depth).translate(bottom_center)
    logo_text = logo_text_dxf().extrude(bottom_logo_depth).translate(bottom_center)
    
    body = body.faces("<Z").cut(logo).cut(logo_text)

show_object(body)
