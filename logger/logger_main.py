#!/usr/bin/env python
# -*- config: utf-8 -*-
# mypy: ignore-errors

""" Root Logger: Acts as Main logger invocation in any .py files/scripts """

import logging
from pathlib import Path
from colorama import Fore, Style

SRC = Path(__file__).resolve().parent.parent
LOGS = Path(SRC.joinpath('.logs'))
LOG_FILE = Path(LOGS.joinpath('logs.log'))


def create_log_dir(log_dir=LOGS):
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def create_log_file(log_file=LOG_FILE):
    log_file.touch(exist_ok=True)


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_format = logging.Formatter(
        f'\n\t{Fore.GREEN + Style.BRIGHT}LOG-LEVEL:\t{Fore.RESET} -> {Fore.RED}%(levelname)s:'
        f'\n\t{Fore.GREEN + Style.BRIGHT}Time-Date:\t{Fore.RESET} -> {Fore.LIGHTYELLOW_EX}%(asctime)s'
        f'\n\t{Fore.GREEN + Style.BRIGHT}MODULE-SRC:\t{Fore.RESET} -> {Fore.LIGHTWHITE_EX}%(module)s:{Fore.LIGHTGREEN_EX} -> Line #{Fore.RED} %(lineno)s{Fore.RESET}'
        f'\n\t{Fore.GREEN}MESSAGE:\t{Fore.RESET} -> {Fore.RED + Style.BRIGHT}%(message)s{Fore.RED}{Style.RESET_ALL}')
    stream_handler.setFormatter(stream_format)
    return stream_handler


def get_file_handler(log_file_path=LOG_FILE):
    if not Path.exists(log_file_path):
        create_log_dir()
        create_log_file()

    file_handler = logging.FileHandler(f'{log_file_path}')
    file_format = logging.Formatter(
        f'{"-" * 66}'
        f'\nDATE & TIME:\t --> %(asctime)s'
        f'\nLOG-SOURCE\t\t --> %(name)s'
        f'\nMODULE-NAME:\t --> %(module)s'
        f'\nFunctionName:\t --> %(funcName)s'
        f'\nLOG-LEVEL:\t\t --> %(levelname)s'
        f'\nPROCESS-ID:\t\t --> %(process)d'
        f'\nPROCESS-NAME\t --> %(processName)s'
        f'\nTHREAD-ID:\t\t --> %(thread)d'
        f'\n\nLOG-Message:\t --> %(message)s'
        f'\nSOURCE-PATH:\t --> %(pathname)s \t| Code-Line #: %(lineno)s\n')
    file_handler.setFormatter(file_format)
    return file_handler


def get_logger(name, log_file_path=LOG_FILE, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(get_stream_handler())
    logger.addHandler(get_file_handler(log_file_path))
    logger.propagate = False
    return logger


if __name__ == "__main__":
    pass
