#!/usr/bin/env python3
"""Convert a .docx Solution Design Document to markdown for pipeline review.

Standard library only — no pip installs. Extracts headings, paragraphs,
lists, and tables. Images are noted as placeholders so the intake manifest
can record which diagrams must be exported separately.

Usage: python3 tools/docx_to_md.py <input.docx> <output.md>
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def para_text(p):
    parts = []
    for node in p.iter():
        if node.tag == f"{W}t":
            parts.append(node.text or "")
        elif node.tag == f"{W}tab":
            parts.append("\t")
        elif node.tag == f"{W}br":
            parts.append("\n")
        elif node.tag == f"{W}drawing":
            parts.append("[embedded image: export separately as an image file]")
    return "".join(parts)


def heading_level(p):
    style = p.find(f"{W}pPr/{W}pStyle")
    if style is not None:
        m = re.fullmatch(r"(?:Heading|Ttulo|Titre|berschrift)(\d)", style.get(f"{W}val", ""))
        if m:
            return int(m.group(1))
    return 0


def is_list_item(p):
    return p.find(f"{W}pPr/{W}numPr") is not None


def table_to_md(tbl):
    rows = []
    for tr in tbl.findall(f"{W}tr"):
        cells = [" ".join(para_text(p).strip() for p in tc.findall(f"{W}p")).strip()
                 for tc in tr.findall(f"{W}tc")]
        rows.append("| " + " | ".join(c.replace("|", "\\|") or " " for c in cells) + " |")
    if not rows:
        return ""
    ncols = rows[0].count("|") - 1
    rows.insert(1, "|" + "---|" * ncols)
    return "\n".join(rows)


def convert(src, dst):
    with zipfile.ZipFile(src) as z:
        body = ET.fromstring(z.read("word/document.xml")).find(f"{W}body")
    out = []
    for el in body:
        if el.tag == f"{W}p":
            text = para_text(el).strip()
            if not text:
                continue
            lvl = heading_level(el)
            if lvl:
                out.append("#" * lvl + " " + text)
            elif is_list_item(el):
                out.append("- " + text)
            else:
                out.append(text)
        elif el.tag == f"{W}tbl":
            md = table_to_md(el)
            if md:
                out.append(md)
    with open(dst, "w", encoding="utf-8") as f:
        f.write("\n\n".join(out) + "\n")
    print(f"Converted {src} -> {dst} ({len(out)} blocks)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    convert(sys.argv[1], sys.argv[2])
