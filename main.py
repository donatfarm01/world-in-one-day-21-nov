#!/usr/bin/env python3
"""World in One Day -- 21 November 2026.

A program that draws one newspaper-style poster summing up the world's
news of Saturday 21 November 2026 as a single 1024x1024 PNG and writes it
to $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).

Pure Python 3.13 standard library: no network, no files read, no
randomness, no timestamps. Every run writes byte-identical output.

The six stories on the poster were each verified against wire-style
reports published on 21 November 2026 (Reuters/AP/UKMTO/ICJ coverage as
carried by the day's news roundups):

  1. Russian missiles hit Poland -- two missiles and a suspected drone
     came down in Poland; Warsaw calls it a deliberate provocation and
     NATO calls it a grave violation of allied airspace.
  2. Wall Street slumps -- the S&P 500 fell about 3.7% as AI shares sold
     off, pushing US benchmarks into correction territory.
  3. Trump, Xi and Putin meet -- the first trilateral summit, in
     Shenzhen, ends with a symbolic declaration against nuclear war and
     few concrete results.
  4. The World Court rules 9-6 that Myanmar committed genocide against
     the Rohingya.
  5. COP31 climate talks in Turkey run into extra hours, split over
     fossil fuels and finance.
  6. Cyclone Akvan crosses India's Odisha coast with strong winds and
     heavy rain.

In brief: a tanker is hit and ablaze off Oman in the Strait of Hormuz;
the Saudi-led coalition intercepts Houthi missiles over Riyadh; the UK
and EU sign food, carbon and youth-mobility deals; JPMorgan, Visa and
Mastercard report cyberattacks on third-party vendors.
"""

import math
import os
import struct
import zlib

W = 1024
H = 1024

# --- palette: a newspaper front page -------------------------------------
PAPER = (248, 244, 233)   # warm off-white
INK = (22, 19, 14)        # near-black ink
RED = (179, 39, 30)       # lead red
BLUE = (31, 78, 121)      # steel blue
GOLD = (176, 132, 32)     # muted gold
GREEN = (46, 110, 62)     # deep green
WHITE = (255, 255, 255)
GREY = (112, 106, 96)     # captions
PANEL = (255, 253, 247)   # panel background

# --- 5x7 bitmap font ------------------------------------------------------
# Each glyph is 7 rows of 5 pixels, "#" on, " " off. Uppercase only; the
# renderer uppercases input, so lowercase letters render as capitals.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
}

BLANK = ("00000", "00000", "00000", "00000", "00000", "00000", "00000")


def text_width(text, scale):
    """Pixel width of text at the given scale (6 px per glyph, scaled)."""
    return len(text) * 6 * scale


