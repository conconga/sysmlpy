#!/usr/bin/env python3
"""PoC: SysML v2 action flow rendered through sysmlpy's diagramboxes
adapter (boxes_view.as_action_flow_view_boxes) with the v2-native
glyphs (diagramboxes v0.15.x): chamfered action-usage octagons and the
solid start diamond — the same notation as the Intro deck's
'providePower' Action Flow example (reproduced directly at trace
coordinates in sysml-v2-repro, accepted 10/10).

The model text is this repo's own approximation of the deck's example:
an action def providePower containing the five action usages, a
succession chain (start -> trigger1 -> generateTorque -> ... ->
transferTorque) and flows between the action outputs/inputs.

Renders:
  figv2_actionflow.txt — terminal braille
  figv2_actionflow.svg — SVG (converted to .png by inkscape)
under /home/jfox/proj/sysml-distilled/reproduced/.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from sysmlpy.boxes_view import (            # noqa: E402
    as_action_flow_view_boxes,
    render_action_flow_view_boxes,
    render_action_flow_view_boxes_svg,
)

OUT_DIR = "/home/jfox/proj/sysml-distilled/reproduced"

MODEL = """
package EngineAssembly {
    item def Torque;
    item def EngineStartSignal;
    action def generateTorque { in item demand; out item torque : Torque; }
    action def amplifyTorque { in item torqueIn : Torque; out item torqueOut : Torque; }
    action def distributeTorque { in item torqueIn : Torque; out item torqueOut : Torque; }
    action def transferTorque { in item torqueIn : Torque; }
    action def triggerAction { out item es : EngineStartSignal; }
    action def providePower {
        action generateTorque;
        action amplifyTorque;
        action distributeTorque;
        action transferTorque;
        action trigger1;
        connect trigger1 to amplifyTorque;
        succession s1 first start then trigger1;
        succession s2 first generateTorque then amplifyTorque;
        succession s3 first amplifyTorque then distributeTorque;
        succession s4 first distributeTorque then transferTorque;
    }
}
"""


def main():
    d = as_action_flow_view_boxes(MODEL)
    txt = render_action_flow_view_boxes(MODEL)
    svg = render_action_flow_view_boxes_svg(MODEL)
    with open(os.path.join(OUT_DIR, "figv2_actionflow.txt"), "w") as fp:
        fp.write(txt)
    with open(os.path.join(OUT_DIR, "figv2_actionflow.svg"), "w") as fp:
        fp.write(svg)
    subprocess.run(
        ["inkscape",
         os.path.join(OUT_DIR, "figv2_actionflow.svg"),
         "--export-type=png",
         "--export-filename=" + os.path.join(OUT_DIR, "figv2_actionflow.png"),
         "-w", "1200"],
        check=False,
    )
    print("nodes:", len(d.nodes), "octagons:",
          len([n for n in d.nodes if getattr(n, "chamfer", 0)]),
          "diamonds:", len([a for a in d.activities
                            if getattr(a, "filled", False)]))


main()