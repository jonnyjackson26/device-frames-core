device-frames-core
==================

Core library for applying device frames to screenshots.

Install
-------

```bash
pip install device-frames-core
```

Quick Start
-----------

```python
from pathlib import Path

from device_frames_core import apply_frame, list_devices

# List all iOS device variations
devices = list_devices(category="iOS")
print(f"Found {len(devices)} iOS device variations")

apply_frame(
    screenshot_path=Path("input.png"),
    device="16 Pro Max",
    variation="Black Titanium",
    output_path=Path("output/framed.png"),
    category="iOS",
)
```

API
---

- `list_devices(category=None, device=None)` returns a list of available devices and variations, optionally filtered.
- `apply_frame(...)` applies a frame using bundled assets and writes an output image.
- `find_template(device, variation, category=None)` returns the template data as a dict.
- `get_frame_image(device, variation, category=None)` returns the frame image as a PIL Image.
- `get_mask_image(device, variation, category=None)` returns the mask image as a PIL Image.

Notes
-----

- Assets are bundled in the package under `device_frames_core/assets`.
- The package depends on Pillow.