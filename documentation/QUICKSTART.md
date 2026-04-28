# Quick Start

Source workflow Python: `3.9+`
Briefcase packaging Python: `3.12+`

```bash
cd /Users/jacobbickus/Python_Files/apps/untapped_data
source .venv/bin/activate
python3 src/run.py
```

Default behavior:

- If `data/my_beers.csv` already exists, Streamlit opens immediately
- Use `python3 src/run.py --update` to force a fresh Untappd download
- Exports to `data/my_beers.csv`
- Opens Streamlit after the export finishes

Briefcase packaging:

```bash
python3 -m venv .briefcase-venv
source .briefcase-venv/bin/activate
pip install briefcase
BRIEFCASE_HOME=.briefcase-home briefcase create macOS
BRIEFCASE_HOME=.briefcase-home briefcase update macOS
BRIEFCASE_HOME=.briefcase-home briefcase build macOS
BRIEFCASE_HOME=.briefcase-home briefcase package macOS --adhoc-sign
```

Best install path for non-developers:

- Download the DMG from `GitHub Releases`
- Use `Download ZIP` only if you want the source code

Useful commands:

```bash
python3 src/run.py
python3 src/run.py --update
python3 src/run.py selenium-launch-chrome
python3 src/run.py selenium-fetch-beers
python3 src/run.py selenium-fetch-beers --backstop-total 250
python3 src/run.py streamlit
```
