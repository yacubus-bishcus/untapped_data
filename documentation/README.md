# Untappd Beer History Exporter

This project exports your Untappd beer history with Selenium, saves it under `data/my_beers.csv`, and opens a Streamlit dashboard for reviewing the results.

Source workflow Python: `3.9+`
Briefcase packaging Python: `3.12+`

## Download Options

- `GitHub Releases`: best option for macOS users who just want to install the app
- `Download ZIP`: source code only, best for development or manual local setup

## Project Layout

```text
untapped_data/
├── data/
├── documentation/
├── resources/
├── src/
└── pyproject.toml
```

- `data/`: generated CSVs, local app config, and producer cache
- `documentation/`: setup and usage docs
- `resources/`: Briefcase app icon assets
- `src/`: Python source files and `requirements.txt`
- `pyproject.toml`: Briefcase packaging configuration

## Briefcase Packaging

The macOS distribution path is Briefcase.

Project files for Briefcase live at:

```text
pyproject.toml
src/untappd_beer_history/
resources/appicon.icns
```

Typical macOS packaging flow:

```bash
python3 -m venv .briefcase-venv
source .briefcase-venv/bin/activate
pip install briefcase
BRIEFCASE_HOME=.briefcase-home briefcase create macOS
BRIEFCASE_HOME=.briefcase-home briefcase update macOS
BRIEFCASE_HOME=.briefcase-home briefcase build macOS
BRIEFCASE_HOME=.briefcase-home briefcase package macOS --adhoc-sign
```

This produces a native app bundle and a DMG installer for local distribution and testing.

Recommended retest flow after code changes:

1. Rebuild with `briefcase update macOS` and `briefcase build macOS`
2. Test the direct app bundle under `build/`
3. Package a fresh DMG
4. Reinstall from the new DMG if the direct bundle looks good

## Setup

```bash
cd /Users/jacobbickus/Python_Files/apps/untapped_data
python3 -m venv .venv
source .venv/bin/activate
pip install -r src/requirements.txt
```

## Main Workflow

```bash
python3 src/run.py
python3 src/run.py --update
```

Default behavior:

1. If `data/my_beers.csv` already exists, Streamlit opens immediately
2. With `--update`, Chrome launches for manual login if needed
3. Selenium exports the beer history to `data/my_beers.csv`
4. The dashboard opens after export

## Commands

```bash
python3 src/run.py
python3 src/run.py --update
python3 src/run.py selenium-launch-chrome
python3 src/run.py selenium-fetch-beers
python3 src/run.py selenium-fetch-beers --backstop-total 250
python3 src/run.py streamlit
```

## Output Files

- `data/my_beers.csv`
- `data/producer_location_cache.json`
- `data/app_config.json`

## Notes

- `src/run.py` opens Streamlit immediately when `data/my_beers.csv` already exists. Pass `--update` to refresh from Untappd first.
- The Streamlit app reads `data/my_beers.csv` by default.
- Producer locations are cached in `data/producer_location_cache.json`.
- The Briefcase macOS build produces a native `.app` and DMG installer.
- The bundled app window shows a version/build stamp so you can tell whether you are opening a fresh build or a stale installed copy.
