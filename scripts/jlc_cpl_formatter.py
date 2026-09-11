import sys

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


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: jlc_cpl_formatter.py INPUT.csv OUTPUT.csv")
    cpl_file = pd.read_csv(sys.argv[1], dtype=str, keep_default_na=False)
    normalize_cpl(cpl_file).to_csv(sys.argv[2], index=False)
