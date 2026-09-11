#!/usr/bin/env python3
"""Regression checks for revision-label clearance; native release source is read-only."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest

import validate_rev_a_manufacturing_metadata as validator


class RevisionLabelClearanceTests(unittest.TestCase):
    def check_fixture(self, x, y):
        original = validator.PCB
        text = original.read_text(encoding="utf-8")
        self.assertEqual(text.count("(at 180 142 0)"), 1)
        with tempfile.TemporaryDirectory(prefix="ayab-label-regression-") as temporary:
            fixture = Path(temporary) / "fixture.kicad_pcb"
            fixture.write_text(text.replace("(at 180 142 0)", f"(at {x} {y} 0)"), encoding="utf-8")
            try:
                validator.PCB = fixture
                with contextlib.redirect_stdout(io.StringIO()):
                    validator.main()
            finally:
                validator.PCB = original

    def test_release_label_passes(self):
        self.check_fixture(180, 142)

    def test_artwork_overlap_is_rejected(self):
        # This location crosses the AYAB artwork, which uses reference G***.
        with self.assertRaisesRegex(RuntimeError, "overlaps front footprint silkscreen"):
            self.check_fixture(150, 133)

    def test_previous_pad_overlap_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "overlaps front pad/mask clearance"):
            self.check_fixture(174, 161.2)


if __name__ == "__main__":
    unittest.main()
