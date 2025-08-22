#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# mypy: ignore-errors

from rich.console import Console
from deep_translator import GoogleTranslator
from functools import lru_cache
from typing import Union

colored = Console()

class AutoTranslator:
    def __init__(self, source_lang="en", language="es", backend="google"):
        self.source = source_lang
        self.target = language
        self.backend = backend

    @lru_cache(maxsize=128)
    def translate(self, text: str) -> str:
        try:
            if self.backend == "google":
                return GoogleTranslator(source=self.source, target=self.target).translate(text)
            else:
                raise ValueError(f"Unsupported backend: {self.backend}")
        except Exception as e:
            print(f"[Translation error] {text}: {e}")
            return text

    def translate_list(self, texts: list[str]) -> list[str]:
        return [self.translate(text) for text in texts]

    def translate_dict(self, mapping: dict) -> dict:
        return {self.translate(keys): self.translate(values) for keys, values in mapping.items()}

    @staticmethod
    def available_languages(as_dict=False) -> Union[list[str], dict[str, str]]:
        try:
            temp = GoogleTranslator(source='auto', target='en')
            languages = temp.get_supported_languages(as_dict=True)
            if not as_dict:
                for code, name in languages.items():
                    colored.print(f"[bold]{name:<8}[/bold][dim] -> [/dim][bright_yellow]{code:>21}[/bright_yellow]")
                    # colored.print(f"[bold]{emoji.emojize(name):<8}[/bold][dim] -> [/dim][bright_yellow]{code:>21}[/bright_yellow]")
                return list(languages.keys())
            return languages
        except Exception as e:
            print(f"[Error retrieving languages]: {e}")
            return {} if as_dict else []


if __name__ == "__main__":
    AutoTranslator.available_languages(as_dict=False)

    # AutoTranslator.available_languages()
    # persian = AutoTranslator(language="ps")
    # russian = AutoTranslator(language="ru")
    # chinese = AutoTranslator(language="zh-TW")
    # arabic = AutoTranslator(language="ar")
    # hebrew = AutoTranslator(language="iw")
    # serbian = AutoTranslator(language="sr")
    # urdu = AutoTranslator(language="ur")
