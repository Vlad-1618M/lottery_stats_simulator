#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def format_key_pairs(pairs, width=0):
    return ", ".join(f"({x},{y})" for x, y in pairs).rjust(width)


if __name__ == "__main__":
    pass
