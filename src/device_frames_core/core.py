from __future__ import annotations

import json
from importlib.resources import as_file, files
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageFilter

from .errors import TemplateAmbiguousError, TemplateNotFoundError


def _assets_root() -> Path:
    return Path(files("device_frames_core").joinpath("assets"))


def list_devices(
    category: Optional[str] = None,
    device: Optional[str] = None,
) -> list[dict]:
    """Return all available devices and variations, optionally filtered by category and/or device.
    
    If device is specified, category must also be specified.
    """
    
    if device and not category:
        raise ValueError("category must be specified when device is specified")

    with as_file(_assets_root()) as assets_root:
        templates = sorted(assets_root.rglob("template.json"))

        devices = []
        for template_path in templates:
            relative = template_path.parent.relative_to(assets_root)
            parts = relative.parts
            if len(parts) < 3:
                continue

            category_name = parts[0]
            device_name = parts[-2]
            variation_name = parts[-1]

            if category and category_name != category:
                continue
            if device and device_name != device:
                continue

            with open(template_path, "r", encoding="utf-8") as handle:
                template = json.load(handle)

            devices.append(
                {
                    "category": category_name,
                    "device": device_name,
                    "variation": variation_name,
                    "frame_size": template.get("frameSize", {}),
                    "screen": template.get("screen", {}),
                }
            )

        return devices


def _find_template_path(
    assets_root: Path,
    device: str,
    variation: str,
    category: Optional[str],
) -> Path:
    pattern = f"{device}/{variation}/template.json"
    matches = list(assets_root.rglob(pattern))

    if category:
        matches = [
            match for match in matches
            if match.parent.parent.name == device
            and match.parent.name == variation
            and match.parent.parent.parent.name == category
        ]

    if not matches:
        raise TemplateNotFoundError(
            f"No template found for device='{device}', variation='{variation}', category='{category}'."
        )

    if len(matches) > 1:
        raise TemplateAmbiguousError(
            "Multiple templates matched. Specify a category to disambiguate."
        )

    return matches[0]


def find_template(
    device: str,
    variation: str,
    *,
    category: Optional[str] = None,
) -> dict:
    """Load and return the template data for the given device and variation."""

    with as_file(_assets_root()) as assets_root:
        template_path = _find_template_path(assets_root, device, variation, category)
        with open(template_path, "r", encoding="utf-8") as handle:
            return json.load(handle)


def get_frame_image(
    device: str,
    variation: str,
    *,
    category: Optional[str] = None,
) -> Image.Image:
    """Load and return the frame image for the given device and variation."""

    with as_file(_assets_root()) as assets_root:
        template_path = _find_template_path(assets_root, device, variation, category)
        with open(template_path, "r", encoding="utf-8") as handle:
            template = json.load(handle)

        frame_dir = template_path.parent
        return Image.open(frame_dir / template["frame"])


def get_mask_image(
    device: str,
    variation: str,
    *,
    category: Optional[str] = None,
) -> Image.Image:
    """Load and return the mask image for the given device and variation."""

    with as_file(_assets_root()) as assets_root:
        template_path = _find_template_path(assets_root, device, variation, category)
        with open(template_path, "r", encoding="utf-8") as handle:
            template = json.load(handle)

        frame_dir = template_path.parent
        return Image.open(frame_dir / template["mask"])


def apply_frame(
    screenshot_path: Path,
    device: str,
    variation: str,
    output_path: Path,
    *,
    category: Optional[str] = None,
    background_color: Tuple[int, int, int, int] | Tuple[int, int, int] = (0, 0, 0, 0),
) -> Path:
    """Apply a device frame to a screenshot and save the output image."""

    with as_file(_assets_root()) as assets_root:
        template_path = _find_template_path(assets_root, device, variation, category)

        with open(template_path, "r", encoding="utf-8") as handle:
            template = json.load(handle)

        frame_dir = template_path.parent

        frame = Image.open(frame_dir / template["frame"])
        mask = Image.open(frame_dir / template["mask"])
        screenshot = Image.open(screenshot_path)

    screen = template["screen"]

    screenshot_resized = screenshot.resize(
        (screen["width"], screen["height"]),
        Image.Resampling.LANCZOS,
    )

    if screenshot_resized.mode != "RGBA":
        screenshot_resized = screenshot_resized.convert("RGBA")

    mask_region = mask.crop(
        (
            screen["x"],
            screen["y"],
            screen["x"] + screen["width"],
            screen["y"] + screen["height"],
        )
    )

    mask_region = mask_region.filter(ImageFilter.MaxFilter(3))
    screenshot_resized.putalpha(mask_region)

    composite = Image.new(
        "RGBA",
        (template["frameSize"]["width"], template["frameSize"]["height"]),
        background_color,
    )
    composite.paste(screenshot_resized, (screen["x"], screen["y"]), screenshot_resized)
    composite.paste(frame, (0, 0), frame)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    composite.save(output_path)

    return output_path
