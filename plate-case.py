import cadquery as cq
import os
import re
import csv

file_dir = os.environ.get("REVXLP_DIR") or os.getcwd()

design_size = '10u'

assembly_generation = True

plate_thickness = 2
pcb_wiggle_room = 0.25

pcb_thickness = 1.6
solder_nut_height = 2
pcb_to_switch_plate_gap = 1
switch_plate_thickness = 1.2
height_buffer = 0.0

interior_height = (
    solder_nut_height +
    pcb_thickness +
    pcb_to_switch_plate_gap +
    switch_plate_thickness +
    height_buffer
)

screw_hole_diameter = 3

bottom_logo_depth = 0.5

# For 3M SJ5382
bumpon_width = 6.4

# Possible optional features
feature_logo = True

screw_hole_type = 'csk'

feature_button_cutouts = True

feature_chamfer_outside = False
feature_fillet_outside = True

feature_chamfer_inside = False
feature_fillet_inside = True

feature_bumpon_insets = True

def generate_solder_nut(height):
    main = cq.Workplane("XY").circle(4.56/2).extrude(height)
    with_nub = main.faces(">Z").circle(3.9/2).extrude(1.53)
    nut = with_nub.faces(">Z").hole(diameter=2)
    
    nut.faces("<Z").tag("bottom")
    nut.faces(">Z[-2]").tag("rim")
    return nut

def pcb_step():
    return cq.importers.importStep(f'{file_dir}/{design_size}/pcb/revxlp-3D.step')

def plate_pcb_step():
    return cq.importers.importStep(f'{file_dir}/{design_size}/plate/revxlp_plate-3D.step')

def pnp_locations():
    with open(f"{file_dir}/{design_size}/pcb/revxlp_cpl_jlc.csv") as file:
        reader = csv.DictReader(file)
        return dict([(x['Designator'],x) for x in reader])

def bottom_pnp_locations():
    with open(f"{file_dir}/{design_size}/bottom/revxlp_bottom_cpl_jlc.csv") as file:
        reader = csv.DictReader(file)
        return dict([(x['Designator'],x) for x in reader])

def drill_points():
    file = open(f"{file_dir}/{design_size}/bottom/JLCPCB/revxlp_bottom-NPTH.drl", 'r')
    regex = re.compile("^X(-?\d+.\d+)Y(-?\d+.\d+)")
    return [(float(m.group(1)), float(m.group(2))) for l in file.readlines() for m in [regex.search(l)] if m]

def edge_cut_sketch():
    return 

