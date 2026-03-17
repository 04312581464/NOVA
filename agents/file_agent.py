from __future__ import annotations

import os
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from .base import AgentResult, BaseNovaAgent


def _safe_home_dir() -> Path:
    return Path(os.path.expanduser("~"))


def _downloads_dir() -> Path:
    # Works for most Windows setups; falls back safely
    return _safe_home_dir() / "Downloads"


@dataclass
class OrganizeRules:
    by_ext: Dict[str, str]


DEFAULT_RULES = OrganizeRules(
    by_ext={
        ".pdf": "Documents",
        ".doc": "Documents",
        ".docx": "Documents",
        ".ppt": "Documents",
        ".pptx": "Documents",
        ".xls": "Documents",
        ".xlsx": "Documents",
        ".zip": "Archives",
        ".rar": "Archives",
        ".7z": "Archives",
        ".jpg": "Images",
        ".jpeg": "Images",
        ".png": "Images",
        ".gif": "Images",
        ".webp": "Images",
        ".mp4": "Videos",
        ".mkv": "Videos",
        ".mp3": "Audio",
        ".wav": "Audio",
        ".exe": "Installers",
        ".msi": "Installers",
    }
)


class FileAgent(BaseNovaAgent):
    name = "file_agent"

    def __init__(self, rules: Optional[OrganizeRules] = None):
        self.rules = rules or DEFAULT_RULES

    def match(self, text: str, ctx=None) -> float:
        t = (text or "").lower()
        keywords = ["file", "folder", "organize", "rename", "downloads", "cleanup", "clean", "junk"]
        return 0.7 if any(k in t for k in keywords) else 0.0

    def run(self, text: str, ctx=None) -> AgentResult:
        res = AgentResult(agent=self.name, confidence=self.match(text, ctx))
        if res.confidence <= 0:
            return res
        res.directives.append("Prefer safe file operations. Confirm before deleting anything outside temp/downloads. Log any changes made for transparency.")
        res.tool_hints.append("If needed, use universal_file_opener or create_here for file actions; keep actions minimal and reversible.")
        return res

    def organize_downloads(self, downloads_dir: Optional[Path] = None, dry_run: bool = False) -> Dict[str, int]:
        ddir = downloads_dir or _downloads_dir()
        if not ddir.exists():
            return {"moved": 0, "skipped": 0}
        moved = 0
        skipped = 0
        for p in ddir.iterdir():
            if p.is_dir():
                continue
            ext = p.suffix.lower()
            bucket = self.rules.by_ext.get(ext)
            if not bucket:
                skipped += 1
                continue
            target_dir = ddir / bucket
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / p.name
            if target.exists():
                stem = re.sub(r"\s+", " ", p.stem).strip()
                ts = datetime.now().strftime("%Y%m%d-%H%M%S")
                target = target_dir / f"{stem}-{ts}{p.suffix}"
            if not dry_run:
                shutil.move(str(p), str(target))
            moved += 1
        return {"moved": moved, "skipped": skipped}

