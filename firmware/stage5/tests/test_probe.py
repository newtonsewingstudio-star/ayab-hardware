"""Host-only tests for the read-only physical USB probe."""
import unittest
from probe_usb import slip_encode, slip_frames, parse_info

class ProbeTests(unittest.TestCase):
    def test_slip_round_trip(self):
        frame = bytes([0x03, 0xC0, 0xDB, 0x07])
        self.assertEqual(list(slip_frames(slip_encode(frame))), [frame])

    def test_info(self):
        payload = bytes([0xC3, 6, 0, 0, 1]) + b'esp32-proto\x00' + bytes(5)
        self.assertEqual(parse_info(payload)['suffix'], 'esp32-proto')

    def test_corrupt_escape_rejected(self):
        self.assertEqual(list(slip_frames(bytes([0xC0, 0x03, 0xDB, 0x01, 0xC0]))), [])

    def test_invalid_info_rejected(self):
        with self.assertRaises(ValueError):
            parse_info(bytes([0xC5, 0]))

if __name__ == '__main__':
    unittest.main()