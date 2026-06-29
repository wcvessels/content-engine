#!/usr/bin/env python3
"""render-doc: doc-model (docmodel-1.0) -> self-contained HTML + PDF.

The single shared renderer for every content-engine lane. It consumes ONE
contract, the docmodel-1.0 object pinned in
`_standards/doc-model-schema.md`, and produces a self-contained HTML file
(inline CSS, base64 images, sticky TOC, collapsible sections) and a PDF
derived from that same HTML via headless Chrome or Edge.

Dependencies: Python stdlib + Pillow. NO markdown library (a ~30-line inline
escaper handles **bold** / *italic* / `code` / [text](url)). NO PDF library
(Chrome/Edge --print-to-pdf is the path).

Public API:
    build_html(docmodel, manifest_path=None, css=None) -> str
    build_pdf(html, out_pdf_path, html_path=None) -> str
    resolve_frame(frame_index, manifest_path, crop=None, max_px=1200) -> str|None
    render(docmodel, out_dir, slug, manifest_path=None, targets=("html","pdf"))
    build_docx(...)  -> documented stub, NOT implemented (pandoc path)

House rule: zero em dash characters anywhere in output or source.
"""

from __future__ import annotations

import base64
import html as _html
import io
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover - Pillow is a hard dependency
    Image = None


# Brand assets baked in so the renderer stays self-contained (no _config read
# at render time). Source of truth: _config/brand/logo/. Keep these in sync if
# the brand changes; the _config loader bridge is a tracked follow-up.
# favicon-32.png (content-engine mark on indigo).
_FAVICON_DATA_URI = (
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADE0lEQVR4AcRV"
    "3UtUQRw9M7ZqVK6rZJppkgp+ItmXu2ovWWAFtpbWg6SVD5GBmJgEUYZE0ZohRhCUbB8P+VL05h8QafbBIqY"
    "mJSLaU2qIbsm2O81d3FV27+wdl0WHe5h7z+835xzm3stQLI3cojuGLGPbrWyj5V2W0bKYbWpjoYRbU9E2WV"
    "qyjO0xS7ZwB8g0Wswul26MENwAIYWEkHBPQ6hmt6aiDXKTEOf3jIK2ckWbpu9t38VTvOAP0RxrdBFDGGHPd"
    "0z3UqlO52wFIZvWyHnZhnu6QFooCPZgnQYByaUAScE6DcZYCiVAxGr9dboIxMXFIyEhURN6vQF8l6E2+Iep5"
    "zugVhJzhFJkZ+YgaUcytvMAWkhLTUdCfKJQcNUBovXRCNsQJhRUKxgM3t/erywMQPi72Z+fhIvnjLh0weRF9"
    "Zk8mI/uVMWh4gRs2azzM3E4HH6chxAGqCjLQ1dnJS7XcvPzPMQSaqvycaI0WRVnK9Nw+1q+R1tqFgYoLcmQ"
    "EvBt0keFIyNd70sLn4UB+C8iXBTKgjDAShPrs5coM5/2g8Kv7AvmXipAMMKya6QC1FRX4e2bbj8ovKyRqE8q"
    "QFPzdWyNTxHCVFwi0tfkpQKcLC9DU2O9EA31dZpGogapAAUH9uFqU4MQFafMIn1NXirAv99jWBiwYn6gSxWL"
    "U72aRqIGqQBz/Q/cxkoINcz13hXpa/JSAQjhB0MAKdff2QDVwCWpAIElAlftdjumfk4Km6QC0MhYoYBSoJEx"
    "yuTF6OgIPn/pd2N4ZBD2hXlvzfdGKkCUqRkxRzphONyhithjT711pZ+FAcYnZrwiJCwSurg8hG/brQq6cXmH"
    "GAPGxqe9a7VuhAFevbbhk20SiqCWiKc+M/sHj629mJ61eyjNmTKwb2pdoz9+oaauG7lF95FTKIeDxx/h4ZP3"
    "anKqHD/yP/AdIDbV6tqQNgoHbeX7LL9noQrGmJ0yVwcd+njlK2M0+NMkyECK52Bf8zB/BcBQX6OVuJxZ/J30"
    "8G9ign/IziB1/ZZ5CEXTrc1Yj+KleCq1/wAAAP//QpB88AAAAAZJREFUAwAfnEj+KLR3JQAAAABJRU5Erk"
    "Jggg=="
)

