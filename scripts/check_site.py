"""Validate the site pages (*.html at the repository root): balanced tags (html.parser) and every relative href/src resolves to a file.

Run from the repository root:  python scripts/check_site.py
"""
import glob
import os
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Check(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors, self.refs, self.ids = [], [], [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))
        for k in ("href", "src"):
            if a.get(k):
                self.refs.append((a[k], self.getpos()))
        if tag == "img" and "alt" not in a:
            self.errors.append("img without alt at %s" % (self.getpos(),))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1][0] != tag:
            self.errors.append("unexpected </%s> at %s (open: %s)" % (tag, self.getpos(),
                                                                       self.stack[-1] if self.stack else None))
            return
        self.stack.pop()


bad = 0
for fn in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
    c = Check()
    c.feed(open(fn, encoding="utf-8").read())
    c.close()
    errs = list(c.errors) + ["unclosed <%s> from %s" % t for t in c.stack]
    n_rel = 0
    for ref, pos in c.refs:
        u = urlparse(ref)
        if u.scheme in ("http", "https", "mailto") or ref.startswith("#"):
            continue
        n_rel += 1
        target = os.path.normpath(os.path.join(os.path.dirname(fn), unquote(u.path)))
        if not os.path.exists(target):
            errs.append("broken link %s at %s" % (ref, pos))
    print("%-20s %s  (%d relative links/images checked)" % (os.path.basename(fn), "OK" if not errs else "FAIL", n_rel))
    for e in errs:
        print("    ", e)
    bad += len(errs)
sys.exit(1 if bad else 0)
