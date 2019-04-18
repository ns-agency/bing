#!/usr/bin/env python3

try:
    import bing_drive
except ImportError:
    raise RuntimeError("Couldn't import bing_drive, have you run pip install -e app?")

import os

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.py")

    print("Loading config from", config_path)
    bing_drive.app.config.from_pyfile(config_path, silent=True)

    bing_drive.app.run(host="0.0.0.0", port=4141, debug=True, use_evalex=False)
