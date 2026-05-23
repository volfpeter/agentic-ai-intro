from __future__ import annotations

import re
from abc import ABC, abstractmethod
from pathlib import Path

from pylatexenc.latex2text import LatexNodes2Text


class PaperConverter(ABC):
    @abstractmethod
    def convert(self, tex_files: list[Path], main_file: Path) -> str: ...


class PylatexencConverter(PaperConverter):
    def __init__(self) -> None:
        self._converter = LatexNodes2Text()

    def convert(self, tex_files: list[Path], main_file: Path) -> str:
        content = main_file.read_text(encoding="utf-8", errors="replace")
        plain = self._converter.latex_to_text(content)
        lines = plain.split("\n")
        result: list[str] = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                result.append("")
                continue
            result.append(stripped)

        body = "\n".join(result)
        return re.sub(r"\n{3,}", "\n\n", body)
