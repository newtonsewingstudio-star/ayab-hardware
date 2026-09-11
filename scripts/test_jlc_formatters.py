import subprocess
import sys
import tempfile
import unittest
import json
from pathlib import Path

import pandas as pd


SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent


class JlcFormatterTests(unittest.TestCase):
    def run_formatter(self, script, source_text):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.csv"
            output = Path(directory) / "output.csv"
            source.write_text(source_text, encoding="utf-8")
            subprocess.run(
                [sys.executable, str(SCRIPTS / script), str(source), str(output)],
                check=True,
            )
            return pd.read_csv(output, dtype=str, keep_default_na=False)

    def test_current_ten_column_kicad_bom(self):
        result = self.run_formatter(
            "jlc_bom_formatter.py",
            "Reference,Value,Footprint,Datasheet,Description,Qty,#,Mfg,Mfg P/N,LCSC ID\n"
            "R1 R2,10k,Resistor_SMD:R_0603_1608Metric,example,Resistor,2,1,UNI-ROYAL,0603WAF1002T5E,C25804\n",
        )
        self.assertEqual(
            list(result.columns),
            ["Comment", "Designator", "Footprint", "LCSC Part #"],
        )
        self.assertEqual(result.iloc[0].to_dict(), {
            "Comment": "10k",
            "Designator": "R1 R2",
            "Footprint": "R0603",
            "LCSC Part #": "C25804",
        })

    def test_jobset_exports_lcsc_id_as_a_custom_field(self):
        jobset = json.loads(
            (ROOT / "ayab-library" / "ayab-jobset.kicad_jobset").read_text(encoding="utf-8")
        )
        bom_job = next(job for job in jobset["jobs"] if job["type"] == "sch_export_bom")
        ordered = bom_job["settings"]["fields_ordered"]
        self.assertIn("LCSC ID", ordered)
        self.assertNotIn("__LCSC ID", ordered)
        position_job = next(job for job in jobset["jobs"] if job["type"] == "pcb_export_pos")
        self.assertTrue(position_job["settings"]["exclude_dnp"])
        gerber_job = next(job for job in jobset["jobs"] if job["type"] == "pcb_export_gerbers")
        self.assertIn("F.Paste", gerber_job["settings"]["layers"])
        self.assertIn("B.Paste", gerber_job["settings"]["layers"])
        self.assertTrue(gerber_job["settings"]["subtract_solder_mask_from_silk"])
        drill_job = next(job for job in jobset["jobs"] if job["type"] == "pcb_export_drill")
        self.assertEqual(drill_job["settings"]["units"], "mm")
        self.assertTrue(drill_job["settings"]["excellon.combine_pth_npth"])
        self.assertTrue(drill_job["settings"]["generate_map"])
        self.assertEqual(drill_job["settings"]["map_format"], "gerberx2")

    def test_legacy_six_column_bom(self):
        result = self.run_formatter(
            "jlc_bom_formatter.py",
            "A,B,C,D,E,F\nU1,ESP32,Module:ESP32-S3-MINI-1,Espressif,ESP32-S3-MINI-1-N8,C2913202\n",
        )
        self.assertEqual(result.iloc[0]["Footprint"], "ESP32-S3-MINI-1")
        self.assertEqual(result.iloc[0]["LCSC Part #"], "C2913202")

    def test_cpl_keeps_last_component_without_footer(self):
        result = self.run_formatter(
            "jlc_cpl_formatter.py",
            "Ref,Val,Package,PosX,PosY,Rot,Side\nR1,10k,R0603,10.0,20.0,90,top\nC1,100n,C0603,11.0,21.0,180,bottom\n",
        )
        self.assertEqual(list(result["Designator"]), ["R1", "C1"])
        self.assertEqual(list(result["Layer"]), ["T", "B"])

    def test_cpl_removes_comment_footer_only(self):
        result = self.run_formatter(
            "jlc_cpl_formatter.py",
            "Ref,Val,Package,PosX,PosY,Rot,Side\nR1,10k,R0603,10.0,20.0,90,top\n# End of position file,,,,,,\n",
        )
        self.assertEqual(list(result["Designator"]), ["R1"])

    def test_cpl_is_reconciled_to_fitted_bom(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.csv"
            bom = Path(directory) / "bom.csv"
            output = Path(directory) / "output.csv"
            source.write_text(
                "Ref,Val,Package,PosX,PosY,Rot,Side\n"
                "R1,10k,R0603,10.0,20.0,90,top\n"
                "R2,10k,R0603,11.0,21.0,90,top\n"
                "R3,DNP,R0603,12.0,22.0,90,top\n"
                "FID1,Fiducial,Fiducial,13.0,23.0,0,top\n",
                encoding="utf-8",
            )
            bom.write_text(
                "Comment,Designator,Footprint,LCSC Part #\n10k,R1 R2,R0603,C25804\n",
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "jlc_cpl_formatter.py"),
                    str(source),
                    str(output),
                    str(bom),
                ],
                check=True,
            )
            result = pd.read_csv(output, dtype=str, keep_default_na=False)
            self.assertEqual(list(result["Designator"]), ["R1", "R2"])


if __name__ == "__main__":
    unittest.main()
