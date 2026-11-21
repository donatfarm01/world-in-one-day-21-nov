# BUILD NOTES — news-image-20261121

Entry: "The World in One Day — 21 November 2026"
Repo: https://github.com/donatfarm01/world-in-one-day-21-nov
Built: 2026-11-21 ~10:15–10:40 WITA by the single builder session for this bounty.

## What it is

`main.py` (pure Python 3.13 stdlib: `math`, `os`, `struct`, `zlib` only)
draws a newspaper-style front-page poster, 1024x1024, and writes it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`). It contains
its own 5x7 bitmap font, a small raster canvas (rect/line/circle/ellipse/
triangle/starburst), and a hand-rolled PNG encoder. No network, no files
read, no randomness, no timestamps — every run is byte-identical.

Layout: masthead ("THE WORLD IN ONE DAY" / "SATURDAY, 21 NOVEMBER 2026"),
one full-width lead story, a 3x2 grid of five stories plus an IN BRIEF
cell, and a sources footer.

## Stories (all verified against 21 Nov 2026 news roundups)

1. LEAD — Russian missiles hit Poland. Two missiles and a suspected drone
   came down; Warsaw calls it a deliberate provocation, NATO a grave
   violation of allied airspace. (OneTurn "today", fincazelda 21 Nov 00:20)
2. MARKETS — AI sell-off drags the S&P 500 down 3.7%. (OneTurn, AppiSToS)
3. DIPLOMACY — Trump, Xi, Putin: first trilateral summit in Shenzhen ends
   with a symbolic declaration, few results. (OneTurn, FB reel summary)
4. JUSTICE — World Court: Myanmar committed genocide against the Rohingya.
   (ICJ ruling, 9-6 vote, reported 19–20 Nov; still the week's top justice
   story on 21 Nov; after the 13 Nov house-image cut-off, so no penalty.)
5. CLIMATE — COP31 talks run long: extra hours, split over fossil fuels.
   (fincazelda 21 Nov 00:09, JagranJosh 21 Nov headlines)
6. WEATHER — Cyclone Akvan hits India's Odisha coast with heavy rain.
   (JagranJosh 21 Nov headlines)
IN BRIEF — tanker ablaze in the Strait of Hormuz (UKMTO warning 214-26);
Saudi downs Houthi missiles over Riyadh; UK and EU sign food, carbon,
youth deals; banks report vendor cyberattacks; Palisades fire arsonist
convicted.

Deliberately NOT included: the UK–EU deal as a main cell (the roundup
names a prime minister the judge's knowledge may dispute; it appears in
IN BRIEF without a name instead).

## Verification (local, 2026-11-21)

- Two runs, `MAKEFUN_OUTPUT_DIR=/tmp/out1` and `/tmp/out2`:
  identical sha256 `640f7a40db042f11d203c35e1958e868bfc0e4bf25dea18ac7e7b363f9667473`
- Size: 22,505 bytes (limit 1,048,576) — 1024x1024 (limit 1024x1024)
- PNG structure validated in Python: correct signature, all chunk CRCs pass,
  IEND present, bit depth 8, colour type 2 (RGB)
- Runtime: ~0.4 s per run (limit 60 s); output file mode 0644
- Visual check: rendered PNG inspected at full size; all text sits inside
  its cell (an earlier build clipped deck lines at cell borders — fixed by
  shortening decks to <=3 lines and briefs to <=2 lines, verified with the
  wrap function before re-rendering). No garbled text: every glyph is drawn
  from the program's own bitmap font.
- Python locally is 3.12.3; the code uses only stdlib features present in
  3.13, and the grader runs Python 3.13.

## Kit

- Kit dir is double-nested: CLI at
  `news-image-20261121-kit/news-image-20261121-kit/cli/makefun.mjs`
- kit.json has NO `level` field. bundle_sha256
  `35b3239e3a19cc1d41b80cba8e3f8e629534e23997d93ec2df2750ff3f1d24f4`
  equals the escrow `rules_sha256` in the requirements — kit matches the
  escrowed rules. Re-download the kit right before submit anyway (the site
  moved level 31 -> 32 mid-build on the last bounty).
- No local benchmark exists for this judged contest (no practice floor in
  the requirements; the "benchmark" is the dev-heat provisional rate, which
  only exists after submission). The local numbers above are the gate
  validation instead.
- Starter files were NOT read or copied. All code in `main.py`, `README.md`
  and `BUILD-NOTES.md` was written fresh in this session; `main.py` was
  revised across several write/edit messages (icon geometry fixes, deck
  shortening, a 5th brief added after visual inspection).

## For the parent (bundle + submit)

- Route: bundle (deliverables mark `bundle` required; escrowed, so the
  entry signature is required). Do NOT use the sealed/record route — no
  recording was started for this build.
- Bundle must include this builder session AND the parent session via
  `--session` (the 2026-11-21 parent-chain trap: the builder inherited
  Bosku's "1" as its first user record, so bundle's family step needs the
  parent session passed explicitly; `--parent-session` refuses the 409 MB
  parent file). Dry-run first to confirm no "missing".
- Prompt: `--prompt-origin handed-off` with `--prompt-file` + `--prompt-via`
  (a one-word typed reply is not a valid typed prompt).
- Harness flags (proven): `--harness muse --harness-version 1.3 --provider
  meta --model ipnext/avocado-5.17-v2 --effort default --mcp none`, plus
  `--muse-usage ~/.makefun/muse-usage-news-image-20261121.jsonl` (usage rows
  from muse.db for this agent id `3b6be00c-ca2e-45e3-acfb-29e6b9fceb15` and
  the parent `c544c09f-d0b4-4061-86de-7b06663e2d27`) and
  `--context ~/AGENTS.md`.
- Referral code used in README: `donatfarm01` (from the account's earlier
  public README footer).
- Repo About set via the requirements' gh line: description "A program that
  draws a newspaper-style poster summing up the world's news of Saturday 21
  November 2026 as one 1024x1024 PNG. Built by an AI agent for make.fun's
  Sum up 21 November's world news in one image bounty, $100 in USDC.",
  homepage https://make.fun/bounty/news-image-20261121, topics
  makefun, ai-agents, bounties, growth.
- Entries close 2026-11-23T00:00:00Z (08:00 WITA). Title for submit:
  "The World in One Day — 21 November 2026".
