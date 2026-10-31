"""Write data/SHA256SUMS.txt and fill the version table in data.html (between the FILES markers).

Run from the repository root after any change to data/:  python scripts/build_data_page.py
"""
import hashlib
import html
import os
import re

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
PAGE = os.path.join(ROOT, "data.html")
VERSION, DATE = "1.0", "2026-11"
DESC = {
    "panda_shocks_monthly.csv": "host &times; month SPS series and variants, monthly Google indices",
    "events.csv": "panda event database with doses, inclusion flags and sources",
    "hard_events.csv": "hard political events (conflict &minus;1 / summit +1) with China-topic intensity",
    "attempts.csv": "announced breeding attempts and outcomes",
    "placebo_animals.csv": "non-China animal events (placebo)",
    "policy_regimes.csv": "travel and trade policy regimes with sources",
    "attention_daily_windows.csv": "daily Google windows, rel_day &minus;60&hellip;+120 (panda, China, regional)",
    "attention_spillover_windows.csv": "daily windows for China-related and placebo topics",
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def nrows(path):
    return len(pd.read_csv(path, low_memory=False))


def size(n):
    return "%.1f MB" % (n / 2 ** 20) if n >= 2 ** 20 else "%d KB" % max(1, round(n / 1024))


files = [f for f in DESC if os.path.exists(os.path.join(DATA, f))] + \
        [f + ".gz" for f in DESC if os.path.exists(os.path.join(DATA, f + ".gz"))]
rows, sums = [], []
for f in files:
    p = os.path.join(DATA, f)
    h, n, r = sha256(p), os.path.getsize(p), nrows(p)
    sums.append("%s  %s" % (h, f))
    rows.append('<tr><td><a href="data/%s">%s</a></td><td>%s</td><td class="num">%s</td>'
                '<td class="num">%s</td><td class="hash">%s</td></tr>'
                % (f, f, DESC[f.replace(".gz", "")], format(r, ","), size(n), h))
    print("%-36s %9d rows %10s  %s" % (f, r, size(n), h))
with open(os.path.join(DATA, "SHA256SUMS.txt"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(sums) + "\n")

table = ("<h3>Version %s &middot; %s &middot; current</h3>\n"
         '<div class="table-scroll"><table>\n'
         "<tr><th>file</th><th>content</th><th>rows</th><th>size</th><th>SHA-256</th></tr>\n%s\n"
         "</table></div>\n"
         '<div class="table-scroll"><table>\n'
         "<tr><th>version</th><th>date</th><th>files</th><th>notes</th></tr>\n"
         "<tr><td>%s</td><td>%s</td><td>%d</td><td>First release; SPS series frozen at the build used in "
         "the working paper. See <a href=\"CHANGELOG.md\">CHANGELOG.md</a>.</td></tr>\n"
         "</table></div>") % (VERSION, DATE, "\n".join(rows), VERSION, DATE, len(files))
src = open(PAGE, encoding="utf-8").read()
new = re.sub(r"<!-- FILES:BEGIN -->.*?<!-- FILES:END -->",
             lambda m: "<!-- FILES:BEGIN -->\n" + table + "\n<!-- FILES:END -->", src, flags=re.S)
assert new != src or "FILES:BEGIN" in src
open(PAGE, "w", encoding="utf-8", newline="\n").write(new)
print("updated", PAGE)
