
### device-frames-core
Python core library for applying device frames to screenshots and retrieving up-to-date media of device frame PNGs (with metadata)

![apply_frame function example](docs/example.png)

```
pip install device-frames-core
```

```python
from pathlib import Path
from device_frames_core import apply_frame, list_devices

# List devices
all_devices = list_devices()

# Apply a frame
apply_frame(
    screenshot_path=Path("input.png"),
    device="16-pro-max",
    variation="black-titanium",
    output_path=Path("output/framed.png"),
    category="ios",
)
```
