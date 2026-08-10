#!/usr/bin/env python3
"""Generate the Cold Shower Timer app icons (no third-party libraries).

Draws an icy vertical-gradient rounded square with a glowing snowflake,
supersampled for smooth edges, and writes the PNG sizes the PWA needs.
"""
import math, struct, zlib, os

OUT = os.path.join(os.path.dirname(__file__), "..", "icons")
os.makedirs(OUT, exist_ok=True)

# ---- colours ----
TOP = (14, 61, 92)      # #0e3d5c
BOT = (4, 18, 31)       # #04121f
GLOW = (20, 92, 128)    # radial highlight near top
SNOW = (236, 247, 255)  # #ecf7ff
CYAN = (127, 227, 255)  # glow tint


def lerp(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def smoothstep(e0, e1, x):
    if e1 == e0:
        return 0.0 if x < e0 else 1.0
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


def dist_to_segment(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    if L2 == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def snowflake_segments(cx, cy, radius):
    """Return list of (ax, ay, bx, by) for a 6-arm snowflake."""
    segs = []
    arm = radius
    branch = radius * 0.30
    for k in range(6):
        a = math.radians(60 * k)
        ex, ey = cx + math.cos(a) * arm, cy + math.sin(a) * arm
        segs.append((cx, cy, ex, ey))
        # two branch pairs along the arm
        for frac in (0.55, 0.82):
            bx, by = cx + math.cos(a) * arm * frac, cy + math.sin(a) * arm * frac
            for da in (60, -60):
                a2 = a + math.radians(da)
                segs.append((bx, by,
                             bx + math.cos(a2) * branch,
                             by + math.sin(a2) * branch))
    return segs


def render(size, ss, rounded, snow_scale):
    S = size * ss
    px = bytearray(S * S * 4)
    cx = cy = S / 2.0
    corner = S * 0.225 if rounded else 0.0
    core_w = S * 0.018          # snowflake stroke half-width
    feather = S * 0.010
    glow_w = S * 0.05
    segs = snowflake_segments(cx, cy, S * 0.5 * snow_scale)
    snow_reach = S * 0.5 * snow_scale + glow_w + core_w

    for y in range(S):
        ty = y / (S - 1)
        base = lerp(TOP, BOT, ty)
        row = y * S * 4
        for x in range(S):
            # radial glow near top-centre
            gd = math.hypot(x - cx, y - S * 0.30) / (S * 0.7)
            col = list(lerp(base, GLOW, max(0.0, 0.55 - gd) * 0.6))

            # snowflake (only test pixels within reach of centre)
            if abs(x - cx) < snow_reach and abs(y - cy) < snow_reach:
                dmin = 1e9
                for (ax, ay, bx, by) in segs:
                    d = dist_to_segment(x, y, ax, ay, bx, by)
                    if d < dmin:
                        dmin = d
                        if dmin < core_w * 0.4:
                            break
                a_core = 1.0 - smoothstep(core_w, core_w + feather, dmin)
                if a_core > 0:
                    col = list(lerp(col, SNOW, a_core))
                a_glow = (1.0 - smoothstep(core_w, core_w + glow_w, dmin)) * 0.35
                if a_glow > 0:
                    for i in range(3):
                        col[i] = min(255, col[i] + CYAN[i] * a_glow)

            # rounded-corner alpha mask
            alpha = 255
            if rounded:
                ddx = max(0.0, abs(x - cx) - (S / 2 - corner))
                ddy = max(0.0, abs(y - cy) - (S / 2 - corner))
                cd = math.hypot(ddx, ddy)
                alpha = int(round(255 * (1.0 - smoothstep(corner - 1.0, corner + 0.5, cd))))

            o = row + x * 4
            px[o] = int(max(0, min(255, col[0])))
            px[o + 1] = int(max(0, min(255, col[1])))
            px[o + 2] = int(max(0, min(255, col[2])))
            px[o + 3] = alpha

    return downsample(px, S, ss), size


def downsample(px, S, ss):
    out_size = S // ss
    out = bytearray(out_size * out_size * 4)
    inv = 1.0 / (ss * ss)
    for y in range(out_size):
        for x in range(out_size):
            r = g = b = a = 0
            for dy in range(ss):
                sy = (y * ss + dy) * S * 4
                for dx in range(ss):
                    o = sy + (x * ss + dx) * 4
                    r += px[o]; g += px[o + 1]; b += px[o + 2]; a += px[o + 3]
            o = (y * out_size + x) * 4
            out[o] = int(r * inv); out[o + 1] = int(g * inv)
            out[o + 2] = int(b * inv); out[o + 3] = int(a * inv)
    return out


def write_png(path, rgba, size):
    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data +
                struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))
    raw = bytearray()
    for y in range(size):
        raw.append(0)
        raw += rgba[y * size * 4:(y + 1) * size * 4]
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


if __name__ == "__main__":
    for size, ss, rounded, scale, name in [
        (512, 3, True,  0.62, "icon-512.png"),
        (192, 3, True,  0.62, "icon-192.png"),
        (180, 3, True,  0.62, "icon-180.png"),
        (512, 3, False, 0.50, "icon-512-maskable.png"),
    ]:
        print(f"Rendering {name}…")
        rgba, _ = render(size, ss, rounded=rounded, snow_scale=scale)
        write_png(os.path.join(OUT, name), rgba, size)
    print("Done →", os.path.abspath(OUT))
