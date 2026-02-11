INFO
====

Local Test (Build + Verify)
---------------------------

1. Create and activate a virtualenv:

```bash
rm -rf dist
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

Publish to PyPI (Recommended Flow: TestPyPI first)
--------------------------------------------------

0. Remove dist and activate a virtualenv:

```bash
rm -rf dist
source .venv/bin/activate
```

1. Build fresh artifacts:

```bash
python -m build
python -m twine check dist/*
```

2. Upload to TestPyPI and verify install:

```bash
python -m twine upload --repository testpypi dist/*
```
Put in your api token

```bash
python -m venv .venv-testpypi
source .venv-testpypi/bin/activate
python -m pip install --upgrade pip
python -m pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ device-frames-core
python - <<'PY'
from device_frames_core import list_devices
print(len(list_devices()))
PY
```

3. Upload to PyPI:

```bash
python -m twine upload dist/*
```

Upload Methods and Pros/Cons
----------------------------

Option A: API Token + Twine (most direct)
Pros:
- Simple, works locally, no CI required
- Easy to test with TestPyPI and then PyPI
Cons:
- You must store/manage a long-lived token
- Risk of accidentally leaking credentials if shell history is shared

How:
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-REPLACE_WITH_YOUR_TOKEN
python -m twine upload --repository testpypi dist/*
python -m twine upload dist/*
```

Option B: Keyring + Twine (safer local auth)
Pros:
- Avoids plaintext env vars
- Still local and straightforward
Cons:
- Extra setup (keyring backend)
- Can be tricky in containers

How:
```bash
python -m pip install keyring
python -m twine upload --repository testpypi dist/*
python -m twine upload dist/*
```

Option C: Trusted Publishing via GitHub Actions (recommended long-term)
Pros:
- No API tokens to manage (uses OIDC)
- Auditable releases in CI
- Scales well for future releases
Cons:
- Initial setup in PyPI and GitHub
- Requires CI workflow

How (high level):
- In PyPI/TestPyPI, add a "Trusted Publisher" for this GitHub repo.
- Create a GitHub Actions workflow that runs `python -m build` and then uses `pypa/gh-action-pypi-publish`.

If you've already linked GitHub to PyPI, Option C is typically the most secure. For an immediate release, Option A is fastest.

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


**IN THE FUTURE:**
adopt a tool like setuptools-scm or hatch if you want automatic versioning from git tags.