def wrap_text(text, max_chars):
    """Word-wrap text to lines of at most max_chars characters."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        line = ""
        for word in words:
            if not line:
                line = word
            elif len(line) + 1 + len(word) <= max_chars:
                line += " " + word
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


class Canvas:
    """An RGB raster canvas with simple vector drawing primitives."""

    def __init__(self, width, height, bg):
        self.w = width
        self.h = height
        self.px = bytearray(bg * (width * height))

    def _idx(self, x, y):
        return (y * self.w + x) * 3

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = self._idx(x, y)
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            i = self._idx(x0, yy)
            self.px[i:i + len(row)] = row

    def hline(self, x, y, w, color):
        self.fill_rect(x, y, w, 1, color)

    def vline(self, x, y, h, color):
        self.fill_rect(x, y, 1, h, color)

    def line(self, x0, y0, x1, y1, color, thick=1):
        """Bresenham line with a square brush of the given thickness."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        half = thick // 2
        while True:
            self.fill_rect(x - half, y - half, thick, thick, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def polyline(self, points, color, thick=1):
        for (ax, ay), (bx, by) in zip(points, points[1:]):
            self.line(ax, ay, bx, by, color, thick)

    def circle(self, cx, cy, r, color):
        """Filled circle, drawn scanline by scanline."""
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            self.fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)

    def ring(self, cx, cy, r, color, thick=2):
        """Circle outline of the given thickness."""
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            inner = int(math.sqrt(max(0, (r - thick) * (r - thick) - dy * dy))) \
                if r - thick > abs(dy) else 0
            self.fill_rect(cx - dx, cy + dy, dx - inner, 1, color)
            self.fill_rect(cx + inner + 1, cy + dy, dx - inner, 1, color)

    def ellipse(self, cx, cy, rx, ry, color):
        for dy in range(-ry, ry + 1):
            dx = int(rx * math.sqrt(max(0.0, 1.0 - (dy * dy) / float(ry * ry))))
            self.fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)

    def triangle(self, p0, p1, p2, color):
        """Filled triangle via barycentric test inside its bounding box."""
        xs = [p0[0], p1[0], p2[0]]
        ys = [p0[1], p1[1], p2[1]]
        x0, x1 = max(0, min(xs)), min(self.w - 1, max(xs))
        y0, y1 = max(0, min(ys)), min(self.h - 1, max(ys))
        d = (p1[1] - p2[1]) * (p0[0] - p2[0]) + (p2[0] - p1[0]) * (p0[1] - p2[1])
        if d == 0:
            return
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                a = ((p1[1] - p2[1]) * (x - p2[0]) + (p2[0] - p1[0]) * (y - p2[1])) / d
                b = ((p2[1] - p0[1]) * (x - p2[0]) + (p0[0] - p2[0]) * (y - p2[1])) / d
                c = 1.0 - a - b
                if a >= 0 and b >= 0 and c >= 0:
                    self.set(x, y, color)

    def starburst(self, cx, cy, r_outer, r_inner, points, color):
        """A spiky star: alternating outer/inner vertices, filled fan."""
        verts = []
        for i in range(points * 2):
            r = r_outer if i % 2 == 0 else r_inner
            ang = math.pi * i / points - math.pi / 2
            verts.append((cx + int(r * math.cos(ang)),
                          cy + int(r * math.sin(ang))))
        for i in range(1, len(verts) - 1):
            self.triangle(verts[0], verts[i], verts[i + 1], color)

    def text(self, x, y, text, scale, color, align="left"):
        """Draw text; returns the pixel width drawn."""
        text = text.upper()
        width = text_width(text, scale)
        if align == "center":
            x -= width // 2
        elif align == "right":
            x -= width
        for ch in text:
            glyph = FONT.get(ch, BLANK)
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.fill_rect(x + col * scale, y + row * scale,
                                       scale, scale, color)
            x += 6 * scale
        return width

    def para(self, x, y, text, scale, color, max_chars, line_gap=4,
             align="left"):
        """Draw word-wrapped text; returns the y just below the last line."""
        lines = wrap_text(text, max_chars)
        for line in lines:
            if align == "center":
                self.text(x, y, line, scale, color, align="center")
            else:
                self.text(x, y, line, scale, color)
            y += 7 * scale + line_gap
        return y


def write_png(canvas, path):
    """Encode the canvas as a PNG (8-bit RGB, filter 0) and write it."""
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)
        i = y * stride
        raw += canvas.px[i:i + stride]
    data = zlib.compress(bytes(raw), 9)

    def chunk(kind, payload):
        out = struct.pack(">I", len(payload)) + kind + payload
        out += struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", data)
           + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
    os.chmod(path, 0o644)
    return len(png)


# --- story icons -----------------------------------------------------------
# Each icon draws inside a box (x, y, w, h) using simple flat shapes that
# stay legible when the image is viewed small.

def icon_missile(c, x, y, w, h):
    """Explosion burst with a compact missile at lower left (lead story)."""
    cx, cy = x + w // 2 + 20, y + h // 2
    c.starburst(cx, cy, 50, 26, 12, GOLD)
    c.starburst(cx, cy, 36, 18, 12, RED)
    c.circle(cx, cy, 13, (255, 214, 90))
    # missile: short body from lower left toward the burst, nose cone,
    # tail fins and a flame puff at the tail
    c.line(x + 28, y + h - 28, x + 118, y + 66, INK, 6)
    c.triangle((x + 118, y + 66), (x + 150, y + 48),
               (x + 132, y + 88), RED)
    c.triangle((x + 52, y + h - 56), (x + 40, y + h - 30),
               (x + 70, y + h - 38), INK)
    c.starburst(x + 22, y + h - 22, 10, 5, 8, (255, 140, 40))


def icon_chart(c, x, y, w, h):
    """A market line falling hard, with an arrowhead (markets story)."""
    ox, oy = x + 14, y + h - 16
    c.line(ox, y + 10, ox, oy, INK, 3)
    c.line(ox, oy, x + w - 8, oy, INK, 3)
    pts = [(ox + 6, y + 20), (ox + 34, y + 28), (ox + 58, y + 24),
           (ox + 86, y + 44), (ox + 112, y + 62), (ox + 136, y + 76)]
    c.polyline(pts, RED, 5)
    ex, ey = pts[-1]
    c.triangle((ex, ey), (ex - 18, ey - 2), (ex - 4, ey - 18), RED)
    c.text(x + w - 66, y + 8, "-3.7%", 2, RED)


