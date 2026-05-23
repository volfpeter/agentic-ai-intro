import tarfile
import tempfile
from pathlib import Path

import requests

ARXIV_SOURCE_URL = "https://arxiv.org/e-print/{arxiv_id}"


def download_source(arxiv_id: str) -> Path | None:
    url = ARXIV_SOURCE_URL.format(arxiv_id=arxiv_id)
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    if "pdf" in content_type:
        return None

    temp_dir = Path(tempfile.mkdtemp(prefix=f"arxiv_{arxiv_id}_"))
    tar_path = temp_dir / f"{arxiv_id}.tar.gz"
    tar_path.write_bytes(response.content)
    return tar_path


def extract_source(tar_path: Path, arxiv_id: str) -> tuple[list[Path], Path | None]:
    extract_dir = tar_path.parent / "extracted"
    extract_dir.mkdir(parents=True, exist_ok=True)

    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=extract_dir)

    all_tex = sorted(extract_dir.rglob("*.tex"))
    main_tex = _find_main_tex(all_tex)

    return all_tex, main_tex


def _find_main_tex(tex_files: list[Path]) -> Path | None:
    for tex in tex_files:
        content = tex.read_text(encoding="utf-8", errors="replace")
        if "\\documentclass" in content:
            return tex

    if tex_files:
        return max(tex_files, key=lambda p: p.stat().st_size)

    return None


def cleanup(temp_path: Path) -> None:
    import shutil

    parent = temp_path.parent if temp_path.is_file() else temp_path
    if parent.exists():
        shutil.rmtree(parent, ignore_errors=True)


def download_and_extract(arxiv_id: str) -> tuple[list[Path], Path | None]:
    tar_path = download_source(arxiv_id)
    if tar_path is None:
        return [], None
    try:
        return extract_source(tar_path, arxiv_id)
    except Exception:
        cleanup(tar_path)
        raise
