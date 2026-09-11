#!/usr/bin/env python3
"""Close the remaining KiCad-native PCB/schematic association warnings.

This changes footprint association metadata and explicit no-connect net names.
It does not add, remove, or reroute copper.
"""

from pathlib import Path

import pcbnew


PCB = Path(__file__).resolve().parents[1] / "ayab-esp32.kicad_pcb"


def main() -> None:
    board = pcbnew.LoadBoard(str(PCB))
    by_ref = {fp.GetReference(): fp for fp in board.GetFootprints()}

    for ref in ("D205", "D206"):
        by_ref[ref].SetSheetname("ESP32")
        by_ref[ref].SetSheetfile("mcu.kicad_sch")

    # These are connector-pin probes, not the separate TP601/TP602 rail probes.
    by_ref["TP401"].SetValue("9")
    by_ref["TP402"].SetValue("10")

    # Retained, independent J702/U701 level-shifter channels are unnamed in
    # the cleaned schematic; use KiCad's canonical generated net names.
    for old_name, new_name in {
        "/IO CONDITIONING/EOL_L_K": "Net-(J702-Pin_4)",
        "/IO CONDITIONING/EOL_L_L": "Net-(J702-Pin_5)",
        "/ESP32/ESP14": "/ESP32/FRONT_PANEL_AUX",
        "/ESP32/ESP39": "/ESP32/PANEL_INT",
        "Net-(U201-SPIIO7{slash}GPIO36{slash}FSPICLK{slash}SUBSPICLK)": "/ESP32/USER_BUTTON",
    }.items():
        net = board.FindNet(old_name)
        if net is not None:
            net.SetNetname(new_name)

    intentional_nc = {
        ("U201", "7"): "unconnected-(U201-GPIO3{slash}TOUCH3{slash}ADC1_CH2-Pad7)",
        ("U403", "4"): "unconnected-(U403-N{slash}C-Pad4)",
    }
    nets = {net.GetNetname(): net for net in board.GetNetInfo().NetsByName().values()}
    for (ref, pad_number), net_name in intentional_nc.items():
        net = nets.get(net_name)
        if net is None:
            net = pcbnew.NETINFO_ITEM(board, net_name)
            board.Add(net)
            nets[net_name] = net
        pad = by_ref[ref].FindPadByNumber(pad_number)
        if pad is None:
            raise RuntimeError(f"missing {ref}.{pad_number}")
        pad.SetNet(net)

    pcbnew.SaveBoard(str(PCB), board)
    print("NATIVE_PARITY_ASSOCIATIONS_OK")


if __name__ == "__main__":
    main()
