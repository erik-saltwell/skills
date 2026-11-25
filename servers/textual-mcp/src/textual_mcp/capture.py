"""Preserve the original renderer output and derive framed documentation assets."""

import hashlib
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET

import cairosvg
from rich.cells import cell_len
from textual.app import App

from textual_mcp.inspection import snapshot, unique_widget, visible_region
from textual_mcp.models import Capture

SVG = "{http://www.w3.org/2000/svg}"
ET.register_namespace("", "http://www.w3.org/2000/svg")


def capture(app: App, action: Capture, directory: Path, sequence: int) -> dict:
    original = app.export_screenshot(title=app.title)
    root = ET.fromstring(original)
    crop = None
    if action.selector:
        widget = unique_widget(app, action.selector)
        region = visible_region(widget)
        if not widget.visible or not widget.display or not region:
            raise ValueError("Capture target has no visible region. Scroll it into view first.")
        region = region.grow((action.padding,) * 4).intersection(app.size.region)
        # Derive the cell geometry from Rich's generated line clips and content group.
        # Fail explicitly if a future Rich exporter changes this layout.
        clips = {
            node.attrib.get("id", ""): node.find(f"{SVG}rect")
            for node in root.iter(f"{SVG}clipPath")
        }
        first = next(rect for name, rect in clips.items() if name.endswith("-line-0"))
        second = next(rect for name, rect in clips.items() if name.endswith("-line-1"))
        cell_width = float(first.attrib["width"]) / app.size.width
        cell_height = float(second.attrib["y"]) - float(first.attrib["y"])
        group = next(
            node
            for node in root.iter(f"{SVG}g")
            if node.attrib.get("clip-path", "").endswith("-clip-terminal)")
        )
        transform = re.fullmatch(r"translate\(([\d.]+),\s*([\d.]+)\)", group.attrib["transform"])
        if transform is None:
            raise ValueError("Unsupported Rich SVG layout; capture the full screen instead.")
        origin_x, origin_y = map(float, transform.groups())
        box = (
            origin_x + region.x * cell_width,
            origin_y + region.y * cell_height,
            region.width * cell_width,
            region.height * cell_height,
        )
        root.set("viewBox", " ".join(str(number) for number in box))
        root.set("width", str(box[2]))
        root.set("height", str(box[3]))
        crop = region._asdict()

    framed = ET.tostring(root, encoding="unicode") if crop else original
    # Cairo ignores SVG textLength. Place glyphs on the exported cell grid for previews.
    raster_root = ET.fromstring(framed)
    for style in raster_root.iter(f"{SVG}style"):
        style.text = (style.text or "").replace(
            "font-family: Fira Code, monospace;", "font-family: DejaVu Sans Mono;"
        )
    for node in raster_root.iter(f"{SVG}text"):
        content = node.text or ""
        cells = cell_len(content)
        if "textLength" not in node.attrib or not cells or not content.strip():
            continue
        spacing = float(node.attrib.pop("textLength")) / cells
        x = float(node.attrib.get("x", 0))
        node.text = None
        last = None
        for character in content:
            width = cell_len(character)
            if width == 0 and last is not None:
                last.text += character
                continue
            last = ET.SubElement(node, f"{SVG}tspan", {"x": str(x)})
            last.text = character
            x += width * spacing
    png = cairosvg.svg2png(bytestring=ET.tostring(raster_root))
    stem = f"{sequence:06d}"
    directory.mkdir(parents=True, exist_ok=True)
    original_path = directory / f"{stem}-full.svg"
    svg_path = directory / f"{stem}.svg"
    png_path = directory / f"{stem}.png"
    original_path.write_text(original, encoding="utf-8")
    svg_path.write_text(framed, encoding="utf-8")
    png_path.write_bytes(png)
    metadata = {
        "sequence": sequence,
        "label": action.label,
        "selector": action.selector,
        "crop_cells": crop,
        "state": snapshot(app),
        "svg": str(svg_path),
        "original_svg": str(original_path),
        "png": str(png_path),
        "svg_sha256": hashlib.sha256(framed.encode()).hexdigest(),
        "png_sha256": hashlib.sha256(png).hexdigest(),
        "renderer": "Textual export_screenshot; PNG via CairoSVG with cell-positioned glyphs",
        "font_note": (
            "SVG uses Fira Code/monospace; PNG requests DejaVu Sans Mono. "
            "Local fallback and glyph appearance may differ."
        ),
    }
    metadata_path = directory / f"{stem}.json"
    metadata["metadata"] = str(metadata_path)
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata
