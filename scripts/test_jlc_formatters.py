import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


SCRIPTS = Path(__file__).resolve().parent


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


if __name__ == "__main__":
    unittest.main()
