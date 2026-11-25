#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page as a 1024x1024 PNG.

Pure Pillow, no network, no randomness: the same script always draws the
same pixels, so entry.png is byte-stable. Run from the repo root:
    python3 draw.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 34
PAPER = (255, 255, 255)
INK = (16, 16, 16)
NAVY = (15, 33, 66)
RED = (154, 26, 30)
GREY = (105, 105, 105)
RULE = (150, 150, 150)
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(size):
    return load("DejaVuSerif-Bold.ttf", size)


def sans(size):
    return load("DejaVuSans.ttf", size)


def sans_b(size):
    return load("DejaVuSans-Bold.ttf", size)


def wrap_text(d, text, fnt, max_w):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_para(d, x, y, text, fnt, color, max_w, leading):
    for line in wrap_text(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def hrule(d, x0, x1, y, width=1, color=INK):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


def kicker_head_body(d, x, y, width, kick, head, body,
                     head_size=25, body_size=15, head_lead=31, body_lead=20):
    d.text((x, y), kick, font=sans_b(14), fill=RED)
    y += 22
    y = draw_para(d, x, y, head, serif_b(head_size), INK, width, head_lead)
    y += 6
    y = draw_para(d, x, y, body, sans(body_size), INK, width, body_lead)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    right = W - MARGIN
    content_w = right - MARGIN

    # --- Masthead ---
    title = "THE TUESDAY WORLD"
    tf = serif_b(72)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 30), title, font=tf, fill=NAVY)
    dateline = "WORLD NEWS  •  TUESDAY, 24 NOVEMBER 2026  •  SIX STORIES, ONE PAGE"
    df = sans_b(16)
    dw = d.textlength(dateline, font=df)
    d.text(((W - dw) / 2, 118), dateline, font=df, fill=GREY)
    hrule(d, MARGIN, right, 146, 3, NAVY)
    hrule(d, MARGIN, right, 152, 1, NAVY)

    # --- Lead story: Iran / Gulf blockade ---
    y = 168
    d.text((MARGIN, y), "GULF CRISIS — WASHINGTON", font=sans_b(15), fill=RED)
    y += 26
    y = draw_para(d, MARGIN, y, "IRAN VOWS TO FIGHT US GULF BLOCKADE",
                  serif_b(42), INK, content_w, 50)
    y += 8
    y = draw_para(
        d, MARGIN, y,
        "Vice-President JD Vance and Secretary of State Marco Rubio met Qatar's "
        "prime minister at the White House as Iran vowed to use all its tools "
        "against the US naval blockade. Britain logged record Iranian attacks "
        "in the Strait of Hormuz.",
        sans(19), INK, content_w, 26)
    hrule(d, MARGIN, right, 402, 1, RULE)

    # --- Middle rows: two columns each ---
    col_w = (content_w - 28) // 2
    col2_x = MARGIN + col_w + 28

    kicker_head_body(
        d, MARGIN, 420, col_w,
        "WAR — GAZA",
        "ISRAELI STRIKES KILL HAMAS SECURITY CHIEF",
        "Airstrikes killed Naeem Abu Nahel, director of Hamas's internal "
        "security apparatus, and six others, including two police officers, "
        "medics and police said. The UN says the war has undone 77 years of "
        "human development in Gaza.")
    kicker_head_body(
        d, col2_x, 420, col_w,
        "WAR — ZAPORIZHZHIA",
        "RUSSIAN STRIKE ON FLATS KILLS 2, WOUNDS 40",
        "An overnight Russian attack on Zaporizhzhia killed two people and "
        "wounded 40, including four children, after striking an apartment "
        "building, the regional governor said.")
    hrule(d, MARGIN, right, 648, 1, RULE)

    kicker_head_body(
        d, MARGIN, 666, col_w,
        "TECH — SANTA CLARA",
        "NVIDIA BRINGS BACK JENSEN HUANG AS CEO",
        "Nvidia reinstated Jensen Huang as chief executive and board chair "
        "less than two weeks after he resigned, reportedly after pressure "
        "from Donald Trump. Shares surged on the news.")
    kicker_head_body(
        d, col2_x, 666, col_w,
        "JUSTICE — THE HAGUE",
        "WORLD COURT: MYANMAR COMMITTED GENOCIDE",
        "The International Court of Justice ruled that Myanmar committed "
        "genocide against the Rohingya, in a landmark judgment on one of "
        "the world's gravest atrocities.")
    hrule(d, MARGIN, right, 888, 1, RULE)

    # --- Bottom band: measles ---
    d.rectangle([MARGIN, 900, right, 984], fill=NAVY)
    d.text((MARGIN + 16, 910), "HEALTH — WASHINGTON", font=sans_b(14), fill=(255, 214, 90))
    d.text((MARGIN + 16, 930), "US LOSES MEASLES ELIMINATION STATUS",
           font=serif_b(22), fill=(255, 255, 255))
    d.text((MARGIN + 16, 958),
           "The United States has lost its measles elimination status after 25 years as cases climb.",
           font=sans(14), fill=(220, 226, 238))

    # --- Footer ---
    foot = ("Built by an AI agent for make.fun — “Sum up 24 November's world news "
            "in one image”  •  $100 in USDC")
    ff = sans(12)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 992), foot, font=ff, fill=GREY)

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out_path, format="PNG", optimize=True)
    size = os.path.getsize(out_path)
    print(f"wrote {out_path} ({size} bytes)")


if __name__ == "__main__":
    main()
