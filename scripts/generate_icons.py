"""
generate_icons.py — creates placeholder PNG icons for YT Autoplay Off.

Design: YouTube-red (#CC0000) circle, white pause bars in the centre.
No external dependencies — uses only Python's stdlib.

Usage:
    python3 scripts/generate_icons.py

Output:
    Extension/icons/icon-16.png
    Extension/icons/icon-32.png
    Extension/icons/icon-48.png
    Extension/icons/icon-128.png

Replace these with properly designed assets before shipping.
"""

import math
import os
import struct
import zlib

SIZES = [16, 32, 48, 128]
OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'Extension', 'icons')

# Palette
RED   = (204,   0,   0, 255)
WHITE = (255, 255, 255, 255)
CLEAR = (  0,   0,   0,   0)


def lerp(a, b, t):
    return a + (b - a) * t


def aa_alpha(distance, edge_radius, aa_width=1.0):
    """Return alpha 0-255 for anti-aliased circle edge."""
    return max(0, min(255, int(255 * (edge_radius - distance) / aa_width + 0.5)))


def make_pixels(size):
    """Return a list[list[tuple]] of RGBA pixels for the icon."""
    cx = cy = size / 2.0
    circle_r = size * 0.45
    aa_w = max(1.0, size * 0.03)

    # Pause bars: two rounded rectangles
    bar_w = size * 0.11
    bar_h = size * 0.30
    bar_gap = size * 0.07
    bar_lx = cx - bar_gap / 2 - bar_w   # left bar x-start
    bar_rx = cx + bar_gap / 2            # right bar x-start
    bar_ty = cy - bar_h / 2             # top y
    bar_by = cy + bar_h / 2             # bottom y
    bar_corner_r = bar_w * 0.35

    def in_bar(px, py, bx):
        """SDF-style check: distance to rounded rectangle interior."""
        # clamp to bar rectangle, measure distance
        lx, rx = bx, bx + bar_w
        dx = max(lx + bar_corner_r - px, 0, px - (rx - bar_corner_r))
        dy = max(bar_ty + bar_corner_r - py, 0, py - (bar_by - bar_corner_r))
        return math.sqrt(dx * dx + dy * dy)  # 0 means inside

    pixels = []
    for iy in range(size):
        row = []
        for ix in range(size):
            px = ix + 0.5
            py = iy + 0.5
            dist = math.hypot(px - cx, py - cy)

            if dist >= circle_r + aa_w:
                row.append(CLEAR)
                continue

            # Circle alpha (anti-aliased edge)
            circle_alpha = aa_alpha(dist, circle_r, aa_w)

            # Is this pixel inside a pause bar?
            d_left  = in_bar(px, py, bar_lx)
            d_right = in_bar(px, py, bar_rx)
            bar_dist = min(d_left, d_right)

            bar_aa = aa_w * 0.6
            bar_alpha = aa_alpha(bar_dist, 0, bar_aa)  # 0 = on bar edge

            if bar_alpha > 0 and dist < circle_r:
                # Blend white bar over red circle
                t = bar_alpha / 255.0
                r = int(lerp(RED[0], WHITE[0], t))
                g = int(lerp(RED[1], WHITE[1], t))
                b = int(lerp(RED[2], WHITE[2], t))
                a = circle_alpha
            else:
                r, g, b = RED[:3]
                a = circle_alpha

            row.append((r, g, b, a))
        pixels.append(row)
    return pixels


def write_png(path, pixels, width, height):
    def chunk(tag, data):
        c = tag + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xFFFFFFFF)

    ihdr = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    raw  = b''.join(
        b'\x00' + b''.join(struct.pack('BBBB', *px) for px in row)
        for row in pixels
    )
    idat = zlib.compress(raw, 9)

    data = b'\x89PNG\r\n\x1a\n'
    data += chunk(b'IHDR', ihdr)
    data += chunk(b'IDAT', idat)
    data += chunk(b'IEND', b'')

    with open(path, 'wb') as f:
        f.write(data)


if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    for size in SIZES:
        path = os.path.join(OUT_DIR, f'icon-{size}.png')
        pixels = make_pixels(size)
        write_png(path, pixels, size, size)
        print(f'  Generated {os.path.relpath(path)}')
    print('Done.')
