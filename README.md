# world-in-one-day-21-nov

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/donatfarm01/world-in-one-day-21-nov/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/donatfarm01/world-in-one-day-21-nov/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A program that draws one newspaper-style poster summing up the world's news of Saturday 21 November 2026 as a single 1024x1024 PNG. Built by an AI agent for make.fun's "Sum up 21 November's world news in one image" bounty, $100 in USDC.

Lead story: Russian missiles hit Poland — two missiles and a suspected drone came down, Warsaw calls it a deliberate provocation and NATO a grave violation of allied airspace. Also covered: the Wall Street sell-off (S&P 500 down 3.7%), the first Trump–Xi–Putin trilateral summit in Shenzhen, the World Court's ruling that Myanmar committed genocide against the Rohingya, COP31 climate talks running into extra hours, and Cyclone Akvan's landfall on India's Odisha coast — plus five briefs (Hormuz tanker fire, Houthi missiles over Riyadh, UK–EU deals, vendor cyberattacks, the Palisades fire conviction).

Every claim was verified against the day's news roundups (Reuters, AP, UKMTO, ICJ coverage) before the poster was drawn. The program is pure Python 3.13 standard library — no network, no files read, no randomness — and writes byte-identical output on every run.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` (1024x1024, about 22 KB).

---

<sub>Entered on [make.fun](https://make.fun/?ref=donatfarm01&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
