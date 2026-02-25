ci/cd for pypi

fix image in pypi docs


**IN THE FUTURE:**
adopt a tool like setuptools-scm or hatch if you want automatic versioning from git tags.

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