from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def block_end(text: str, start: int) -> int:
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i + 1
    raise RuntimeError("Unbalanced KiCad block")


def iter_blocks(text: str, starter: str):
    pos = 0
    while True:
        start = text.find(starter, pos)
        if start < 0:
            return
        end = block_end(text, start)
        yield start, end, text[start:end]
        pos = end


def pcb_ref_for_block(block: str):
    for pat in (
        r'\(property "Reference" "([^"]+)"',
        r'\(fp_text reference "([^"]+)"',
    ):
        m = re.search(pat, block)
        if m:
            return m.group(1)
    return None


def find_u602_block(text: str, path: Path):
    if path.suffix == ".kicad_sch":
        # In this KiCad schematic the placed symbols retain generic reference
        # properties and annotation is stored in the instance table. The 3V3
        # regulator U602 is the XL1509 symbol placed at x=201.93, y=128.27.
        candidates = []
        for start, end, block in iter_blocks(text, "(symbol "):
            if "XL1509-5.0E1" in block or "XL1509-3.3E1" in block:
                candidates.append((start, end, block))
                if "(at 201.93 128.27" in block:
                    return start, end, block
        raise RuntimeError(
            f"{path}: could not identify U602 at expected placement; "
            f"found {len(candidates)} XL1509 regulator symbols"
        )

    if path.suffix == ".kicad_pcb":
        candidates = []
        for start, end, block in iter_blocks(text, "(footprint "):
            if "XL1509-5.0E1" in block or "XL1509-3.3E1" in block:
                ref = pcb_ref_for_block(block)
                candidates.append((ref, start, end, block))
        for ref, start, end, block in candidates:
            if ref == "U602":
                return start, end, block
        refs = [r for r, *_ in candidates]
        raise RuntimeError(f"{path}: could not identify U602 regulator footprint; regulator refs={refs}")

    raise RuntimeError(f"Unsupported KiCad file: {path}")


def patch_u602(path: Path):
    text = path.read_text(encoding="utf-8")
    start, end, block = find_u602_block(text, path)

    if "XL1509-3.3E1" in block and '"C74193"' in block:
        print(f"{path}: U602 already corrected")
        return False

    if "XL1509-5.0E1" not in block:
        raise RuntimeError(f"{path}: U602 does not contain expected XL1509-5.0E1 metadata")

    block2 = block.replace("XL1509-5.0E1", "XL1509-3.3E1")
    block2 = block2.replace("XL1509-5-0E1_C61063.pdf", "XL1509-3-3E1_C74193.html")
    block2 = block2.replace('"C61063"', '"C74193"')
    block2 = re.sub(
        r'\(property "Datasheet" "[^"]*"',
        '(property "Datasheet" "https://www.lcsc.com/product-detail/C74193.html"',
        block2,
        count=1,
    )

    if block2 == block:
        raise RuntimeError(f"{path}: no U602 changes produced")

    path.write_text(text[:start] + block2 + text[end:], encoding="utf-8")
    print(f"{path}: corrected U602 to XL1509-3.3E1 / LCSC C74193")
    return True


def main():
    changed = False
    for rel in (
        "ayab-esp32/psu.kicad_sch",
        "ayab-esp32/ayab-esp32.kicad_pcb",
    ):
        changed |= patch_u602(ROOT / rel)
    if not changed:
        print("No changes required")


if __name__ == "__main__":
    main()