# content-engine mark (the new brand glyph: two pages composing into a finished
# document, amber screenshot block). Inlined into the title-page lockup.
# Source: _config/brand/logo/mark.svg. The #5E6CC2 back-card tint is a
# logo-only color, intentionally not a brand token.
_MARK_SVG = (
    '<svg width="30" height="30" viewBox="0 0 64 64" fill="none" aria-hidden="true">'
    '<rect width="64" height="64" rx="14" fill="#2B3A8C"/>'
    '<rect x="25.5" y="13" width="26" height="33" rx="3.5" fill="#5E6CC2"/>'
    '<rect x="12.5" y="19" width="30" height="35" rx="4" fill="#FFFFFF"/>'
    '<rect x="18.5" y="26.5" width="13" height="2.8" rx="1.4" fill="#14171F"/>'
    '<rect x="18.5" y="32.2" width="17.5" height="2.8" rx="1.4" fill="#14171F"/>'
    '<rect x="18.5" y="39.2" width="17.5" height="9.2" rx="2" fill="#E8A33D"/>'
    '</svg>'
)


# ----------------------------------------------------------------------------
# 1. Inline markdown -> HTML (no library; ~30 lines)
# ----------------------------------------------------------------------------
# Grammar (docmodel-1.0 prose/callout/list items): **bold**, *italic*,
# `code`, [text](url). NO block-level HTML, headings, tables, or fences.
# Order matters: escape first, then code (so markup inside code is literal),
# then links, bold, italic.

_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
_CODE_RE = re.compile(r"`([^`]+)`")


def md_inline(text):
    """Convert an inline-markdown string to safe HTML.

    Escapes HTML first so user text cannot inject markup, then applies the
    four inline forms. Code spans are extracted to placeholders before the
    other passes so emphasis markers inside code stay literal.
    """
    if text is None:
        return ""
    s = _html.escape(str(text), quote=False)

    # Pull code spans out so bold/italic do not touch their contents.
    codes = []

    def _stash_code(m):
        codes.append(m.group(1))
        return "\x00CODE%d\x00" % (len(codes) - 1)

    s = _CODE_RE.sub(_stash_code, s)

    # Links: [text](url). The url is attribute-escaped.
    def _link(m):
        label, url = m.group(1), m.group(2)
        safe_url = _html.escape(url, quote=True)
        return '<a href="%s">%s</a>' % (safe_url, label)

    s = _LINK_RE.sub(_link, s)
    s = _BOLD_RE.sub(r"<strong>\1</strong>", s)
    s = _ITALIC_RE.sub(r"<em>\1</em>", s)

    # Restore code spans.
    for i, code in enumerate(codes):
        s = s.replace("\x00CODE%d\x00" % i, "<code>%s</code>" % code)
    return s


# ----------------------------------------------------------------------------
# 2. Frame resolution + crop + downscale + base64 (the screenshot pipeline)
# ----------------------------------------------------------------------------

def _frame_file_for_index(frame_index, manifest_path):
    """Return (abs_path, file_name) for a frame_index, or (None, None).

    frames_dir resolves RELATIVE TO THE MANIFEST FILE'S OWN DIRECTORY, never
    cwd (docmodel-schema section 5). If 01-ingest already copied frames into
    an in-bundle dir, point manifest_path at that bundle's manifest.
    """
    if manifest_path is None:
        return None, None
    manifest_path = os.path.abspath(manifest_path)
    try:
        with open(manifest_path, "r", encoding="utf-8") as fh:
            manifest = json.load(fh)
    except (OSError, ValueError):
        return None, None

    index_to_file = {}
    for fr in manifest.get("frames", []):
        index_to_file[fr.get("index")] = fr.get("file")
    file_name = index_to_file.get(frame_index)
    if not file_name:
        return None, None

    frames_dir = manifest.get("artifacts", {}).get("frames_dir", "")
    base = os.path.dirname(manifest_path)
    abs_dir = frames_dir if os.path.isabs(frames_dir) else os.path.join(base, frames_dir)
    abs_path = os.path.join(abs_dir, os.path.basename(file_name))
    return abs_path, os.path.basename(file_name)


