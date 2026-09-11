import sys

import pandas as pd

def footprintFix(fpName):
    propertiesList = fpName.split('_')

    if len(propertiesList) == 4:
        if  any(rcl in propertiesList[0] for rcl in ["Resistor", "Capacitor", "Inductor", "Diode"]):
            # For things like R/C/L, return something like C0402
            return propertiesList[1][-1] + propertiesList[2]

    # Strip out library name from FP.
    return fpName.split(":")[-1]


def normalize_bom(bom_file):
    """Return the four header-driven columns expected by JLCPCB.

    Current KiCad jobsets emit ten named columns.  Older AYAB exports used
    four, five, or six positional columns, so retain that compatibility while
    refusing ambiguous input instead of silently shifting fields.
    """
    bom_file.columns = [str(column).strip().lstrip("\ufeff") for column in bom_file.columns]

    aliases = {
        "Reference": "Designator",
        "References": "Designator",
        "Value": "Comment",
        "Package": "Footprint",
        "LCSC ID": "LCSC Part #",
        "LCSC PN": "LCSC Part #",
        "JLCPCB Part #": "LCSC Part #",
    }
    bom_file = bom_file.rename(columns=aliases)

    required = {"Designator", "Comment", "Footprint"}
    if not required.issubset(bom_file.columns):
        legacy_width = bom_file.shape[1]
        legacy_columns = {
            4: ["Designator", "Comment", "Footprint", "LCSC Part #"],
            5: ["Designator", "Comment", "Footprint", "Mfg", "Mfg P/N"],
            6: ["Designator", "Comment", "Footprint", "Mfg", "Mfg P/N", "LCSC Part #"],
        }
        if legacy_width not in legacy_columns:
            raise ValueError(
                "Unrecognized BOM columns; expected named KiCad fields or "
                "a legacy 4-, 5-, or 6-column AYAB export: "
                + ", ".join(bom_file.columns)
            )
        bom_file.columns = legacy_columns[legacy_width]

    if "LCSC Part #" not in bom_file.columns:
        bom_file["LCSC Part #"] = ""

    result = bom_file[["Comment", "Designator", "Footprint", "LCSC Part #"]].copy()
    result["Footprint"] = result["Footprint"].apply(footprintFix)
    return result


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: jlc_bom_formatter.py INPUT.csv OUTPUT.csv")

    bom_file = pd.read_csv(sys.argv[1], dtype=str, keep_default_na=False)
    normalize_bom(bom_file).to_csv(sys.argv[2], index=False)


if __name__ == "__main__":
    main()
