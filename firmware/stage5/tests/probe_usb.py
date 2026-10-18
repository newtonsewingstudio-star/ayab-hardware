#!/usr/bin/env python3
"""Read-only AYAB USB discovery probe. NEVER starts knitting or touches outputs.

Usage: pip install pyserial
       python tests/probe_usb.py COM5
"""
import argparse
import sys

END, ESC, ESC_END, ESC_ESC = 0xC0, 0xDB, 0xDC, 0xDD


def slip_encode(data):
    result = bytearray([END])
    for b in data:
        if b == END:
            result.extend((ESC, ESC_END))
        elif b == ESC:
            result.extend((ESC, ESC_ESC))
        else:
            result.append(b)
    result.append(END)
    return bytes(result)


def slip_frames(stream):
    buf = bytearray()
    escape = False
    invalid = False
    for b in stream:
        if b == END:
            if buf and not invalid and not escape:
                yield bytes(buf)
            buf.clear()
            escape = False
            invalid = False
        elif invalid:
            continue
        elif escape:
            escape = False
            if b == ESC_END:
                buf.append(END)
            elif b == ESC_ESC:
                buf.append(ESC)
            else:
                invalid = True
        elif b == ESC:
            escape = True
        elif len(buf) < 256:
            buf.append(b)
        else:
            invalid = True


def parse_info(payload):
    if len(payload) != 22 or payload[0] != 0xC3:
        raise ValueError(f"Unexpected AYAB response ({len(payload)} bytes): {payload.hex()}")
    suffix = payload[5:22].split(b'\x00', 1)[0].decode('ascii', errors='replace')
    return dict(api=payload[1], firmware='.'.join(map(str, payload[2:5])), suffix=suffix)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('port', help='Serial port, e.g. COM5 on Windows')
    parser.add_argument('--timeout', type=float, default=3)
    args = parser.parse_args()
    try:
        import serial
    except ImportError:
        print('Install pyserial: python -m pip install pyserial', file=sys.stderr)
        return 2
    try:
        with serial.Serial(args.port, baudrate=115200, timeout=args.timeout, write_timeout=2) as conn:
            conn.reset_input_buffer()
            conn.write(slip_encode(b'\x03'))  # ONLY reqInfo
            raw = conn.read(128)
    except serial.SerialException as exc:
        print(f'Serial connection failed: {exc}', file=sys.stderr)
        return 2
    for frame in slip_frames(raw):
        if frame and frame[0] == 0xC3:
            print(parse_info(frame))
            return 0
    print(f'No valid info response; received {raw.hex()}', file=sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())
