#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
from pathlib import Path

# ____ load game types | track mum limits:
def get_games_catalog(cfg_path=None) -> dict:
    game_settings = cfg_path or Path(__file__).resolve().parents[1] / "globs/games.yml"
    with game_settings.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# if __name__ == "__main__":
#     pass
    # [print(_) for _ in get_games_catalog(cfg_path=None).items()]