def icon_summit(c, x, y, w, h):
    """Three leaders' circles around a table (summit story)."""
    cy = y + 44
    c.circle(x + 42, cy, 24, RED)
    c.circle(x + w // 2, cy - 12, 24, BLUE)
    c.circle(x + w - 42, cy, 24, GOLD)
    c.ring(x + 42, cy, 24, INK, 3)
    c.ring(x + w // 2, cy - 12, 24, INK, 3)
    c.ring(x + w - 42, cy, 24, INK, 3)
    c.fill_rect(x + 18, y + h - 24, w - 36, 6, INK)
    c.fill_rect(x + 30, y + h - 18, 8, 18, INK)
    c.fill_rect(x + w - 38, y + h - 18, 8, 18, INK)


def icon_scales(c, x, y, w, h):
    """Scales of justice (World Court story)."""
    cx = x + w // 2
    c.vline(cx, y + 12, h - 40, INK)
    c.hline(cx - 52, y + 20, 104, INK)
    c.fill_rect(cx - 8, y + 8, 16, 6, GOLD)
    for sx in (cx - 52, cx + 52):
        c.line(sx, y + 20, sx - 16, y + 56, INK, 3)
        c.line(sx, y + 20, sx + 16, y + 56, INK, 3)
        c.triangle((sx - 20, y + 56), (sx + 20, y + 56),
                   (sx, y + 74), GOLD)
    c.fill_rect(cx - 34, y + h - 14, 68, 6, INK)


def icon_globe(c, x, y, w, h):
    """A globe with a leaf (climate talks story)."""
    cx, cy = x + w // 2, y + h // 2 - 2
    c.circle(cx, cy, 38, BLUE)
    c.ellipse(cx, cy, 38, 15, (64, 140, 190))
    c.ellipse(cx, cy, 15, 38, (64, 140, 190))
    c.ring(cx, cy, 38, INK, 3)
    c.circle(cx - 14, cy - 10, 9, GREEN)
    c.circle(cx + 12, cy + 10, 8, GREEN)
    # leaf sprouting from the top
    c.ellipse(cx + 26, cy - 42, 12, 5, GREEN)
    c.line(cx + 16, cy - 36, cx + 34, cy - 44, GREEN, 3)


def icon_cyclone(c, x, y, w, h):
    """A storm spiral with rain slashes (cyclone story)."""
    cx, cy = x + w // 2, y + h // 2 - 6
    for r in (36, 28, 20, 12):
        c.ring(cx, cy, r, BLUE, 4)
    c.circle(cx, cy, 8, BLUE)
    c.ring(cx, cy, 8, INK, 2)
    # rain slashes below the spiral
    for rx in (x + 16, x + 44, x + 72, x + 100, x + 128):
        c.line(rx, y + h - 16, rx - 6, y + h - 4, BLUE, 4)


# --- layout ----------------------------------------------------------------

MARGIN = 24
CELL_W = 304
CELL_H = 256
GUTTER = 16

# (tag, tag color, headline, deck, icon function)
STORIES = [
    ("MARKETS - NEW YORK", BLUE, "WALL STREET SLUMPS",
     "AI sell-off drags the S&P 500 down 3.7%.",
     icon_chart),
    ("DIPLOMACY - SHENZHEN", GOLD, "TRUMP, XI, PUTIN MEET",
     "Trilateral summit ends: a symbolic declaration, few results.",
     icon_summit),
    ("JUSTICE - THE HAGUE", RED, "ICJ: MYANMAR GENOCIDE",
     "World Court: Myanmar committed genocide against the Rohingya.",
     icon_scales),
    ("CLIMATE - TURKEY", GREEN, "COP31 TALKS RUN LONG",
     "UN climate talks head into extra hours, split over fossil fuels.",
     icon_globe),
    ("WEATHER - INDIA", BLUE, "CYCLONE AKVAN LANDFALL",
     "Cyclone Akvan hits India's Odisha coast with heavy rain.",
     icon_cyclone),
]

BRIEFS = [
    "Tanker ablaze in the Strait of Hormuz.",
    "Saudi downs Houthi missiles over Riyadh.",
    "UK and EU sign food, carbon, youth deals.",
    "Banks report vendor cyberattacks.",
    "Palisades fire arsonist convicted.",
]


def draw_cell(c, x, y, tag, tag_color, headline, deck, icon_fn):
    """One grid cell: tag, icon, headline, deck."""
    c.fill_rect(x, y, CELL_W, CELL_H, PANEL)
    c.fill_rect(x, y, CELL_W, 8, tag_color)
    # 2 px ink border
    c.fill_rect(x, y, CELL_W, 2, INK)
    c.fill_rect(x, y + CELL_H - 2, CELL_W, 2, INK)
    c.fill_rect(x, y, 2, CELL_H, INK)
    c.fill_rect(x + CELL_W - 2, y, 2, CELL_H, INK)
    c.text(x + 14, y + 18, tag, 2, tag_color)
    icon_fn(c, x + (CELL_W - 160) // 2, y + 36, 160, 96)
    c.para(x + 14, y + 136, headline, 3, INK, 15, line_gap=3)
    c.para(x + 14, y + 188, deck, 2, INK, 23, line_gap=3)


def draw_brief_cell(c, x, y):
    """The IN BRIEF cell: four one-line stories with red square bullets."""
    c.fill_rect(x, y, CELL_W, CELL_H, PANEL)
    c.fill_rect(x, y, CELL_W, 8, INK)
    c.fill_rect(x, y, CELL_W, 2, INK)
    c.fill_rect(x, y + CELL_H - 2, CELL_W, 2, INK)
    c.fill_rect(x, y, 2, CELL_H, INK)
    c.fill_rect(x + CELL_W - 2, y, 2, CELL_H, INK)
    c.text(x + 14, y + 18, "IN BRIEF", 2, INK)
    yy = y + 46
    for item in BRIEFS:
        c.fill_rect(x + 14, yy + 4, 10, 10, RED)
        yy = c.para(x + 32, yy, item, 2, INK, 21, line_gap=3)
        yy += 6


def draw_poster():
    c = Canvas(W, H, PAPER)

    # --- masthead ------------------------------------------------------
    c.text(W // 2, 30, "THE WORLD IN ONE DAY", 5, INK, align="center")
    c.text(W // 2, 92, "SATURDAY, 21 NOVEMBER 2026", 3, RED, align="center")
    c.text(W // 2, 126, "SIX STORIES THAT DEFINED THE DAY", 2, GREY,
           align="center")
    c.fill_rect(MARGIN, 152, W - 2 * MARGIN, 4, RED)
    c.fill_rect(MARGIN, 158, W - 2 * MARGIN, 2, INK)

    # --- lead story ----------------------------------------------------
    lx, ly, lw, lh = MARGIN, 170, W - 2 * MARGIN, 230
    c.fill_rect(lx, ly, lw, lh, PANEL)
    c.fill_rect(lx, ly, lw, 3, INK)
    c.fill_rect(lx, ly + lh - 3, lw, 3, INK)
    c.fill_rect(lx, ly, 3, lh, INK)
    c.fill_rect(lx + lw - 3, ly, 3, lh, INK)
    c.text(lx + 20, ly + 16, "LEAD STORY - EUROPE", 2, RED)
    c.text(lx + 20, ly + 44, "RUSSIAN MISSILES HIT POLAND", 4, INK)
    c.para(lx + 20, ly + 92,
           "Two missiles and a suspected drone came down in Poland. "
           "Warsaw calls it a deliberate provocation; NATO calls it a "
           "grave violation of allied airspace.",
           3, INK, 37, line_gap=5)
    icon_missile(c, lx + lw - 260, ly + 16, 240, 198)

    # --- story grid ----------------------------------------------------
    gx, gy = MARGIN, 416
    for i, (tag, color, headline, deck, icon_fn) in enumerate(STORIES):
        col = i % 3
        row = i // 3
        draw_cell(c, gx + col * (CELL_W + GUTTER),
                  gy + row * (CELL_H + GUTTER),
                  tag, color, headline, deck, icon_fn)
    draw_brief_cell(c, gx + 2 * (CELL_W + GUTTER), gy + CELL_H + GUTTER)

    # --- footer --------------------------------------------------------
    c.fill_rect(MARGIN, 962, W - 2 * MARGIN, 2, INK)
    c.text(MARGIN, 976, "SOURCES: REUTERS - AP - UKMTO - ICJ - WIRE REPORTS",
           2, GREY)
    c.text(W - MARGIN, 976, "21 NOVEMBER 2026", 2, GREY, align="right")
    return c


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    canvas = draw_poster()
    size = write_png(canvas, path)
    print("wrote %s (%d bytes, %dx%d)" % (path, size, W, H))


if __name__ == "__main__":
    main()
