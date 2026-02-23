from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path
from typing import Optional, Tuple
from urllib.request import urlopen

from PIL import Image, ImageFilter

from .errors import TemplateAmbiguousError, TemplateNotFoundError


# URL to the device frames index JSON
DEVICE_FRAMES_INDEX_URL = "https://raw.githubusercontent.com/jonnyjackson26/device-frames-media/main/device-frames-output/index.json"

# Cache for the device frames index
_device_frames_cache: Optional[dict] = None


def _get_device_frames_index() -> dict:
    """Fetch and cache the device frames index from the remote URL."""
    global _device_frames_cache
    
    if _device_frames_cache is None:
        with urlopen(DEVICE_FRAMES_INDEX_URL) as response:
            _device_frames_cache = json.loads(response.read().decode('utf-8'))
    
    return _device_frames_cache


def list_devices(
    category: Optional[str] = None,
    device: Optional[str] = None,
) -> list[dict]:
    """Return all available devices and variations, optionally filtered by category and/or device.
    
    If device is specified, category must also be specified.
    """
    
    if device and not category:
        raise ValueError("category must be specified when device is specified")

    index = _get_device_frames_index()
    devices = []
    
    for category_name, category_devices in index.items():
        if category and category_name != category:
            continue
            
        for device_name, device_variations in category_devices.items():
            if device and device_name != device:
                continue
                
            for variation_name, variation_data in device_variations.items():
                devices.append({
                    "category": category_name,
                    "device": device_name,
                    "variation": variation_name,
                    "frame_size": variation_data.get("frameSize", {}),
                    "screen": variation_data.get("screen", {}),
                })
    
    return devices


def _find_template_data(
    device: str,
    variation: str,
    category: Optional[str],
) -> dict:
    """Find and return the template data for the given device and variation."""
    index = _get_device_frames_index()
    
    matches = []
    
    for category_name, category_devices in index.items():
        if category and category_name != category:
            continue
            
        for device_name, device_variations in category_devices.items():
            if device_name != device:
                continue
                
            if variation in device_variations:
                matches.append({
                    "category": category_name,
                    "data": device_variations[variation]
                })
    
    if not matches:
        raise TemplateNotFoundError(
            f"No template found for device='{device}', variation='{variation}', category='{category}'."
        )

    if len(matches) > 1:
        raise TemplateAmbiguousError(
            "Multiple templates matched. Specify a category to disambiguate."
        )

    return matches[0]["data"]


def find_template(
    device: str,
    variation: str,
    *,
    category: Optional[str] = None,
) -> dict:
    """Load and return the template data for the given device and variation."""
    return _find_template_data(device, variation, category)


def _download_image(url: str) -> Image.Image:
    """Download an image from a URL and return it as a PIL Image."""
    with urlopen(url) as response:
        image_data = response.read()
        return Image.open(BytesIO(image_data))


def get_frame_image(
    device: str,
    variation: str,
    *,
    category: Optional[str] = None,
) -> Image.Image:
    """Load and return the frame image for the given device and variation."""
    template_data = _find_template_data(device, variation, category)
    return _download_image(template_data["frame"])


def get_mask_image(
    device: str,
    variation: str,
    *,
    category: Optional[str] = None,
) -> Image.Image:
    """Load and return the mask image for the given device and variation."""
    template_data = _find_template_data(device, variation, category)
    return _download_image(template_data["mask"])


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
    
    template = _find_template_data(device, variation, category)
    
    # Download frame and mask images
    frame = _download_image(template["frame"])
    mask = _download_image(template["mask"])
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
