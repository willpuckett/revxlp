# Load CQGI
import cadquery.cqgi as cqgi
import cadquery as cq

# load the cadquery script
model = cqgi.parse(open("plate-case.py").read())

# run the script and store the result (from the show_object call in the script)
build_result = model.build()

# test to ensure the process worked.
if build_result.success:
    # loop through all the shapes returned and export to STEP
    for i, result in enumerate(build_result.results):
        cq.exporters.export(result.shape, f"plate_case_{i}.step")
else:
    print(f"BUILD FAILED: {build_result.exception}")
