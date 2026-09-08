from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def enclosing_block(text: str, needle: str, starters=("(symbol ", "(footprint ")):
    pos = text.find(needle)
    if pos < 0:
        raise RuntimeError(f"Could not find {needle!r}")

    candidates = []
    for starter in starters:
        i = text.rfind(starter, 0, pos)
        while i >= 0:
            depth = 0
            in_string = False
            escape = False
            end = None
            for j in range(i, len(text)):
                ch = text[j]
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
                        end = j + 1
                        break
            if end is not None and i <= pos < end:
                candidates.append((end - i, i, end))
                break
            i = text.rfind(starter, 0, i)
    if not candidates:
        raise RuntimeError(f"Could not find enclosing KiCad block for {needle!r}")
    _, start, end = min(candidates)
    return start, end


def patch_u602(path: Path):
    text = path.read_text(encoding="utf-8")
    start, end = enclosing_block(text, '(property "Reference" "U602"')
    block = text[start:end]

    if "XL1509-3.3E1" in block and '"C74193"' in block:
        print(f"{path}: U602 already corrected")
        return False

    if "XL1509-5.0E1" not in block:
        raise RuntimeError(f"{path}: U602 does not contain expected XL1509-5.0E1 metadata")

    block2 = block.replace("XL1509-5.0E1", "XL1509-3.3E1")
    block2 = block2.replace("XL1509-5-0E1_C61063.pdf", "XL1509-3-3E1_C74193.html")
    block2 = block2.replace('"C61063"', '"C74193"')

    # If the old LCSC datasheet URL remains for any reason, replace the entire
    # Datasheet field inside U602 with a stable LCSC product page.
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
