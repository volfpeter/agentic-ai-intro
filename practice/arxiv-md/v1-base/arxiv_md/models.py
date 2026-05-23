from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar


@dataclass
class Paper:
    id: str
    title: str
    authors: list[str]
    abstract: str
    url: str
    published: str
    categories: list[str]


@dataclass
class Settings:
    output_dir: Path = Path("papers")
    default_max_results: int = 30
    default_date_range_days: int = 30

    PAPERS_DIR: ClassVar[Path] = Path("papers")
