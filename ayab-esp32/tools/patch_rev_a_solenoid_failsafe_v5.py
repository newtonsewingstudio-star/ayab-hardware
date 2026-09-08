#!/usr/bin/env python3
"""Correct Q806 AO3400A orientation in the Rev A solenoid fail-safe.

AO3400A SOT-23 pinout is 1=Gate, 2=Source, 3=Drain. The first custom symbol
placed pin 2 on the P-MOS gate node and pin 3 on ground. That reverses the
pull-down device and puts its body diode in the wrong direction.

Keep the existing schematic geometry but place:
  pin 3 Drain  -> upper node -> P-MOS gate
  pin 2 Source -> lower node -> GND
"""

import patch_rev_a_solenoid_failsafe_v3 as v3

base = v3.base
SOL = base.SOL


def main() -> None:
    text = SOL.read_text()
    token = '(symbol "ayab-lib:AO3400A_FAILSAFE"'
    start = text.find(token)
    if start < 0:
        raise RuntimeError('AO3400A_FAILSAFE library symbol missing')
    old_block, end = base.extract_block(text, start)

    correct_source = '''(pin passive line (at 0 -7.62 90) (length 2.54)
          (name "S" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27))))
        )'''
    correct_drain = '''(pin passive line (at 0 7.62 270) (length 2.54)
          (name "D" (effects (font (size 1.27 1.27))))
          (number "3" (effects (font (size 1.27 1.27))))
        )'''
    if correct_source in old_block and correct_drain in old_block:
        print('Q806 AO3400A source/drain orientation already correct')
        return

    wrong_source = '''(pin passive line (at 0 7.62 270) (length 2.54)
          (name "S" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27))))
        )'''
    wrong_drain = '''(pin passive line (at 0 -7.62 90) (length 2.54)
          (name "D" (effects (font (size 1.27 1.27))))
          (number "3" (effects (font (size 1.27 1.27))))
        )'''
    if wrong_source not in old_block or wrong_drain not in old_block:
        raise RuntimeError('Unexpected AO3400A_FAILSAFE pin geometry')

    new_block = old_block.replace(wrong_source, correct_source, 1).replace(wrong_drain, correct_drain, 1)
    text = text[:start] + new_block + text[end:]

    check = base.get_block(text, token)
    if correct_source not in check or correct_drain not in check:
        raise RuntimeError('Q806 orientation postcondition failed')
    SOL.write_text(text)
    print('Corrected Q806: drain to P-MOS gate, source to GND')


if __name__ == '__main__':
    main()
