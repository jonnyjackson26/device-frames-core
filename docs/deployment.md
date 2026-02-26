1. Bump version number in pyproject.toml
2. Remove dist and activate a virtualenv:
```bash
rm -rf dist
source .venv/bin/activate
```
3. Build fresh artifacts:
```bash
python -m build
python -m twine check dist/*
```
4. (Optional) Upload to TestPyPI and verify install:
```bash
python -m twine upload --repository testpypi dist/*   #you'll need to put in your api token
```
5. Upload to PyPI:
```bash
python -m twine upload dist/*                         #you'll need to put in your api token
```