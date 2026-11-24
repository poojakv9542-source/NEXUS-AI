from __future__ import annotations

import hashlib
import re
import shutil
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/files", tags=["File management"])

# All file operations are restricted to this dedicated folder.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = (PROJECT_ROOT / "workspace").resolve()
ALLOWED_TEXT = {".txt", ".md", ".csv", ".json", ".log"}
MAX_READ_BYTES = 2_000_000


def _safe_path(relative_path: str = "") -> Path:
    if not isinstance(relative_path, str):
        raise HTTPException(400, "Path must be text.")
    raw = relative_path.strip().replace("\\", "/")
    if raw.startswith("/") or re.match(r"^[A-Za-z]:", raw):
        raise HTTPException(400, "Use a path relative to the NEXUS workspace.")
    candidate = (WORKSPACE / raw).resolve()
    try:
        candidate.relative_to(WORKSPACE)
    except ValueError:
        raise HTTPException(403, "Access outside the NEXUS workspace is blocked.")
    if candidate == WORKSPACE and raw not in ("", "."):
        raise HTTPException(400, "Invalid workspace path.")
    return candidate


def _require_file(path: Path) -> None:
    if not path.exists() or not path.is_file():
        raise HTTPException(404, "File not found in the NEXUS workspace.")


class MoveRequest(BaseModel):
    source: str = Field(min_length=1)
    destination_folder: str = Field(min_length=1)
    confirm: bool = False


class RenameRequest(BaseModel):
    path: str = Field(min_length=1)
    new_name: str = Field(min_length=1)
    confirm: bool = False


class SummaryRequest(BaseModel):
    path: str = Field(min_length=1)


@router.get("/list")
def list_files(folder: str = ""):
    """CAP-001: List files and folders in a workspace folder."""
    target = _safe_path(folder)
    if not target.exists() or not target.is_dir():
        raise HTTPException(404, "Folder not found.")
    entries = []
    for item in sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
        if item.is_symlink():
            continue
        entries.append({
            "name": item.name,
            "type": "folder" if item.is_dir() else "file",
            "size_bytes": item.stat().st_size if item.is_file() else None,
            "relative_path": item.relative_to(WORKSPACE).as_posix()
        })
    return {"folder": folder or ".", "count": len(entries), "items": entries}


@router.get("/read")
def read_text_file(path: str):
    """CAP-002: Read supported text files."""
    target = _safe_path(path)
    _require_file(target)
    if target.suffix.lower() not in ALLOWED_TEXT:
        raise HTTPException(415, f"Supported text formats: {', '.join(sorted(ALLOWED_TEXT))}")
    if target.stat().st_size > MAX_READ_BYTES:
        raise HTTPException(413, "File is too large for this endpoint.")
    try:
        content = target.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise HTTPException(415, "File is not valid UTF-8 text.")
    return {"path": path, "content": content}


@router.get("/find")
def find_file(name: str, folder: str = ""):
    """CAP-003: Find files by exact or partial filename."""
    base = _safe_path(folder)
    if not base.exists() or not base.is_dir():
        raise HTTPException(404, "Folder not found.")
    matches = []
    for item in base.rglob("*"):
        if item.is_symlink():
            continue
        if item.is_file() and name.casefold() in item.name.casefold():
            matches.append(item.relative_to(WORKSPACE).as_posix())
    return {"query": name, "count": len(matches), "matches": matches[:500]}


@router.post("/organize")
def organize_file(request: MoveRequest):
    """CAP-004: Move a file into a workspace folder; requires explicit confirmation."""
    source = _safe_path(request.source)
    destination_dir = _safe_path(request.destination_folder)
    _require_file(source)
    if not destination_dir.exists() or not destination_dir.is_dir():
        raise HTTPException(404, "Destination folder does not exist.")
    destination = (destination_dir / source.name).resolve()
    try:
        destination.relative_to(WORKSPACE)
    except ValueError:
        raise HTTPException(403, "Destination outside workspace is blocked.")
    if destination.exists():
        raise HTTPException(409, "A file with that name already exists in the destination.")
    if not request.confirm:
        return {"preview": True, "requires_confirmation": True,
                "from": source.relative_to(WORKSPACE).as_posix(),
                "to": destination.relative_to(WORKSPACE).as_posix(),
                "message": "No file was moved. Repeat with confirm=true to perform the move."}
    shutil.move(str(source), str(destination))
    return {"success": True, "moved_to": destination.relative_to(WORKSPACE).as_posix()}


@router.post("/rename")
def rename_file(request: RenameRequest):
    """CAP-005: Rename a workspace file; requires explicit confirmation."""
    source = _safe_path(request.path)
    _require_file(source)
    if request.new_name in (".", "..") or "/" in request.new_name or "\\" in request.new_name:
        raise HTTPException(400, "new_name must be a filename only.")
    destination = (source.parent / request.new_name).resolve()
    if destination.exists():
        raise HTTPException(409, "A file with that name already exists.")
    if not request.confirm:
        return {"preview": True, "requires_confirmation": True,
                "from": source.relative_to(WORKSPACE).as_posix(),
                "to": destination.relative_to(WORKSPACE).as_posix(),
                "message": "No file was renamed. Repeat with confirm=true to perform the rename."}
    source.rename(destination)
    return {"success": True, "renamed_to": destination.relative_to(WORKSPACE).as_posix()}


@router.get("/duplicates")
def find_duplicates(folder: str = ""):
    """CAP-006: Identify duplicate files using SHA-256 hashes."""
    base = _safe_path(folder)
    if not base.exists() or not base.is_dir():
        raise HTTPException(404, "Folder not found.")
    groups: dict[str, list[str]] = {}
    for item in base.rglob("*"):
        if item.is_symlink() or not item.is_file():
            continue
        digest = hashlib.sha256(item.read_bytes()).hexdigest()
        groups.setdefault(digest, []).append(item.relative_to(WORKSPACE).as_posix())
    duplicates = [{"sha256": digest, "files": paths}
                  for digest, paths in groups.items() if len(paths) > 1]
    return {"duplicate_groups": len(duplicates), "duplicates": duplicates}


@router.post("/summarize")
def summarize_document(request: SummaryRequest):
    """CAP-007: Produce a simple extractive preview summary (not an LLM summary)."""
    target = _safe_path(request.path)
    _require_file(target)
    text = _extract_text(target)
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    summary = " ".join(sentences[:5])
    return {"path": request.path, "summary": summary[:2000],
            "method": "extractive_preview",
            "note": "This is a basic extractive summary. Local AI summarization will be connected later."}


@router.get("/extract")
def extract_document_text(path: str):
    """CAP-008: Extract text from supported text files and PDFs."""
    target = _safe_path(path)
    _require_file(target)
    return {"path": path, "text": _extract_text(target)}


def _extract_text(target: Path) -> str:
    suffix = target.suffix.lower()
    if suffix in ALLOWED_TEXT:
        if target.stat().st_size > MAX_READ_BYTES:
            raise HTTPException(413, "File is too large.")
        try:
            return target.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raise HTTPException(415, "File is not valid UTF-8 text.")
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError:
            raise HTTPException(501, "PDF support is not installed. Install pypdf using: python -m pip install pypdf")
        try:
            reader = PdfReader(str(target))
            return "\n".join(page.extract_text() or "" for page in reader.pages)[:100000]
        except Exception as exc:
            raise HTTPException(422, f"Could not extract PDF text: {exc}")
    raise HTTPException(415, "Supported formats: TXT, MD, CSV, JSON, LOG, PDF.")
