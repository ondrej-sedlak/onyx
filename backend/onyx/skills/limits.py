"""Per-user skill limits for writes.

A user's own write may not move them from within these limits to past them.
"""

from dataclasses import dataclass
from typing import Final

from pydantic import BaseModel

SKILL_WRITE_MAX_BYTES: Final[int] = 500 * 1024 * 1024
SKILL_WRITE_MAX_FILES: Final[int] = 5_000


@dataclass(frozen=True)
class SkillUsage:
    """Unpacked size and file count of skills."""

    bytes: int = 0
    files: int = 0

    def __add__(self, other: "SkillUsage") -> "SkillUsage":
        return SkillUsage(
            bytes=self.bytes + other.bytes, files=self.files + other.files
        )

    def __sub__(self, other: "SkillUsage") -> "SkillUsage":
        return SkillUsage(
            bytes=self.bytes - other.bytes, files=self.files - other.files
        )

    def grew_from(self, other: "SkillUsage") -> bool:
        return self.bytes > other.bytes or self.files > other.files

    @property
    def is_over_write_limit(self) -> bool:
        return self.bytes > SKILL_WRITE_MAX_BYTES or self.files > SKILL_WRITE_MAX_FILES


class SkillUsageModel(BaseModel):
    bytes: int
    files: int


class SkillLimitRefusal(BaseModel):
    """Why a write was refused: the acting user's usage after it, and the
    write limits."""

    usage: SkillUsageModel
    max_bytes: int
    max_files: int
