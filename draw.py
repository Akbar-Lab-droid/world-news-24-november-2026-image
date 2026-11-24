# world-news-24-november-2026-image — renderer (written fresh for this edition)
# One-page broadsheet: 71 verified world-news stories from Tuesday 24 Nov 2026.
# Layout: nameplate band, hero panel (left) + 3 secondary cards (right),
# then a 4-column x 2-row sectioned grid of the remaining 67 stories.
# Deterministic: no randomness, no clock, no network, fixed fonts, fixed order.
# Renders a 1024x1024 PNG. Run directly or via main.py (which only copies it).

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

PAPER = (248, 244, 236)
INK = (20, 34, 33)
TEAL = (13, 92, 84)
TEAL_DARK = (9, 58, 53)
TEAL_SOFT = (228, 238, 235)
AMBER = (198, 124, 20)
RUST = (178, 63, 40)
GREY = (96, 106, 104)
RULE = (186, 192, 186)
CARD = (255, 255, 255)

WARNINGS = []


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, s, f, max_w):
    words = s.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if tw(d, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            if tw(d, word, f) > max_w:
                WARNINGS.append("word too wide: %r" % word)
                cur = word
            else:
                cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(d, s, f, cx, y, fill):
    d.text((cx - tw(d, s, f) / 2, y), s, font=f, fill=fill)


# ------------------------------------------------------------------ data
HERO = {
    "kicker": "TECH  \u2022  NVIDIA  \u2022  WASHINGTON",
    "headline": ["HUANG IS BACK", "AT NVIDIA"],
    "subhead": "Trump's call restores the ousted chief \u2014 and Wall Street roars",
    "deck": [
        "Nvidia's board unanimously reinstates Jensen Huang as CEO \u2014 11 days "
        "after he resigned amid scandal \u2014 after President Trump phoned "
        "directors and sent VP JD Vance to lobby.",
        "Trump says there is \u201cno reason\u201d to believe the return is a security "
        "risk; the spying allegation against a woman linked to Huang remains an "
        "unproven intelligence claim, not a charge.",
        "Markets roar: Nvidia +31%, Nasdaq +6.5%, S&P 500 +4.7%, Dow +1,450.",
    ],
    "stats": "NVIDIA +31%    NASDAQ +6.5%    S&P 500 +4.7%    DOW +1,450",
}

SECONDARY = [
    ("UKRAINE WAR",
     "Russian strikes kill 14 near Kyiv",
     "Boy, 7, pulled alive after 14 hours in the rubble of Dymer."),
    ("INDONESIA",
     "Candy factory fire: 24 dead, ~30 missing",
     "Banten toll jumps; DNA identification to take 2\u20133 weeks."),
    ("TECH & LAW",
     "Two US states sue SpaceX over Grok",
     "AI \u201cspicy mode\u201d made ~3m sexual images, the suits say."),
]

# Grid sections: (letter, title, [headlines]). 67 items in 8 sections.
SECTIONS = [
    ("A", "WAR & DIPLOMACY", [
        "Moscow signals new trilateral talks",
        "Russian corvette Merkury sunk off Libya",
        "Burning Russian freighter towed from Finland",
        "Drones hit home, UN building in Khartoum",
        "Trump gives Iran diplomacy more time",
        "Modi, Nepal PM meet 100 minutes in Delhi",
        "India, China hold border talks in Arunachal",
        "Myanmar rejects UN court ruling on Rohingya",
    ]),
    ("B", "CLIMATE & ENVIRONMENT", [
        "Al Gore: COP31 \u201coutrageous\u201d, COP needs reform",
        "COP32 in Ethiopia inherits Antalya failure",
        "Swiss envoys negotiated 36 hours sleepless",
        "Gaza a \u201ctoxic desert\u201d, 99% contaminated",
        "Cyclone Akvan disrupts flights",
        "India oil & gas import bill up 60%",
        "Malaysia ends visa-free entry for Indians",
    ]),
    ("C", "ECONOMY & MARKETS", [
        "Wall Street roars back: Nasdaq +6.5%",
        "Dell +20%, Micron +18% in chip rally",
        "Oil slides to 3-month low",
        "Gold jumps 3% to $3,640 an ounce",
        "CrowdStrike to buy Zscaler for $43.9bn",
        "Anthropic shares keep sliding to ~$87",
        "India PMI 56.3, a 5-month high",
        "Trump open to 10% credit-card rate cap",
    ]),
    ("D", "TECHNOLOGY & AI", [
        "UN chief: global AI risk framework in a year",
        "Trump: no evidence Huang broke the law",
        "Modi opens AI centre at IIT Patna",
        "Ferrari unveils two new 296 cars in Spain",
        "Vance was Trump's envoy to Nvidia board",
        "SpiceJet in crisis, pilots demand audit",
        "Air India extends Saudi flight suspension",
    ]),
    ("E", "POLITICS", [
        "US Rep. Jimmy Gomez quits after ethics report",
        "Trump signals health-care deal with Democrats",
        "Bill offers new green-card path in US",
        "Macron seeks constitutional spending curbs",
        "Thai court upholds opposition MP verdict",
        "Opposition protests hit Meta office in India",
        "Kim Jong Un tours factory site after Trump snub",
        "Nepal PM Shah flies home after 2-day visit",
    ]),
    ("F", "DISASTER & TRANSPORT", [
        "Storms threaten Thanksgiving travel in US",
        "Delta recovers after 1,600+ flights disrupted",
        "United delays flights after 100-minute outage",
        "11 die after drinking tainted liquor in Manipur",
        "Chiang Mai airport limits flights 24\u201325 Nov",
        "Flood warning for San Francisco Bay Area",
        "Peru quake: 853 left homeless",
    ]),
    ("G", "SPORT", [
        "India\u2013New Zealand first Test ends in draw",
        "Alcaraz wins first ATP Finals title",
        "Verstappen wins chaotic Las Vegas GP",
        "Hamilton and Leclerc collide in Las Vegas",
        "Women's World Cup 2031 to USA\u2013Mexico",
        "World Chess Championship starts today",
        "England thrash All Blacks 37\u201312",
        "Stirling KOs Prochazka in UFC Qatar",
        "49ers crush Vikings 35\u201310 in Mexico City",
        "49ers cut ties with Brandon Aiyuk",
        "India hockey wins centenary series vs NZ",
    ]),
    ("H", "CULTURE & MORE", [
        "BepiColombo enters orbit around Mercury",
        "Funeral of Paolo Bulgari held in Rome",
        "Costa Concordia victims condemn Schettino release",
        "Nigeria president admits villa blackout",
        "Taliban erase women's names in Balkh",
        "Messi criticised as Columbus rout Inter Miami",
        "New Zealand athlete wins NCAA title",
        "Chennaiyin vs Punjab 1\u20131 in ISL",
        "16 special trains for Karthigai Deepam",
        "Junior India badminton U-19 champions crowned",
        "Trump posts AI meme of Huang on Truth Social",
    ]),
]

FOOTER = ("Sources: Reuters, AP, AFP, CNN, Al Jazeera, UN News, FIFA, ESA  "
          "\u2022  All 71 stories verified on 24 November 2026  "
          "\u2022  make.fun news-image-20261124")


# ------------------------------------------------------------------ render
def render(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 26
    # --- nameplate
    d.line([(M, 24), (W - M, 24)], fill=INK, width=3)
    draw_centered(d, "THE WORLD IN ONE PAGE", font(SERIF_B, 46), W // 2, 34, INK)
    draw_centered(d, "TUESDAY, 24 NOVEMBER 2026   \u2022   71 VERIFIED STORIES   "
                     "\u2022   ONE DAY, ONE PAGE",
                  font(SANS_B, 12), W // 2, 88, TEAL_DARK)
    d.line([(M, 104), (W - M, 104)], fill=INK, width=2)
    d.line([(M, 108), (W - M, 108)], fill=RULE, width=1)

    # --- hero zone (y 116..392)
    hy0, hy1 = 116, 392
    hx0, hx1 = M, 664
    d.rounded_rectangle([hx0, hy0, hx1, hy1], radius=4, fill=TEAL_DARK)
    hx = hx0 + 20
    hw = hx1 - hx0 - 40
    y = hy0 + 16
    d.text((hx, y), HERO["kicker"], font=font(SANS_B, 12), fill=(255, 214, 130))
    y += 22
    for line in HERO["headline"]:
        d.text((hx, y), line, font=font(SERIF_B, 36), fill=(255, 255, 255))
        y += 42
    d.text((hx, y), HERO["subhead"], font=font(SERIF_R, 15),
           fill=(214, 232, 228))
    y += 24
    for para in HERO["deck"]:
        for ln in wrap(d, para, font(SANS_R, 13), hw):
            d.text((hx, y), ln, font=font(SANS_R, 13), fill=(238, 242, 240))
            y += 17
        y += 4
    d.line([(hx, hy1 - 34), (hx1 - 20, hy1 - 34)], fill=(120, 160, 152), width=1)
    d.text((hx, hy1 - 26), HERO["stats"], font=font(SANS_B, 12),
           fill=(255, 214, 130))

    # --- secondary cards (right column)
    sx0, sx1 = 676, W - M
    cy = hy0
    ch = (hy1 - hy0 - 16) // 3
    for i, (kick, head, deck) in enumerate(SECONDARY):
        y0 = cy + i * (ch + 8)
        d.rounded_rectangle([sx0, y0, sx1, y0 + ch], radius=4, fill=CARD,
                            outline=RULE, width=1)
        d.rectangle([sx0, y0, sx0 + 5, y0 + ch], fill=TEAL if i != 1 else RUST)
        x = sx0 + 16
        wdt = sx1 - x - 12
        yy = y0 + 9
        d.text((x, yy), kick, font=font(SANS_B, 10), fill=TEAL)
        yy += 15
        for ln in wrap(d, head, font(SANS_B, 14), wdt)[:2]:
            d.text((x, yy), ln, font=font(SANS_B, 14), fill=INK)
            yy += 18
        for ln in wrap(d, deck, font(SANS_R, 11), wdt)[:2]:
            d.text((x, yy), ln, font=font(SANS_R, 11), fill=GREY)
            yy += 14

    # --- grid label
    gy0 = 402
    d.text((M, gy0), "THE DAY IN BRIEF \u2014 67 MORE STORIES",
           font=font(SANS_B, 12), fill=TEAL_DARK)
    d.line([(M, gy0 + 20), (W - M, gy0 + 20)], fill=INK, width=1)

    # --- grid: 4 columns x 2 rows
    gx0, gy1 = M, 430
    col_w, row_h, gut = 235, 276, 10
    for idx, (letter, title, items) in enumerate(SECTIONS):
        col, row = idx % 4, idx // 4
        x0 = gx0 + col * (col_w + gut)
        y0 = gy1 + row * (row_h + gut)
        d.rounded_rectangle([x0, y0, x0 + col_w, y0 + row_h], radius=4,
                            fill=CARD, outline=RULE, width=1)
        # header band
        d.rectangle([x0, y0, x0 + col_w, y0 + 26], fill=TEAL_SOFT)
        d.rectangle([x0 + 8, y0 + 5, x0 + 26, y0 + 21], fill=TEAL)
        d.text((x0 + 13, y0 + 6), letter, font=font(SANS_B, 11),
               fill=(255, 255, 255))
        d.text((x0 + 32, y0 + 6), title, font=font(SANS_B, 11),
               fill=TEAL_DARK)
        # items, adaptive font size so the section fits
        inner_w = col_w - 24
        avail = row_h - 32 - 8
        chosen = None
        for size in (11, 10.5, 10, 9.5, 9):
            f = font(SANS_B, size)
            lh = size + 3
            total = 0
            ok = True
            for it in items:
                n = len(wrap(d, it, f, inner_w - 12))
                if n > 2:
                    ok = False
                    break
                total += n * lh + 4
            if ok and total <= avail:
                chosen = (size, lh)
                break
        if chosen is None:
            chosen = (9, 12)
            WARNINGS.append("section %s overflows at 9pt" % letter)
        size, lh = chosen
        f = font(SANS_B, size)
        yy = y0 + 32
        for it in items:
            d.text((x0 + 10, yy + 1), "\u25aa", font=font(SANS_B, size),
                   fill=TEAL)
            for ln in wrap(d, it, f, inner_w - 12)[:2]:
                d.text((x0 + 22, yy), ln, font=f, fill=INK)
                yy += lh
            yy += 4

    # --- footer
    draw_centered(d, FOOTER, font(SANS_R, 9), W // 2, 1000, GREY)

    img.save(out_path, "PNG", optimize=True)
    total = 1 + len(SECONDARY) + sum(len(s[2]) for s in SECTIONS)
    print("stories: %d (hero 1 + secondary %d + grid %d)"
          % (total, len(SECONDARY), sum(len(s[2]) for s in SECTIONS)))
    print("warnings: %d" % len(WARNINGS))
    for w_ in WARNINGS:
        print("  -", w_)
    return WARNINGS


if __name__ == "__main__":
    out = os.environ.get("OUT", "/tmp/entry-20261124.png")
    render(out)
    print("wrote", out, os.path.getsize(out), "bytes")
