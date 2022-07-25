
# revxlp Overview

![revxlp](revxlp.jpg)

The revxlp is a 41/42 key low profile (choc v1), unibody split, keyboard, supporting hotswap sockets, two thumb layouts, and single color backlight per-key LEDs. It is a remix of the amazing [revlp](https://github.com/cyril279/keyboards/tree/main/revlp) by Cyril, who created it off the original [reviung41](https://github.com/gtips/reviung/tree/master/reviung41) by gtips.

## Layouts

The revxlp PCB supports 41 or 42 key layouts, with either a single 2u middle thumb, or dual 1u thumb keys.

## Backlighting

Single color LED backlighting is supported. It does *NOT* support per-key RGB. If building yourself, choose the color PLL-2 LED you want to use, and calculate the desired resistor value based on the LED forward voltage and cucurrent.

A jumper on the back of the PCB needs to be jumped, depending on if you want to power the LEDs from the raw 5v from USB, or the regulated 3.3v power source. For a build using the XIAO BLE, you might want to consider, this carefully; bridging to the 5v source means the LEDs will automatically be cut from power when USB is unplugged. If using 3.3v, you will likely deplete the tiny LiPo battery quickly w/ LEDs on *anyways*.

## Controllers

The revxlp is designed to use any controller designed to be Seeed Studio XIAO compatible. The two major families of controllers are the XIAO controllers from Seeed Studio, and the Adafruit Qt PY controllers.

The current list of controllers, and their support status is as follows:

| Controller              | Chip     | Features             | Status                                                         |
| ----------------------- | -------- | -------------------- | -------------------------------------------------------------- |
| XIAO                    | samd21   | USB                  | Supported                                                      |
| Adafruit Qt PY          | samd21   | USB                  | Supported                                                      |
| XIAO BLE                | nRF52840 | USB,BLE,LiPo Battery | Supported                                                      |
| XIAO RP2040             | nRF52840 | USB                  | [Experimental](https://github.com/zmkfirmware/zmk/issues/1085) |
| Adafruit Qt PY RP2040   | nRF52840 | USB                  | [Experimental](https://github.com/zmkfirmware/zmk/issues/1085) |
| XIAO ESP32-C3           | ESP32-C3 | USB,BLE,LiPo Battery | Not Yet Supported                                              |
| Adafruit Qt PY ESP32-C3 | ESP32-C3 | USB,BLE,LiPo Battery | Not Yet Supported                                              |

The ESP32-C3 based controllers will likely be supported in the future, as Zephyr/ZMK support for
that chip is completed.

## Bill Of Materials (BOM)

The BOM for the revxlp is as follows:

| Description                | Count | Footprint | Value/MPN                            | Sources                                                                                                                                                                                         |
| -------------------------- | ----- | --------- | ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| XIAO Compatible Controller | 1     | XIAO      | e.g. XIAO BLE, XIAO, XIAO RP2040     | TODO                                                                                                                                                                                            |
| Shift Register             | 1     | SOIC-16   | SN74HC595 (e.g. SN74HC595D* from TI) | [Octopart](https://octopart.com/search?q=SN74HC595&currency=USD&specs=0) - Note, avoid DW* packages, as those are *wide* SOIC-16.                                                               |
| Controller Sockets         | 2     |           | Mill Max 310-43-107-41-001000        | [Octopart](https://octopart.com/search?q=310-43-107-41-001000&currency=USD&specs=0)                                                                                                             |
| Reset/Battery Pogo Pins    | 2     |           | Mill Max 0906-2-15-20-75-14-11-0     | [Octopart](https://octopart.com/search?q=0906-2-15-20-75-14-11-0&currency=USD&specs=0)                                                                                                          |
| Kailh Choc Hotswap Sockets | 43    |           | CPG135001S30                         | [MKUltra](https://mkultra.click/kailh-hotswap-sockets)/[BoardSource](https://boardsource.xyz/store/5eca381464caf04f83aa6482)/[mb](https://mechboards.co.uk/products/kailh-choc-hotswap-sockets) |
| Kailh Choc v1 Switches     | 41/42 | N/A       | PG1350                               | TODO                                                                                                                                                                                            |
| Reset Button               | 1     |           | Alps SKSN                            | TODO                                                                                                                                                                                            |
| Power Switch               | 1     |           | PCM12                                | TODO                                                                                                                                                                                            |
| JST Socket                 | 1     |           | SM02B-SRSS-TB(LF)(SN)                | TODO                                                                                                                                                                                            |
| Battery                    | 1     | 350820    | 40mAh                                | https://tinycircuits.com/collections/batteries/products/lithium-ion-polymer-battery-3-7v-40mah                                                                                                  |
| Backlight MOSFET           | 1     | SOT-23    | AO3416                               | TODO                                                                                                                                                                                            |
| Backlight MOSFET Resistor  | 1     | 1206      | 4.7k Ω                               | TODO                                                                                                                                                                                            |
| Backlight LEDS             | 42    | PLL-2     | User selected color                  | TODO                                                                                                                                                                                            |
| Backlight Resistors        | 42    | 1206      | See Backlighting calculator docs     | TODO                                                                                                                                                                                            |
| Case Standoff Solder Nuts  | 7     |           | Adafruit M3 x 3mm Solder Nuts        | TODO                                                                                                                                                                                            |
| Case Screws                | 7     |           | M3 x 6mm                             | TODO                                                                                                                                                                                            |

# Production Files

The following files are available as open source hardware (OSH) for folks to produce. They are all released unde the MIT license, like the originals they are based on.

If you get any of these made, and are financially able to, please consider sponsoring me using the "Open Source Hardware Love" one-time tier on my [GitHub Sponsorship Page](https://github.com/sponsors/petejohanson).

## PCB

revxlp PCBs can be made at any of the common services, e.g. [JLC](https://jlcpcb.com/), [AllPCB](https://www.allpcb.com/), etc.

When ordering, you'll want to use the following details:

* Width: 239mm
* Height: 95mm
* Thickness: 1.6mm

You'll need the following download:

* [revxlp PCB Gerbers](https://gitlab.com/lpgalaxy/revxlp/-/jobs/artifacts/main/raw/pcb/JLCPCB/revxlp-JLCPCB.zip?job=export-pcb)

## Switch Plate

The switch plate is exported two ways, one to be used for for JLC's Aluminum PCBs, which are single sided silk, and the other for standard FR4 plates. When ordering either, be sure to use the following details:

* Width: 239mm
* Height: 95mm
* Thickness: 1.2mm

You can download either

* [Aluminum Switch Plate Gerbers](https://gitlab.com/lpgalaxy/revxlp/-/jobs/artifacts/main/raw/plate/JLCPCB/revxlp_plate-JLCPCB_Alu.zip?job=export-switch-plate)
* [FR4 Switch Plate Gerbers](https://gitlab.com/lpgalaxy/revxlp/-/jobs/artifacts/main/raw/plate/JLCPCB/revxlp_plate-JLCPCB_FR4.zip?job=export-switch-plate)

## Bottom Plate

The bottom plate can also be ordered in Aluminum or FR4. When ordering, use the following details:

* Width: 239mm
* Height: 95mm
* Thickness: 1.2mm

You can download either

* [Aluminum Switch Plate Gerbers](https://gitlab.com/lpgalaxy/revxlp/-/jobs/artifacts/main/raw/plate/JLCPCB/revxlp_plate-JLCPCB_Alu.zip?job=export-bottom-plate)
* [FR4 Switch Plate Gerbers](https://gitlab.com/lpgalaxy/revxlp/-/jobs/artifacts/main/raw/plate/JLCPCB/revxlp_plate-JLCPCB_FR4.zip?job=export-bottom-plate)

## 3DP Bottom Case

The 3DP bottom case is designed to work with the switch plate, and has a few optional features you can choose to include for the generate case:

* Button cutouts - Cutouts are added along the top edge to access the power switch and reset buttons. If you don't need either, build the `logo` or `none` variants.
* Logo - The Low Pro Galaxy, LLC logo is added as an inset on the bottom of the case. This should only be used if printing with something like resin. To skip the logo, use the `button_cutout` or `none` variants.
 
Cases can be printed yourself, or ordered through an online service, including JLC if also getting PCBs/plates ordered. They are generated using CadQuery, and are available as STEP or STL files.

* `all` variant, includes logo and button cutouts: [STEP](https://gitlab.com/lpgalaxy/revxlp/-/jobs/artifacts/main/raw/revxlp_case_all.step?job=generate-3dp-case)/[STL](https://gitlab.com/lpgalaxy/revxlp/-/jobs/artifacts/main/raw/revxlp_case_all.stl?job=generate-3dp-case)
* `logo` variant, includes logo, but *NO* button cutouts: [STEP](https://gitlab.com/lpgalaxy/revxlp/-/jobs/artifacts/main/raw/revxlp_case_logo.step?job=generate-3dp-case)/[STL](https://gitlab.com/lpgalaxy/revxlp/-/jobs/artifacts/main/raw/revxlp_case_logo.stl?job=generate-3dp-case)
* `button_cutouts` variant, includes button cutouts, but *NO* logo: [STEP](https://gitlab.com/lpgalaxy/revxlp/-/jobs/artifacts/main/raw/revxlp_case_button_cutouts.step?job=generate-3dp-case)/[STL](https://gitlab.com/lpgalaxy/revxlp/-/jobs/artifacts/main/raw/revxlp_case_button_cutouts.stl?job=generate-3dp-case)
* `base` variant, *NO* button cutouts, nor logo: [STEP](https://gitlab.com/lpgalaxy/revxlp/-/jobs/artifacts/main/raw/revxlp_case_base.step?job=generate-3dp-case)/[STL](https://gitlab.com/lpgalaxy/revxlp/-/jobs/artifacts/main/raw/revxlp_case_base.stl?job=generate-3dp-case)

# Build Guide

TODO!
