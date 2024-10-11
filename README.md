# Revxlp var_rename demo

This repository is a *demonstration* of footprint replacement/ production variants. 

The [original repo](https://gitlab.com/lpgalaxy/revxlp) has a 10u and 12u directory, both of which have the pcb, top, and bottom plates.

Using KiBot's footprint replacement, the 6 kicad files have been consolidated to one. Footprints are switched via the Schematic Editor's `Tools > Edit Symbol Field...`.

The variants are defined in [`revxlp.kibot.yaml`](12u/pcb/revxlp.kibot.yaml). You can run the outputs by cd'ing into [`12u/pcb`](/12u/pcb) and `./output_variants.sh` while in the devcontainer.

There are still caveats. Global deletion on vias and tracks will be necessary, and the kibot zone refill pre_flight doesn't seem to be executing on the variants. This repo was made as a concept demonstration: no work was done to ensure switched footprints have a common origin. *Not recommended for production.*

Sample outputs are in [`12u/pcb/variants`](/12u/pcb/variants).