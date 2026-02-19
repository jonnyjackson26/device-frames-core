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

devices = list_devices()
print(f"Found {len(devices)} device variations")

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

- `list_devices(category=None)` returns a list of `DeviceInfo` entries.
- `list_frame_sizes(category=None)` returns a list of dicts with `frame_size` and `screen`.
- `apply_frame(...)` applies a frame using bundled assets and writes an output image.
- `find_template(device, variation, category=None)` returns the template data as a dict.

Notes
-----

- Assets are bundled in the package under `device_frames_core/assets`.
- The package depends on Pillow.