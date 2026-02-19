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






Usage in Your API/CLI
---------------------

Install:

```bash
pip install device-frames-core
```

Example usage:

```python
from pathlib import Path
from device_frames_core import apply_frame, list_devices, list_frame_sizes

# List devices
all_devices = list_devices()

# Optionally inspect sizes
sizes = list_frame_sizes(category="iOS")

# Apply a frame
apply_frame(
    screenshot_path=Path("input.png"),
    device="16 Pro Max",
    variation="Black Titanium",
    output_path=Path("output/framed.png"),
    category="iOS",
)
```

Tip: For local development in your API/CLI repos, install in editable mode:

```bash
pip install -e /path/to/device-frames-core
```