# The World in One Page — Tuesday 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Akbar-Lab-Droid/world-news-24-november-2026-image/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Akbar-Lab-Droid/world-news-24-november-2026-image/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A single 1024×1024 broadsheet image summing up the world news of
**Tuesday 24 November 2026** — 71 verified stories in one page.

## The front page

- **Hero:** Jensen Huang returns as Nvidia CEO after President Trump phoned
  the board and sent VP JD Vance to lobby — Nvidia +31%, Nasdaq +6.5%,
  S&P 500 +4.7%, Dow +1,450. The spying allegation against a woman linked
  to Huang remains an unproven intelligence claim, not a charge.
- **Secondary:** Russian strikes kill 14 near Kyiv (a 7-year-old boy pulled
  alive after 14 hours in rubble); a candy factory fire in Banten, Indonesia
  leaves 24 dead and ~30 missing; Virginia and Oregon sue SpaceX over Grok's
  "spicy mode" generating sexual images.
- **Grid:** 67 more stories in 8 sections — War & Diplomacy, Climate &
  Environment, Economy & Markets, Technology & AI, Politics, Disaster &
  Transport, Sport, and Culture & More.

Every story was verified against wire and major-outlet reporting
(Reuters, AP, AFP, CNN, Al Jazeera, UN News, FIFA, ESA) on 24 November 2026.
The lead story was checked against five independent sources.

## Run

`main.py` only copies the pre-rendered `entry.png` to `/output/entry.png`
(standard library only, no network, deterministic — two runs write
byte-identical output):

```bash
python3 main.py        # writes /output/entry.png (1024x1024, < 1 MiB)
```

To re-render the page from the story data (needs Python 3, Pillow and the
Liberation fonts, present on most Linux systems):

```bash
python3 draw.py        # renders entry.png (1024x1024, deterministic)
```

## Files

- `entry.png` — the broadsheet image (1024×1024, 71 stories)
- `main.py` — the entry program: copies `entry.png` to `/output/entry.png`
- `draw.py` — the renderer: layout, text and all 71 stories, written from
  verified reporting of 24 November 2026
