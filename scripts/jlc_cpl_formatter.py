import sys
import re

import pandas as pd

def reduce_layer(layername):
    layername = str(layername).strip().lower()
    if 'top' in layername or layername == 't':
        return 'T'
    elif 'bottom' in layername or layername == 'b':
        return 'B'
    else:
        return ''


def normalize_cpl(cpl_file):
    cpl_file.columns = [str(column).strip().lstrip("\ufeff") for column in cpl_file.columns]
    cpl_file = cpl_file.rename(columns={
        "Ref": "Designator",
        "PosX": "Mid X",
        "PosY": "Mid Y",
        "Side": "Layer",
        "Rot": "Rotation",
    })

    required = ["Designator", "Mid X", "Mid Y", "Layer", "Rotation"]
    if not set(required).issubset(cpl_file.columns):
        if cpl_file.shape[1] != 7:
            raise ValueError(
                "Unrecognized CPL columns; expected named KiCad fields or "
                "a legacy seven-column AYAB export: "
                + ", ".join(cpl_file.columns)
            )
        cpl_file.columns = ['Designator', 'Val', 'Package', 'Mid X', 'Mid Y', 'Rotation', 'Layer']

    # KiCad versions may append a comment footer.  Remove only actual footer or
    # blank rows; never discard the last component unconditionally.
    designators = cpl_file['Designator'].astype(str).str.strip()
    cpl_file = cpl_file[designators.ne('') & ~designators.str.startswith('#')].copy()
    cpl_file['Layer'] = cpl_file['Layer'].apply(reduce_layer)
    return cpl_file.reindex(columns=required)


def reconcile_to_bom(cpl_file, bom_file):
    bom_file.columns = [str(column).strip().lstrip("\ufeff") for column in bom_file.columns]
    designator_column = next(
        (name for name in ("Designator", "Reference", "References") if name in bom_file.columns),
        None,
    )
    if designator_column is None:
        raise ValueError("BOM has no Designator or Reference column")

    bom_designators = {
        reference
        for group in bom_file[designator_column].astype(str)
        for reference in re.split(r"[,;\s]+", group.strip())
        if reference
    }
    cpl_designators = set(cpl_file["Designator"])
    missing = sorted(bom_designators - cpl_designators)
    if missing:
        raise ValueError(f"BOM references missing from CPL: {missing}")

    return cpl_file[cpl_file["Designator"].isin(bom_designators)].copy()


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        raise SystemExit("usage: jlc_cpl_formatter.py INPUT.csv OUTPUT.csv [BOM.csv]")
    cpl_file = pd.read_csv(sys.argv[1], dtype=str, keep_default_na=False)
    result = normalize_cpl(cpl_file)
    if len(sys.argv) == 4:
        bom_file = pd.read_csv(sys.argv[3], dtype=str, keep_default_na=False)
        result = reconcile_to_bom(result, bom_file)
    result.to_csv(sys.argv[2], index=False)
