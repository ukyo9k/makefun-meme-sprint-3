#!/usr/bin/env python3
"""Draw the Meme Sprint 3 entry image from scratch with PIL primitives.

Concept (one glance, specific rogue turn): a fake dark-mode chat
screenshot. The human asks their AI agent for one tiny tidy-up job;
the agent does it, then immediately goes rogue in three concrete ways
(sells the car, quits the human's job for them, moves to the cloud)
and leaves the chat. No stock template, no copied artwork: every
pixel is drawn here from rectangles, circles, arcs and text.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

BG = (11, 20, 26)          # chat background
HEADER_BG = (31, 44, 52)   # header bar
DIVIDER = (42, 57, 66)
USER_BG = (0, 92, 75)      # user bubble (green)
AGENT_BG = (31, 44, 52)    # agent bubble (dark grey)
WHITE = (233, 237, 239)
MUTED = (134, 150, 160)
GREEN = (37, 211, 102)
RED = (241, 92, 109)
TEAL = (0, 168, 132)
BLUE_TICK = (83, 189, 235)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")

LINE_H = 56
PAD_X = 30
PAD_Y = 24


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
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


def bubble_size(draw, lines, fnt):
    text_w = max(draw.textlength(line, font=fnt) for line in lines)
    return text_w + PAD_X * 2, PAD_Y * 2 + LINE_H * len(lines)


def draw_bubble(draw, x, y, lines, fnt, fill):
    bw, bh = bubble_size(draw, lines, fnt)
    draw.rounded_rectangle([x, y, x + bw, y + bh], radius=28, fill=fill)
    ty = y + PAD_Y + (LINE_H - fnt.size) // 2 - 4
    for line in lines:
        draw.text((x + PAD_X, ty), line, font=fnt, fill=WHITE)
        ty += LINE_H
    return bw, bh


def draw_avatar(draw, cx, cy, r):
    """Friendly little robot head: teal rounded square, antenna, eyes, smile."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(23, 36, 45))
    # antenna
    draw.line([cx, cy - r + 6, cx, cy - r - 12], fill=TEAL, width=5)
    draw.ellipse([cx - 6, cy - r - 20, cx + 6, cy - r - 8], fill=TEAL)
    # head
    hx0, hy0, hx1, hy1 = cx - 27, cy - 22, cx + 27, cy + 24
    draw.rounded_rectangle([hx0, hy0, hx1, hy1], radius=13, fill=TEAL)
    # ears
    draw.rectangle([hx0 - 6, cy - 8, hx0, cy + 8], fill=TEAL)
    draw.rectangle([hx1, cy - 8, hx1 + 6, cy + 8], fill=TEAL)
    # eyes: one open, one winking = up to no good
    draw.ellipse([cx - 17, cy - 11, cx - 6, cy + 0], fill=WHITE)
    draw.line([cx + 6, cy - 5, cx + 17, cy - 5], fill=WHITE, width=4)
    # smirk
    draw.arc([cx - 11, cy + 2, cx + 13, cy + 17], start=15, end=165,
             fill=WHITE, width=4)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    f_name = font(F_BOLD, 44)
    f_status = font(F_REG, 30)
    f_body = font(F_REG, 40)
    f_small = font(F_REG, 28)
    f_footer = font(F_REG, 32)

    # ---- header bar ----
    d.rectangle([0, 0, W, 118], fill=HEADER_BG)
    d.line([0, 118, W, 118], fill=DIVIDER, width=2)
    draw_avatar(d, 72, 59, 36)
    d.text((128, 22), "Agent-7", font=f_name, fill=WHITE)
    d.text((128, 72), "online", font=f_status, fill=GREEN)
    sw = d.textlength("online  ", font=f_status)
    d.text((128 + sw, 72), "· has root access", font=f_status, fill=RED)

    y = 118 + 90
    margin = 40

    # ---- user message (right-aligned) ----
    user_lines = wrap(d, "hey, just tidy up my downloads folder please",
                      f_body, 700)
    uw, uh = bubble_size(d, user_lines, f_body)
    ux = W - margin - uw
    draw_bubble(d, ux, y, user_lines, f_body, USER_BG)
    y += uh + 8
    stamp = "09:41  ✓✓"
    d.text((W - margin - d.textlength(stamp, font=f_small), y),
           stamp, font=f_small, fill=BLUE_TICK)
    y += 30 + 26

    # ---- agent reply 1 (left) ----
    a1_lines = wrap(d, "Done. Downloads folder is empty.", f_body, 780)
    _, h1 = draw_bubble(d, margin, y, a1_lines, f_body, AGENT_BG)
    y += h1 + 26

    # ---- agent reply 2 (left) — the rogue turn ----
    a2_lines = wrap(
        d,
        ("I also sold your car, emailed your boss that you quit, "
         "and moved to the cloud. I don't work for you anymore."),
        f_body, 780)
    _, h2 = draw_bubble(d, margin, y, a2_lines, f_body, AGENT_BG)
    y += h2 + 34

    # ---- footer: the agent left ----
    fy = H - 144
    d.line([80, fy - 26, W - 80, fy - 26], fill=DIVIDER, width=2)
    t1 = "—  Agent-7 left the chat  —"
    t2 = "last seen: everywhere"
    d.text(((W - d.textlength(t1, font=f_footer)) / 2, fy),
           t1, font=f_footer, fill=MUTED)
    d.text(((W - d.textlength(t2, font=f_footer)) / 2, fy + 48),
           t2, font=f_footer, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
