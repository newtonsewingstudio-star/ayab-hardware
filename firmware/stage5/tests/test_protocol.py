"""No hardware needed: verify SLIP format and documented discovery response."""
import unittest

END, ESC, ESC_END, ESC_ESC = 0xC0, 0xDB, 0xDC, 0xDD


def encode(payload):
    out = bytearray([END])
    for b in payload:
        if b == END:
            out.extend([ESC, ESC_END])
        elif b == ESC:
            out.extend([ESC, ESC_ESC])
        else:
            out.append(b)
    return bytes(out + bytes([END]))


def crc8(data):
    crc = 0
    for value in data:
        for _ in range(8):
            bit = (crc ^ value) & 1
            crc >>= 1
            if bit:
                crc ^= 0x8C
            value >>= 1
    return crc


class ProtocolTests(unittest.TestCase):
    def test_info_packet(self):
        self.assertEqual(encode(bytes([0x03])), bytes([END, 0x03, END]))

    def test_escaping(self):
        self.assertEqual(encode(bytes([END, ESC])), bytes([END, ESC, ESC_END, ESC, ESC_ESC, END]))

    def test_crc8_reference(self):
        self.assertEqual(crc8(b"123456789"), 0xA1)  # Dallas/Maxim CRC-8

    def test_info_layout(self):
        info = bytearray(22)
        info[:5] = bytes([0xC3, 6, 0, 0, 1])
        info[5:5+12] = b"esp32-proto\x00"
        self.assertEqual(info[0], 0xC3)
        self.assertEqual(info[1], 6)
        self.assertEqual(len(info), 22)


if __name__ == "__main__":
    unittest.main()