#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import yaml
from pathlib import Path
from rich.panel import Panel
from datetime import datetime
from rich.console import Console

sys.path.append(str(Path(__file__).resolve().parents[1]))
from logger import logger_main

console = Console()
log_it = logger_main.get_logger(__name__)

# --------------------------------------------------------------------------------------------------
def entrant_catalog(records_dir: str):
    all_artifacts = []
    stamp = datetime.now().strftime("%B-%Y")
    storage = Path(__file__).resolve().parents[1] / stamp / records_dir
    _ini = Path(__file__).resolve().parents[1] / "injectors"
    get_cfg = [cfg for cfg in _ini.iterdir() if cfg.is_file() and cfg.suffix == ".yml"]
    
    for cfg_file in get_cfg:
        with cfg_file.open("r", encoding="utf-8") as entrant:
            data = yaml.safe_load(entrant)
            names = data.get("name", [])
            storage.mkdir(parents=True, exist_ok=True)

            for name in names:
                json_path = storage / f"{name}.json"
                all_artifacts.append(str(json_path))

    return all_artifacts


def reader(position: int, split_by_length: int = None):
    _ini = Path(__file__).resolve().parents[1] / "injectors"
    get_cfg = [cfg for cfg in _ini.iterdir() if cfg.is_file() and cfg.suffix == ".yml"]
    result = []
    
    for cfg_file in get_cfg:
        with cfg_file.open("r", encoding="utf-8") as entrant:
            data = yaml.safe_load(entrant)
            names = data.get("name", [])
            
            # _____ empty strings filter | check for characters:
            valid_names = [name for name in names if isinstance(name, str) and len(name) > position]
            
            if split_by_length:
                # ____ split by chunks | length specified:
                valid_names = [name[:split_by_length] for name in valid_names if len(name) >= split_by_length]
            
            # ___ pull char | index position specified:
            vertical_read = ''.join([name[position] for name in valid_names])
            result.append(vertical_read)
    
    return result
    
if __name__ == "__main__":
    console.print(reader(41))
    # Read character at position 2 from first 3 characters of each name
    # console.print(reader(1, split_by_length=3))
