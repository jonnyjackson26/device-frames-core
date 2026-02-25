# Deployment (PyPI via GitHub OIDC)

This project publishes to PyPI using a GitHub Actions trusted publisher (OIDC), so no PyPI API token is needed.

## Workflow used

- Workflow file: `.github/workflows/updatePyPi.yml`
- Trigger: GitHub Release published (`release.published`)
- Optional trigger: manual run (`workflow_dispatch`)
- Publish job environment: `pypi`

## One-time setup checklist

1. **PyPI trusted publisher is configured** for:
   - Owner/repo: `jonnyjackson26/device-frames-core`
   - Workflow file: `updatePyPi.yml`
   - Environment name: `pypi` (recommended)
2. **GitHub Environment exists** (recommended):
   - In repo settings, create environment `pypi`
   - Optional: add required reviewers for a manual approval gate before publish
3. **Repository permissions are enabled** (default for public repos):
   - GitHub Actions allowed to run
   - OIDC token requests allowed (handled by `id-token: write` in workflow)

## How to make a GitHub Release (recommended publish path)

1. Update version in `pyproject.toml` under `[project].version`.
2. Commit and push to `main`.
3. Create and push a matching git tag:
   - `git tag v0.1.4`
   - `git push origin v0.1.4`
4. In GitHub:
   - Open **Releases** → **Draft a new release**
   - Choose tag `v0.1.4`
   - Set release title (for example, `v0.1.4`)
   - Add release notes
   - Click **Publish release**
5. GitHub Actions runs `Publish to PyPI` and uploads `dist/*` to PyPI.

## Verify deployment

- Check action run status in **Actions** tab.
- Check package page on PyPI:
  - https://pypi.org/project/device-frames-core/
- Optional install check:
  - `python -m pip install --upgrade device-frames-core`

## Troubleshooting

- **"File already exists"**: the version was already published. Bump `pyproject.toml` version and release again.
- **OIDC/trusted publisher error**: confirm publisher mapping in PyPI exactly matches repo + workflow file, and environment if you restrict it.
- **Build failure**: run local checks:
  - `python -m pip install --upgrade build twine`
  - `python -m build`
  - `python -m twine check dist/*`

## Is any more action required?

Only one likely follow-up: in PyPI trusted publisher settings, set the environment to `pypi` (instead of `Any`) to match the workflow and tighten security. If you keep it as `Any`, publishing still works.
