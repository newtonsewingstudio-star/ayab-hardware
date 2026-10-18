"""Compile the hardware-independent C++ knitting-session tests."""
import pathlib
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]

def test_bench_cpp():
    with tempfile.TemporaryDirectory() as directory:
        exe = pathlib.Path(directory)/'bench_session'
        subprocess.run(['g++','-std=c++17','-Wall','-Wextra','-Werror',str(ROOT/'tests/test_bench_session.cpp'),'-o',str(exe)],check=True)
        subprocess.run([str(exe)],check=True)
