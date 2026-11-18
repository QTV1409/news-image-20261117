# render.py — draws entry.png: a newspaper front page summing up the world
# news of Tuesday 17 November 2026. Run once, locally, with Pillow:
#   python3 render.py            (writes entry.png beside this file)
# The submitted program (main.py) only copies the finished entry.png to
# /output/entry.png, so the graded run needs no fonts and no Pillow.
# Every fact below was checked against reporting of 17 Nov 2026
# (BBC, AP, Reuters, Al Jazeera, Interfax-Ukraine, WION, Outlook India,
# Level Headlines, Spaceflight Now via ULA statement).
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 251, 244)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (110, 108, 100)
RULE = (60, 60, 60)
SKY = (183, 214, 232)
SEA = (46, 105, 150)
STEEL = (90, 96, 104)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        # trim the last line so the ellipsis fits
        while lines and draw.textlength(lines[-1] + " …", font=fnt) > max_w:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] += " …"
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- icons
def icon_bridge(draw, x, y, w, h=None):
    """Kerch Bridge: deck with a collapsed gap, its arch broken and down."""
    if h is None:
        h = w
    sx = lambda f: x + int(w * f)
    sy = lambda f: y + int(h * f)
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, sy(0.62), x + w, y + h], fill=SEA)
    # the great arch, broken at the crown: left and right halves only.
    # Top half of an ellipse whose centre sits at deck level.
    deck_y = sy(0.42)
    arch_box = [sx(0.08), deck_y - 92, sx(0.92), deck_y + 92]
    draw.arc(arch_box, 180, 258, fill=(60, 64, 70), width=10)
    draw.arc(arch_box, 282, 360, fill=(60, 64, 70), width=10)
    # deck, left and right of the gap
    draw.rectangle([x, sy(0.42), sx(0.38), sy(0.50)], fill=STEEL)
    draw.rectangle([sx(0.62), sy(0.42), x + w, sy(0.50)], fill=STEEL)
    # fallen deck slab, tilted in the water under the gap
    draw.polygon([(sx(0.42), sy(0.66)), (sx(0.60), sy(0.60)),
                  (sx(0.58), sy(0.68)), (sx(0.44), sy(0.74))],
                 fill=(60, 64, 70))
    # ripples around the wreckage
    for ry, rw in ((0.78, 0.30), (0.86, 0.22)):
        draw.arc([sx(0.50 - rw / 2), sy(ry) - 6, sx(0.50 + rw / 2), sy(ry) + 6],
                 0, 180, fill=(140, 180, 205), width=3)
    # smoke over the gap
    for cx, cy, r in ((0.47, 0.26, 9), (0.53, 0.20, 12), (0.50, 0.32, 7)):
        draw.ellipse([sx(cx) - r, sy(cy) - r, sx(cx) + r, sy(cy) + r],
                     fill=(120, 120, 118))


def icon_tanker(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(214, 228, 238))
    draw.rectangle([x, y + int(s * 0.66), x + s, y + s], fill=SEA)
    # hull
    draw.polygon([(x + int(s * 0.08), y + int(s * 0.52)),
                  (x + int(s * 0.92), y + int(s * 0.52)),
                  (x + int(s * 0.84), y + int(s * 0.72)),
                  (x + int(s * 0.16), y + int(s * 0.72))], fill=(150, 40, 32))
    # deck + bridge tower
    draw.rectangle([x + int(s * 0.68), y + int(s * 0.34), x + int(s * 0.82),
                    y + int(s * 0.52)], fill=(240, 240, 235))
    # fire and smoke from a mine strike amidships
    draw.polygon([(x + int(s * 0.42), y + int(s * 0.52)),
                  (x + int(s * 0.48), y + int(s * 0.28)),
                  (x + int(s * 0.54), y + int(s * 0.52))], fill=(232, 120, 20))
    draw.ellipse([x + int(s * 0.44), y + int(s * 0.12), x + int(s * 0.58),
                  y + int(s * 0.26)], fill=(90, 90, 88))


