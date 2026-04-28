import sys
from pathlib import Path

from streamlit.web.bootstrap import run as run_streamlit_server


def run_streamlit_worker(port_text: str):
    streamlit_app_path = Path(__file__).resolve().parent.parent / "streamlit_app.py"
    run_streamlit_server(
        str(streamlit_app_path),
        False,
        [],
        {
            "server.headless": True,
            "server.address": "127.0.0.1",
            "browser.gatherUsageStats": False,
            "server.port": int(port_text),
        },
    )


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--streamlit-worker":
        run_streamlit_worker(sys.argv[2])
    else:
        from untappd_beer_history.app import main

        main().main_loop()
