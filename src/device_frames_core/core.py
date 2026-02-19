from __future__ import annotations

import json
from dataclasses import dataclass
from importlib.resources import as_file, files
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from PIL import Image, ImageFilter

from .errors import TemplateAmbiguousError, TemplateNotFoundError


@dataclass(frozen=True)
class DeviceInfo:
    category: str
    device: str
    variation: str
    frame_size: Dict[str, int]
    screen: Dict[str, int]
    template_path: str


def _assets_root() -> Path:
    return Path(files("device_frames_core").joinpath("assets"))


def _iter_templates(assets_root: Path) -> Iterable[Path]:
    return sorted(assets_root.rglob("template.json"))


def list_devices(category: Optional[str] = None) -> List[DeviceInfo]:
    """Return all available devices and variations."""

    with as_file(_assets_root()) as assets_root:
        templates = _iter_templates(assets_root)

        devices: List[DeviceInfo] = []
        for template_path in templates:
            relative = template_path.parent.relative_to(assets_root)
            parts = relative.parts
            if len(parts) < 3:
                continue

            category_name = parts[0]
            if category and category_name != category:
                continue

            device_name = parts[-2]
            variation_name = parts[-1]

            with open(template_path, "r", encoding="utf-8") as handle:
                template = json.load(handle)

            devices.append(
                DeviceInfo(
                    category=category_name,
                    device=device_name,
                    variation=variation_name,
                    frame_size=template.get("frameSize", {}),
                    screen=template.get("screen", {}),
                    template_path=str(relative),
                )
            )

        return devices


def list_frame_sizes(category: Optional[str] = None) -> List[Dict[str, object]]:
    """Return frame sizes for all devices/variations."""

    return [
        {
            "category": device.category,
            "device": device.device,
            "variation": device.variation,
            "frame_size": device.frame_size,
            "screen": device.screen,
        }
        for device in list_devices(category=category)
    ]


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