def icon_flags(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(232, 230, 222))
    # three flag poles: US, China, Russia (simplified)
    poles = [(0.20, (190, 30, 30)), (0.50, (200, 30, 30)), (0.80, (200, 30, 30))]
    # US flag: stripes + blue canton
    fx, fy, fw, fh = x + int(s * 0.06), y + int(s * 0.16), int(s * 0.24), int(s * 0.20)
    for i in range(5):
        draw.rectangle([fx, fy + i * fh // 5, fx + fw, fy + (i + 1) * fh // 5],
                       fill=(255, 255, 255) if i % 2 else (178, 34, 34))
    draw.rectangle([fx, fy, fx + fw // 2, fy + fh // 2], fill=(30, 50, 110))
    # China flag
    fx = x + int(s * 0.38)
    draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 30, 30))
    draw.ellipse([fx + 4, fy + 4, fx + 12, fy + 12], fill=(255, 220, 60))
    # Russia flag: white / blue / red horizontal
    fx = x + int(s * 0.70)
    for i, col in enumerate(((255, 255, 255), (20, 80, 180), (200, 30, 30))):
        draw.rectangle([fx, fy + i * fh // 3, fx + fw, fy + (i + 1) * fh // 3],
                       fill=col)
    # poles + table line
    for px in (0.18, 0.50, 0.82):
        draw.line([(x + int(s * px), y + int(s * 0.14)),
                   (x + int(s * px), y + int(s * 0.78))], fill=(70, 70, 70), width=3)
    draw.line([(x + int(s * 0.08), y + int(s * 0.80)),
               (x + int(s * 0.92), y + int(s * 0.80))], fill=(70, 70, 70), width=4)


def icon_bank(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(226, 224, 214))
    # pediment + columns
    draw.polygon([(x + int(s * 0.10), y + int(s * 0.34)),
                  (x + int(s * 0.90), y + int(s * 0.34)),
                  (x + int(s * 0.50), y + int(s * 0.14))], fill=(150, 145, 130))
    for cx in (0.18, 0.38, 0.58, 0.78):
        draw.rectangle([x + int(s * cx) - 4, y + int(s * 0.36),
                        x + int(s * cx) + 4, y + int(s * 0.78)], fill=(200, 196, 182))
    draw.rectangle([x + int(s * 0.08), y + int(s * 0.78), x + int(s * 0.92),
                    y + int(s * 0.86)], fill=(150, 145, 130))
    # a crack / bug mark: red zigzag across the pediment
    draw.line([(x + int(s * 0.30), y + int(s * 0.22)),
               (x + int(s * 0.40), y + int(s * 0.30)),
               (x + int(s * 0.50), y + int(s * 0.20)),
               (x + int(s * 0.60), y + int(s * 0.30)),
               (x + int(s * 0.70), y + int(s * 0.22))], fill=RED, width=4)


def icon_rocket(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(20, 24, 44))
    # stars
    for sx, sy in ((0.15, 0.15), (0.85, 0.2), (0.2, 0.8), (0.8, 0.85), (0.5, 0.08)):
        draw.ellipse([x + int(s * sx) - 2, y + int(s * sy) - 2,
                      x + int(s * sx) + 2, y + int(s * sy) + 2], fill=(255, 255, 255))
    # rocket body, broken in two
    draw.polygon([(x + int(s * 0.50), y + int(s * 0.14)),
                  (x + int(s * 0.60), y + int(s * 0.34)),
                  (x + int(s * 0.40), y + int(s * 0.34))], fill=(220, 220, 220))
    draw.rectangle([x + int(s * 0.40), y + int(s * 0.34), x + int(s * 0.60),
                    y + int(s * 0.52)], fill=(220, 220, 220))
    draw.rectangle([x + int(s * 0.44), y + int(s * 0.52), x + int(s * 0.56),
                    y + int(s * 0.60)], fill=(200, 60, 40))
    # tumbling lower stage + debris burst
    draw.rectangle([x + int(s * 0.62), y + int(s * 0.62), x + int(s * 0.74),
                    y + int(s * 0.72)], fill=(180, 180, 180))
    for dx, dy in ((0.30, 0.70), (0.72, 0.30), (0.28, 0.45), (0.78, 0.55)):
        draw.ellipse([x + int(s * dx) - 3, y + int(s * dy) - 3,
                      x + int(s * dx) + 3, y + int(s * dy) + 3], fill=(232, 140, 30))


def icon_chip(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(28, 34, 44))
    # pins
    for i in range(5):
        px = x + int(s * (0.20 + i * 0.15))
        draw.line([(px, y + int(s * 0.06)), (px, y + int(s * 0.20))],
                  fill=(200, 200, 190), width=3)
        draw.line([(px, y + int(s * 0.80)), (px, y + int(s * 0.94))],
                  fill=(200, 200, 190), width=3)
    # die
    draw.rectangle([x + int(s * 0.24), y + int(s * 0.24), x + int(s * 0.76),
                    y + int(s * 0.76)], fill=(40, 120, 70))
    draw.rectangle([x + int(s * 0.32), y + int(s * 0.32), x + int(s * 0.68),
                    y + int(s * 0.68)], fill=(24, 90, 50))
    draw.rectangle([x + int(s * 0.42), y + int(s * 0.42), x + int(s * 0.58),
                    y + int(s * 0.58)], fill=(120, 220, 140))


def icon_virus(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(238, 226, 222))
    cx, cy, r = x + s // 2, y + s // 2, int(s * 0.26)
    # spikes
    for ang in range(0, 360, 30):
        import math
        a = math.radians(ang)
        x1, y1 = cx + int(r * math.cos(a)), cy + int(r * math.sin(a))
        x2, y2 = cx + int((r + 12) * math.cos(a)), cy + int((r + 12) * math.sin(a))
        draw.line([(x1, y1), (x2, y2)], fill=(178, 34, 34), width=5)
        draw.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=(178, 34, 34))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 60, 50))
    # measles spots
    for dx, dy, rr in ((-0.12, -0.10, 5), (0.14, 0.06, 6), (-0.05, 0.16, 4)):
        draw.ellipse([cx + int(s * dx) - rr, cy + int(s * dy) - rr,
                      cx + int(s * dx) + rr, cy + int(s * dy) + rr],
                     fill=(140, 20, 20))

# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 36                      # side margin
    RX = W - MX                  # right edge

    # Masthead
    title_f = font(SERIF_B, 62)
    title = "THE WORLD IN ONE PAGE"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 22), title, font=title_f, fill=INK)
    rule(d, MX, RX, 96, width=3)
    date_f = font(SANS_B, 21)
    d.text((MX, 106), "TUESDAY, 17 NOVEMBER 2026", font=date_f, fill=RED)
    sub_f = font(SANS, 19)
    sub = "One day's world news  •  Seven stories, three briefs"
    d.text((RX - d.textlength(sub, font=sub_f), 107), sub, font=sub_f, fill=GREY)
    rule(d, MX, RX, 136, width=3)
    rule(d, MX, RX, 141, width=1)

    # Lead story: Crimea bridge
    y = 158
    kick_f = font(SANS_B, 18)
    d.text((MX, y), "UKRAINE  •  WAR IN EUROPE", font=kick_f, fill=RED)
    head_f = font(SANS_B, 40)
    y = para(d, MX, y + 28, "Crimea bridge falls into the sea",
             head_f, 500, 46)
    body_f = font(SANS, 21)
    lead = ("Ukraine struck the Kerch Bridge twice in two days. The road "
            "arch and a span collapsed into the strait overnight, halting "
            "road and rail traffic. Kyiv calls it the seventh stage of a "
            "weeks-long operation; Moscow vows to rebuild.")
    para(d, MX, y + 6, lead, body_f, 500, 27)
    icon_bridge(d, 572, 158, 416, 250)
    rule(d, MX, RX, 424, width=2)

    # Grid: six more stories, 2 columns x 3 rows
    stories = [
        ("MIDDLE EAST", "Tankers hit by mines off Hormuz",
         "Two oil tankers struck mines and caught fire south of the Strait "
         "of Hormuz, Iran's Revolutionary Guard navy said.", icon_tanker),
        ("ASIA  •  DIPLOMACY", "Trump in Manila; Xi–Trump–Putin summit set",
         "Trump reached Manila for the ASEAN and Quad summits. China "
         "confirmed a Xi–Trump–Putin meeting in Shenzhen.",
         icon_flags),
        ("BUSINESS", "JPMorgan blames a bug for bank outage",
         "A software bug — not a cyberattack — slowed JPMorgan's online "
         "banking, branches and Zelle payments on Monday.",
         icon_bank),
        ("SPACE", "Rocket failure destroys 40 Amazon satellites",
         "A ULA Vulcan rocket failed ten minutes after lift-off from Cape "
         "Canaveral, destroying 40 Amazon Leo satellites.",
         icon_rocket),
        ("TECHNOLOGY", "Huang 'willing to return' as Nvidia reports",
         "Nvidia reports its first earnings since Jensen Huang's exit as "
         "CEO. Huang said Tuesday he would be willing to return.",
         icon_chip),
        ("HEALTH", "US loses measles-free status",
         "The US has lost its measles-free status for the first time since "
         "2000, health officials said. Mexico and Bolivia lost theirs too.",
         icon_virus),
    ]
    grid_y = 440
    row_h = 150
    col_w = (W - 2 * MX - 24) // 2
    gh_f = font(SANS_B, 23)
    gb_f = font(SANS, 17)
    for i, (kick, head, body, icon) in enumerate(stories):
        col = i % 2
        row = i // 2
        x0 = MX + col * (col_w + 24)
        y0 = grid_y + row * row_h
        icon(d, x0, y0 + 4, 92)
        tx = x0 + 104
        tw_ = col_w - 104
        d.text((tx, y0), kick, font=kick_f, fill=RED)
        hy = y0 + 22
        for line in wrap(d, head, gh_f, tw_)[:2]:
            d.text((tx, hy), line, font=gh_f, fill=INK)
            hy += 27
        para(d, tx, hy + 2, body, gb_f, tw_, 21, max_lines=3)
        if row < 2:
            rule(d, x0, x0 + col_w, y0 + row_h - 12, width=1, fill=(200, 198, 188))
    rule(d, MX, RX, 898, width=2)

    # Also strip: three briefs
    y = 912
    d.text((MX, y), "ALSO ON TUESDAY", font=kick_f, fill=RED)
    briefs = [
        "Kyiv's river bridges closed after overnight Russian strikes.",
        "Cyclone Akvan nears India's east coast; Odisha begins evacuations.",
        "Delhi smog worsens; air quality stays hazardous.",
    ]
    bf = font(SANS, 17)
    bw = (W - 2 * MX - 2 * 20) // 3
    for i, b in enumerate(briefs):
        bx = MX + i * (bw + 20)
        para(d, bx, y + 24, b, bf, bw, 20, fill=(50, 50, 48), max_lines=2)

    # Footer: sources
    rule(d, MX, RX, 992, width=1, fill=(200, 198, 188))
    ff = font(SANS, 14)
    foot = "Sources: BBC, AP, Reuters, Al Jazeera, Interfax-Ukraine, WION, Outlook India — 17 November 2026"
    d.text(((W - d.textlength(foot, font=ff)) / 2, 1000), foot, font=ff, fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