def _apply_crop(img, crop):
    """Apply a normalized crop box to a Pillow image. Returns a new image.

    crop = {"x","y","w","h"} normalized 0..1, x,y = top-left. An out-of-range
    or malformed box is treated as null (full frame) per the schema.
    """
    if not crop or not isinstance(crop, dict):
        return img
    try:
        x = float(crop["x"]); y = float(crop["y"])
        w = float(crop["w"]); h = float(crop["h"])
    except (KeyError, TypeError, ValueError):
        return img
    # Validity: x,y in [0,1]; w,h in (0,1]; x+w<=1; y+h<=1 (small epsilon).
    eps = 1e-6
    if not (0 <= x <= 1 and 0 <= y <= 1 and 0 < w <= 1 and 0 < h <= 1):
        return img
    if x + w > 1 + eps or y + h > 1 + eps:
        return img
    W, H = img.size
    box = (int(round(x * W)), int(round(y * H)),
           int(round((x + w) * W)), int(round((y + h) * H)))
    # Guard against a degenerate (zero-area) box after rounding.
    if box[2] <= box[0] or box[3] <= box[1]:
        return img
    return img.crop(box)


def resolve_frame(frame_index, manifest_path, crop=None, max_px=1200):
    """Resolve a frame to a base64 data-URI, applying crop then downscale.

    Returns a "data:image/jpeg;base64,..." string, or None if the frame
    cannot be resolved (caller emits a visible placeholder, never hard-fails).
    Crop is applied to a COPY; the original frame file is never modified.
    """
    abs_path, _name = _frame_file_for_index(frame_index, manifest_path)
    if not abs_path or not os.path.exists(abs_path):
        return None
    if Image is None:
        # Without Pillow we can still inline the raw bytes (no crop/downscale).
        if crop:
            return None
        try:
            with open(abs_path, "rb") as fh:
                raw = fh.read()
        except OSError:
            return None
        return "data:image/jpeg;base64," + base64.b64encode(raw).decode("ascii")

    try:
        img = Image.open(abs_path)
        img.load()
    except (OSError, ValueError):
        return None

    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    img = _apply_crop(img, crop)

    # Optional downscale: cap the long edge at max_px to keep the file sane.
    if max_px and max(img.size) > max_px:
        scale = max_px / float(max(img.size))
        new_size = (max(1, int(img.size[0] * scale)), max(1, int(img.size[1] * scale)))
        img = img.resize(new_size, Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


# ----------------------------------------------------------------------------
# 3. Block + section rendering
# ----------------------------------------------------------------------------

_CALLOUT_VARIANTS = {"tip", "warning", "note", "prereq"}


def _render_block(block, manifest_path):
    """Render one doc-model block to HTML. Unknown types degrade to prose."""
    btype = block.get("type")

    if btype == "prose":
        return '<p class="prose">%s</p>' % md_inline(block.get("md", ""))

    if btype == "list":
        ordered = bool(block.get("ordered"))
        tag = "ol" if ordered else "ul"
        items = block.get("items", []) or []
        lis = "".join("<li>%s</li>" % md_inline(it) for it in items)
        return "<%s class=\"doc-list\">%s</%s>" % (tag, lis, tag)

    if btype == "callout":
        variant = block.get("variant", "note")
        if variant not in _CALLOUT_VARIANTS:
            variant = "note"
        label = {"tip": "Tip", "warning": "Warning",
                 "note": "Note", "prereq": "Before you start"}[variant]
        return ('<aside class="callout callout-%s">'
                '<span class="callout-label">%s</span>'
                '<span class="callout-body">%s</span></aside>'
                % (variant, label, md_inline(block.get("md", ""))))

    if btype == "screenshot":
        return _render_screenshot(block, manifest_path)

    # Unknown type: degrade to plain prose if it carries md, else skip.
    if block.get("md"):
        return '<p class="prose">%s</p>' % md_inline(block.get("md"))
    return ""


def _render_screenshot(block, manifest_path):
    frame_index = block.get("frame_index")
    caption = block.get("caption")
    alt = block.get("alt") or caption or ""
    crop = block.get("crop")

    data_uri = resolve_frame(frame_index, manifest_path, crop=crop)
    if data_uri is None:
        # Missing-frame guard: visible placeholder, never hard-fail.
        note = "frame %s unavailable" % frame_index
        cap = ('<figcaption class="caption">%s</figcaption>' % md_inline(caption)) if caption else ""
        return ('<figure class="screenshot missing">'
                '<div class="frame-placeholder">[screenshot %s]</div>%s</figure>'
                % (_html.escape(note), cap))

    cap = ('<figcaption class="caption">%s</figcaption>' % md_inline(caption)) if caption else ""
    return ('<figure class="screenshot">'
            '<img src="%s" alt="%s" loading="lazy">%s</figure>'
            % (data_uri, _html.escape(str(alt), quote=True), cap))


def _section_id(section, idx):
    sid = section.get("id") or ("section-%d" % idx)
    # Keep ids anchor-safe.
    return re.sub(r"[^A-Za-z0-9_-]", "-", str(sid))


def _render_section(section, idx, manifest_path):
    sid = _section_id(section, idx)
    level = section.get("level", 1)
    try:
        level = int(level)
    except (TypeError, ValueError):
        level = 1
    level = 1 if level < 1 else (2 if level > 2 else level)
    kind = section.get("kind", "")
    kind_class = (" kind-%s" % re.sub(r"[^a-z]", "", str(kind).lower())) if kind else ""

    heading = _html.escape(str(section.get("heading", "")))
    htag = "h2" if level == 1 else "h3"

    blocks_html = "".join(
        _render_block(b, manifest_path) for b in section.get("blocks", []) or []
    )

    # Collapsible via native <details open> so it also prints expanded.
    return (
        '<section id="%s" class="doc-section level-%d%s">'
        '<details open><summary><%s class="section-heading">%s</%s></summary>'
        '<div class="section-body">%s</div></details></section>'
        % (sid, level, kind_class, htag, heading, htag, blocks_html)
    )


def _render_toc(sections):
    """Sticky in-page anchor TOC from sections[] (no JS required)."""
    items = []
    for i, sec in enumerate(sections):
        sid = _section_id(sec, i)
        level = sec.get("level", 1)
        try:
            level = int(level)
        except (TypeError, ValueError):
            level = 1
        cls = "toc-l1" if level <= 1 else "toc-l2"
        label = _html.escape(str(sec.get("heading", "")))
        items.append('<li class="%s"><a href="#%s">%s</a></li>' % (cls, sid, label))
    return '<nav class="toc"><div class="toc-title">Contents</div><ul>%s</ul></nav>' % "".join(items)


# ----------------------------------------------------------------------------
# 4. Title page + meta
# ----------------------------------------------------------------------------

def _render_title_page(meta, footer):
    title = _html.escape(str(meta.get("title", "Untitled")))
    subtitle = meta.get("subtitle")
    author = meta.get("author", "")
    date = meta.get("date", "")
    audience = meta.get("audience")
    doc_type = meta.get("doc_type", "")

    parts = ['<header class="title-page">']
    # Brand letterhead: indigo+amber accent rule, then the mark + wordmark lockup.
    parts.append('<div class="title-accent"><span class="seg-primary"></span>'
                 '<span class="seg-accent"></span></div>')
    parts.append('<div class="brand-lockup">%s'
                 '<span class="wordmark">content<span class="hy">-</span>engine</span></div>'
                 % _MARK_SVG)
    parts.append('<div class="brand-mark">%s</div>' % _html.escape(str(doc_type).upper()) if doc_type else "")
    parts.append('<h1 class="doc-title">%s</h1>' % title)
    if subtitle:
        parts.append('<p class="doc-subtitle">%s</p>' % _html.escape(str(subtitle)))
    meta_line = []
    if author:
        meta_line.append(_html.escape(str(author)))
    if date:
        meta_line.append(_html.escape(str(date)))
    if meta_line:
        parts.append('<p class="doc-meta">%s</p>' % " &middot; ".join(meta_line))
    if audience:
        parts.append('<p class="doc-audience">For: %s</p>' % _html.escape(str(audience)))

    # Learning objectives, when present (educational lane).
    objs = meta.get("learning_objectives") or []
    if objs:
        lis = "".join("<li>%s</li>" % md_inline(o) for o in objs)
        parts.append('<div class="objectives"><h2>Learning objectives</h2><ul>%s</ul></div>' % lis)

    parts.append("</header>")
    return "".join(p for p in parts if p)


def _render_footer(footer):
    disclaimer = footer.get("disclaimer", "") if footer else ""
    confidentiality = footer.get("confidentiality", "") if footer else ""
    bits = [b for b in (disclaimer, confidentiality) if b]
    text = " &middot; ".join(_html.escape(str(b)) for b in bits)
    return '<footer class="doc-footer"><p>%s</p></footer>' % text


# ----------------------------------------------------------------------------
# 5. CSS (inline, self-contained). Brand lives in the _DEFAULT_CSS block below,
#    kept in sync with _config/brand.css. (A _config loader that reads brand.css
#    at render and passes it via build_html(css=...) is a tracked follow-up.)
# ----------------------------------------------------------------------------

_DEFAULT_CSS = """
:root{
  --ce-primary:#2B3A8C; --ce-secondary:#5B647F; --ce-accent:#E8A33D;
  --ce-bg:#ffffff; --ce-bg-soft:#F4F5F8; --ce-text:#14171F;
  --ce-muted:#5B647F; --ce-line:#E2E4EC;
  /* Callouts: bar = colored left border, fill = tint, label = AA-safe text.
     Amber/green are non-text bars; their labels use AA-darkened variants. */
  --ce-callout-tip:#2B3A8C; --ce-callout-tip-fill:#EDEFF9;
  --ce-callout-warn:#8A5800; --ce-callout-warn-bar:#E8A33D; --ce-callout-warn-fill:#FBF1DE;
  --ce-callout-note:#5B647F; --ce-callout-note-fill:#F1F2F5;
  --ce-callout-prereq:#2B6B54; --ce-callout-prereq-bar:#3B8C6E; --ce-callout-prereq-fill:#E8F3EE;
  --ce-heading-font:'Helvetica Neue',Helvetica,Arial,sans-serif;
  --ce-body-font:'Helvetica Neue',Helvetica,Arial,sans-serif;
  --ce-mono:ui-monospace,Menlo,Consolas,'Liberation Mono',monospace;
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{margin:0;background:var(--ce-bg);color:var(--ce-text);
  font-family:var(--ce-body-font);line-height:1.6;font-size:16px;}
.layout{display:grid;grid-template-columns:240px minmax(0,1fr);
  max-width:1100px;margin:0 auto;gap:0;}
.toc{position:sticky;top:0;align-self:start;max-height:100vh;overflow:auto;
  padding:24px 16px;border-right:1px solid var(--ce-line);font-size:14px;}
.toc-title{font-weight:700;color:var(--ce-muted);text-transform:uppercase;
  letter-spacing:.06em;font-size:12px;margin-bottom:10px;}
.toc ul{list-style:none;margin:0;padding:0;}
.toc li{margin:.25em 0;}
.toc a{color:var(--ce-text);text-decoration:none;display:block;
  padding:3px 8px;border-radius:4px;transition:background .15s,color .15s;}
.toc a:hover{background:var(--ce-bg-soft);color:var(--ce-primary);}
.toc-l2 a{padding-left:20px;color:var(--ce-muted);font-size:13px;}
.content{padding:32px 40px;min-width:0;}
.title-page{padding:40px 0 32px;border-bottom:2px solid var(--ce-primary);
  margin-bottom:32px;}
.title-accent{display:flex;height:5px;width:100%;margin-bottom:26px;border-radius:2px;overflow:hidden;}
.title-accent .seg-primary{flex:1;background:var(--ce-primary);}
.title-accent .seg-accent{width:84px;background:var(--ce-accent);}
.brand-lockup{display:flex;align-items:center;gap:12px;margin-bottom:18px;}
.brand-lockup svg{display:block;}
.brand-lockup .wordmark{font-family:var(--ce-heading-font);font-size:22px;
  font-weight:600;letter-spacing:-.02em;color:var(--ce-text);}
.brand-lockup .hy{color:var(--ce-primary);}
.brand-mark{font-size:12px;letter-spacing:.18em;color:var(--ce-secondary);
  font-weight:700;margin-bottom:12px;text-transform:uppercase;}
.doc-title{font-family:var(--ce-heading-font);font-size:34px;line-height:1.15;
  margin:0 0 8px;color:var(--ce-primary);}
.doc-subtitle{font-size:18px;color:var(--ce-muted);margin:0 0 16px;}
.doc-meta,.doc-audience{font-size:14px;color:var(--ce-muted);margin:4px 0;}
.objectives{margin-top:24px;background:var(--ce-bg-soft);border:1px solid var(--ce-line);
  border-radius:8px;padding:16px 20px;}
.objectives h2{font-size:16px;margin:0 0 8px;color:var(--ce-primary);}
.doc-section{margin:0 0 8px;}
.doc-section summary{list-style:none;cursor:pointer;outline:none;}
.doc-section summary::-webkit-details-marker{display:none;}
.section-heading{font-family:var(--ce-heading-font);color:var(--ce-primary);
  margin:24px 0 4px;}
h2.section-heading{font-size:24px;border-bottom:1px solid var(--ce-line);
  padding-bottom:6px;}
h3.section-heading{font-size:19px;}
.section-body{padding-left:2px;}
.prose{margin:.7em 0;}
code{background:var(--ce-bg-soft);padding:.1em .35em;border-radius:4px;
  font-family:var(--ce-mono);font-size:.92em;}
a{color:var(--ce-primary);}
.doc-list{margin:.6em 0;padding-left:1.4em;}
.doc-list li{margin:.3em 0;}
.callout{display:block;border-left:4px solid var(--ce-callout-note);
  background:var(--ce-callout-note-fill);padding:12px 16px;border-radius:0 6px 6px 0;margin:1em 0;}
.callout-label{display:block;font-weight:700;font-size:13px;
  text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px;}
.callout-tip{border-left-color:var(--ce-callout-tip);background:var(--ce-callout-tip-fill);}
.callout-tip .callout-label{color:var(--ce-callout-tip);}
.callout-warning{border-left-color:var(--ce-callout-warn-bar);background:var(--ce-callout-warn-fill);}
.callout-warning .callout-label{color:var(--ce-callout-warn);}
.callout-note{border-left-color:var(--ce-callout-note);background:var(--ce-callout-note-fill);}
.callout-note .callout-label{color:var(--ce-callout-note);}
.callout-prereq{border-left-color:var(--ce-callout-prereq-bar);background:var(--ce-callout-prereq-fill);}
.callout-prereq .callout-label{color:var(--ce-callout-prereq);}
.screenshot{margin:1.2em 0;text-align:center;}
.screenshot img{max-width:100%;height:auto;border:1px solid var(--ce-line);
  border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,.08);}
.caption{font-size:13px;color:var(--ce-muted);margin-top:6px;font-style:italic;}
.frame-placeholder{border:2px dashed var(--ce-line);border-radius:6px;
  padding:40px;color:var(--ce-muted);background:var(--ce-bg-soft);}
.doc-footer{margin-top:48px;padding-top:16px;border-top:1px solid var(--ce-line);
  font-size:12px;color:var(--ce-muted);text-align:center;}
@media (max-width:760px){
  .layout{grid-template-columns:1fr;}
  .toc{position:static;max-height:40vh;overflow:auto;border-right:none;
    border-bottom:1px solid var(--ce-line);}
  .content{padding:20px;}
}
"""


# ----------------------------------------------------------------------------
# 6. build_html
# ----------------------------------------------------------------------------

def build_html(docmodel, manifest_path=None, css=None, print_css=None):
    """Build a single self-contained HTML document from a docmodel.

    docmodel: a dict matching docmodel-1.0 (schema literal "docmodel-1.0").
    manifest_path: path to the run manifest (or the in-bundle copy) so
      screenshots resolve; None renders placeholders for screenshots.
    css: override the screen stylesheet (default = the built-in theme).
    print_css: optional @media print stylesheet text appended inline (so the
      PDF path needs no external file).

    Returns the HTML string. Raises ValueError on a wrong schema literal.
    """
    schema = docmodel.get("schema")
    if schema != "docmodel-1.0":
        raise ValueError(
            "render-doc consumes docmodel-1.0 only; got %r. "
            "Refusing to guess a different shape." % schema
        )

    meta = docmodel.get("meta", {}) or {}
    sections = docmodel.get("sections", []) or []
    footer = docmodel.get("footer", {}) or {}

    toc_html = _render_toc(sections)
    title_html = _render_title_page(meta, footer)
    sections_html = "".join(
        _render_section(sec, i, manifest_path) for i, sec in enumerate(sections)
    )
    footer_html = _render_footer(footer)

    style = css if css is not None else _DEFAULT_CSS
    style_block = "<style>%s</style>" % style
    if print_css:
        style_block += "<style media=\"print\">%s</style>" % print_css

    doc_title = _html.escape(str(meta.get("title", "Document")))
    favicon = '<link rel="icon" type="image/png" href="%s">' % _FAVICON_DATA_URI

    return (
        "<!DOCTYPE html>\n"
        '<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        "%s"
        "<title>%s</title>%s</head>"
        '<body><div class="layout">%s'
        '<main class="content">%s%s%s</main></div></body></html>'
        % (favicon, doc_title, style_block, toc_html, title_html, sections_html, footer_html)
    )


# ----------------------------------------------------------------------------
# 7. build_pdf (headless Chrome -> Edge probe)
# ----------------------------------------------------------------------------

def _find_browser():
    """Locate a Chromium browser: Chrome first, then Edge. Returns a path or None."""
    candidates = []
    if sys.platform.startswith("win"):
        pf = os.environ.get("ProgramFiles", r"C:\Program Files")
        pfx86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
        local = os.environ.get("LOCALAPPDATA", "")
        candidates = [
            os.path.join(pf, "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(pfx86, "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(local, "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(pfx86, "Microsoft", "Edge", "Application", "msedge.exe"),
            os.path.join(pf, "Microsoft", "Edge", "Application", "msedge.exe"),
        ]
    elif sys.platform == "darwin":
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ]
    else:
        for name in ("google-chrome", "google-chrome-stable", "chromium",
                     "chromium-browser", "microsoft-edge", "microsoft-edge-stable"):
            found = shutil.which(name)
            if found:
                return found
    for c in candidates:
        if c and os.path.exists(c):
            return c
    # Last resort: anything on PATH.
    for name in ("chrome", "chrome.exe", "msedge", "msedge.exe", "chromium"):
        found = shutil.which(name)
        if found:
            return found
    return None


def build_pdf(html, out_pdf_path, html_path=None, browser=None):
    """Render an HTML string to PDF via headless Chrome/Edge --print-to-pdf.

    html: the HTML string (should include its @media print rules inline).
    out_pdf_path: where to write the PDF.
    html_path: optional path for the intermediate HTML file. If None, a
      sibling .src.html next to the PDF is used (kept; cheap + debuggable).
    browser: explicit browser exe path; else Chrome then Edge are probed.

    Returns out_pdf_path on success. Raises RuntimeError if no browser is
    found or the conversion produces no valid PDF.
    """
    exe = browser or _find_browser()
    if not exe:
        raise RuntimeError(
            "No Chrome or Edge found for --print-to-pdf. Install one, or pass "
            "browser=. (PDF is derived from the same HTML; the HTML target is "
            "unaffected.)"
        )

    out_pdf_path = os.path.abspath(out_pdf_path)
    if html_path is None:
        html_path = os.path.splitext(out_pdf_path)[0] + ".src.html"
    html_path = os.path.abspath(html_path)
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(html)

    file_url = Path(html_path).as_uri()
    cmd = [
        exe,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--print-to-pdf=%s" % out_pdf_path,
        file_url,
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=120)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("Browser PDF conversion timed out: %s" % exc)

    if not os.path.exists(out_pdf_path) or os.path.getsize(out_pdf_path) == 0:
        # Some Chrome builds reject --headless=new; retry the legacy flag.
        cmd[1] = "--headless"
        subprocess.run(cmd, capture_output=True, timeout=120)

    if not os.path.exists(out_pdf_path) or os.path.getsize(out_pdf_path) == 0:
        raise RuntimeError(
            "PDF not produced by %s (exit %s). stderr: %s"
            % (exe, proc.returncode, proc.stderr.decode("utf-8", "replace")[:500])
        )

    with open(out_pdf_path, "rb") as fh:
        head = fh.read(5)
    if head != b"%PDF-":
        raise RuntimeError("Output is not a valid PDF (missing %PDF- header).")
    return out_pdf_path


# ----------------------------------------------------------------------------
# 8. build_docx  --  DOCUMENTED STUB, NOT IMPLEMENTED (decision D3)
# ----------------------------------------------------------------------------

def build_docx(docmodel, out_docx_path, reference_docx=None, manifest_path=None):
    """DOCX target: documented pandoc path, NOT built for this submission (D3).

    The intended path (see `_skills/docx/SKILL.md`):
      1. Reuse build_html(docmodel, manifest_path) to get a docx-flavored HTML
         fragment with base64 data-URI images.
      2. Shell out to pandoc:
           pandoc fragment.html -o out.docx --reference-doc=reference.docx
         pandoc embeds data-URI images as word/media/*.png and maps the
         heading hierarchy to Word styles carried by reference.docx.
      3. reference.docx carries STYLES only (headings, body, header/footer).
         It CANNOT inject a letterhead cover page (pandoc has no cover concept),
         so DOCX ships without the cover-page promise.

    Parked because authoring a good reference.docx is its own mini-project and
    DOCX triples the content-parity QA surface. PDF + HTML satisfy the spirit.
    """
    raise NotImplementedError(
        "DOCX is a documented pandoc path, not built for this submission "
        "(decision D3). See _skills/docx/SKILL.md for the pandoc + "
        "--reference-doc recipe."
    )


# ----------------------------------------------------------------------------
# 9. render: the convenience entry point (HTML + optional PDF)
# ----------------------------------------------------------------------------

def _load_print_css():
    """Read the sibling print.css if present (for the inline PDF path)."""
    here = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(here, "print.css")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as fh:
            return fh.read()
    return None


def render(docmodel, out_dir, slug, manifest_path=None, targets=("html", "pdf"),
           css=None):
    """Render a docmodel to the requested targets in out_dir.

    Writes {slug}.html and/or {slug}.pdf. Returns a dict of produced paths.
    A PDF failure does not delete the HTML (the HTML is the spine).
    """
    os.makedirs(out_dir, exist_ok=True)
    print_css = _load_print_css()
    html = build_html(docmodel, manifest_path=manifest_path, css=css,
                      print_css=print_css)

    produced = {}
    if "html" in targets:
        html_out = os.path.join(out_dir, "%s.html" % slug)
        with open(html_out, "w", encoding="utf-8") as fh:
            fh.write(html)
        produced["html"] = html_out

    if "pdf" in targets:
        pdf_out = os.path.join(out_dir, "%s.pdf" % slug)
        src_html = os.path.join(out_dir, "%s.src.html" % slug)
        produced["pdf"] = build_pdf(html, pdf_out, html_path=src_html)

    return produced


# ----------------------------------------------------------------------------
# 10. CLI: render.py docmodel.json out_dir [--manifest m.json] [--slug name]
#                                          [--targets html,pdf]
# ----------------------------------------------------------------------------

def _main(argv):
    import argparse
    ap = argparse.ArgumentParser(description="Render a docmodel-1.0 to HTML/PDF.")
    ap.add_argument("docmodel", help="path to the docmodel.json")
    ap.add_argument("out_dir", help="output directory")
    ap.add_argument("--manifest", default=None, help="run manifest for frame resolution")
    ap.add_argument("--slug", default=None, help="output basename (default: docmodel stem)")
    ap.add_argument("--targets", default="html,pdf", help="comma list: html,pdf")
    args = ap.parse_args(argv)

    with open(args.docmodel, "r", encoding="utf-8") as fh:
        docmodel = json.load(fh)
    slug = args.slug or os.path.splitext(os.path.basename(args.docmodel))[0]
    targets = tuple(t.strip() for t in args.targets.split(",") if t.strip())

    produced = render(docmodel, args.out_dir, slug,
                      manifest_path=args.manifest, targets=targets)
    for k, v in produced.items():
        print("%-5s -> %s" % (k, v))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
