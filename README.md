# Untappd Beer History

Export your Untappd beer history with Selenium, save it to CSV, and explore it in a local dashboard.

## Best Download Option

If you just want to use the app on macOS, download the latest DMG from GitHub Releases.

- `GitHub Releases`:
  Use the packaged `.dmg` installer
- `Download ZIP`:
  Source code only, intended for development or manual setup

## Project Layout

```text
untapped_data/
├── data/
├── documentation/
├── resources/
├── src/
└── pyproject.toml
```

## Quick Start From Source

Source mode is intended for development and manual local runs.

```bash
cd apps/untapped_data
python3 -m venv .venv
source .venv/bin/activate
pip install -r src/requirements.txt
python3 src/run.py
```

## Build The macOS App

Briefcase is the supported macOS packaging path.

```bash
python3 -m venv .briefcase-venv
source .briefcase-venv/bin/activate
pip install briefcase
BRIEFCASE_HOME=.briefcase-home briefcase create macOS
BRIEFCASE_HOME=.briefcase-home briefcase update macOS
BRIEFCASE_HOME=.briefcase-home briefcase build macOS
BRIEFCASE_HOME=.briefcase-home briefcase package macOS --adhoc-sign
```

The rebuilt direct app appears in:

- `build/untappd_beer_history/macos/app/Untappd Beer History.app`

The packaged installer appears in:

- `dist/Untappd Beer History-0.1.0.dmg`

## More Docs

- `documentation/README.md`
- `documentation/QUICKSTART.md`