def edge_cuts():
    return (
        cq.importers.importDXF(f"{file_dir}/{design_size}/bottom/revxlp_bottom-Edge_Cuts.dxf", tol=0.05)
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

if feature_chamfer_outside:
    core_body = core_body.faces("<Z or >Z").chamfer(plate_thickness)
elif feature_fillet_outside:
    core_body = core_body.faces("<Z or > Z").fillet(plate_thickness)

huller = edge_cuts().offset2D(pcb_wiggle_room).extrude(interior_height + 1).translate([0,0,plate_thickness])
body = core_body.cut(huller)

if feature_chamfer_inside:
    body = body.faces(">Z[-2]").chamfer(plate_thickness * 0.5)
elif feature_fillet_inside:
    body = body.faces(">Z[-2]").fillet(plate_thickness * 0.5)

body.faces(">Z[-2]").tag("interior_bottom")

if feature_bumpon_insets:
    locs = bottom_pnp_locations().values()
    bumpons = [(float(val['Mid X']), float(val['Mid Y'])) for val in bottom_pnp_locations().values() if val['Package'] == 'Bumpon']

    bumpon_bodies = cq.Workplane("XY").pushPoints(bumpons).circle((bumpon_width * 1.1)/2).extrude(1)
    body = body.cut(bumpon_bodies)

drill_prep = body.faces("<Z").workplane().pushPoints(map(lambda p: (p[0], -p[1]), drill_points()))
if screw_hole_type == 'cbore':
    body = drill_prep.cboreHole(screw_hole_diameter, screw_hole_diameter * 2, 1, None, True)
elif screw_hole_type == 'csk':
    body = drill_prep.cskHole(screw_hole_diameter, screw_hole_diameter * 1.5, 90, None, True)
else:
    body = drill_prep.hole(screw_hole_diameter, None, True)

if feature_button_cutouts:
    # Use the pick and place file generated by KiBot to find the locations of the two switches
    # We need holes in the case to reach.
    pnp = pnp_locations()
    
    reset_btn = pnp['SW2']
    reset_btn_point = (float(reset_btn['Mid X']), float(reset_btn['Mid Y']))
    
    power_switch = pnp['SW1']
    power_point = (float(power_switch['Mid X']), float(power_switch['Mid Y']))
    
    # Face selection is a bit fiddly, we need *almost* the farthest face w/ a positive Y normal.
    faces = body.faces(">Y[-2]")
    
    body = (
        faces.workplane()
        .pushPoints([(reset_btn_point[0], plate_thickness + solder_nut_height/2), (power_point[0], plate_thickness + solder_nut_height/2)]).rect(8,solder_nut_height)
        .cutThruAll(True, -45)
    )

if feature_logo:
    bottom_center = body.faces("<Z").val().Center()
    
    logo = logo_dxf().extrude(bottom_logo_depth).translate(bottom_center)
    logo_text = logo_text_dxf().extrude(bottom_logo_depth).translate(bottom_center)
    
    body = body.faces("<Z").cut(logo).cut(logo_text)

show_object(body, options={ 'case': True })

if assembly_generation:
    nut_points = drill_points()
    pcb = pcb_step()
    
    pcb.faces(">Z[-2]").tag("bottom_surface")
    pcb.faces(">Z[-1]").edges(">Y").tag("top_face_bottom_edge")
    
    for idx, (x,y) in enumerate(nut_points):
        pcb.faces(">Z[-2]").edges(cq.NearestToPointSelector((x,y,0))).tag(f"mounting_hole{idx}")
    
    plate = plate_pcb_step()
    plate.faces("<Z").edges("<Y").tag("bottom_edge")
    
    assy = (
        cq.Assembly()
        .add(body, name="case")
        .add(pcb, name="pcb", color=cq.Color("black"), loc=cq.Location(cq.Vector(0,0,0), cq.Vector(0,0,2), 0))
        .add(plate, name="plate", color=cq.Color("white"), loc=cq.Location(cq.Vector(0,0,0), cq.Vector(0,0,2), 0))
    )
    
    for idx, (x,y) in enumerate(nut_points):
        assy = assy.add(generate_solder_nut(solder_nut_height), name=f"nut{idx}", color=cq.Color("blue"), loc=cq.Location(cq.Vector(x,y, 0), cq.Vector(1,0,0), 0))
    
    # Fix our case in place
    assy.constrain("case", "Fixed")
    
    for idx in range(len(nut_points)):
        # Ensure every nut is fixed at the bottom to the case, and at the top rim, in it's matching mounting hole
        assy.constrain(f"nut{idx}?bottom", "case?interior_bottom", "PointInPlane")
        assy.constrain(f"nut{idx}?bottom", "case?interior_bottom", "Axis")
        assy.constrain(f"nut{idx}?rim", f"pcb?mounting_hole{idx}", "Point")
        assy.constrain(f"nut{idx}?rim", "pcb?bottom_surface", "PointInPlane")
        assy.constrain(f"nut{idx}?rim", "pcb?bottom_surface", "Axis")
    
    # Ensure our plate and PCB are aligned on the axis
    assy.constrain("plate@faces@<Z", "pcb@faces@>Z[-1]", "Axis")
    
    # Line up the plate and PCB by using their common bottom edge for alignment, with the 1mm spacing between plate and PCB w/ choc v1.
    assy.constrain("plate?bottom_edge", "pcb?top_face_bottom_edge", "PointInPlane", param=pcb_to_switch_plate_gap)
    
    assy.solve()
    
    show_object(assy, options = { 'full_assembly': True })
