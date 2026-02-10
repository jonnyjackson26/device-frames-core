INFO
====

Local Test (Build + Verify)
---------------------------

1. Create and activate a virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install build tools:

```bash
python -m pip install --upgrade pip
python -m pip install build twine
```

3. Build sdist + wheel:

```bash
python -m build
```

4. Check distribution metadata:

```bash
python -m twine check dist/*
```

5. Install the wheel locally and do a quick import check:

```bash
python -m pip install dist/*.whl
python - <<'PY'
from device_frames_core import list_devices
print(len(list_devices()))
PY
```

Publish to PyPI
--------------

1. Ensure you have a PyPI account and an API token.
2. Set the token in your shell (or use a keyring):

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-REPLACE_WITH_YOUR_TOKEN
```

3. Upload:

```bash
python -m twine upload dist/*
```

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
