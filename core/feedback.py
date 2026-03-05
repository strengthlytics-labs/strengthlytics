# core/feedback.py

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class FeedbackEntry:
    text: str
    feedback_date: date = field(default_factory=date.today)
    source: Optional[str] = None
    context: Optional[str] = None
    entry_type: Optional[str] = None

    def __post_init__(self):
        self.text = (self.text or "").strip()

        if not self.text:
            raise ValueError("Feedback text cannot be empty")

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "feedback_date": self.feedback_date,
            "source": self.source,
            "context": self.context,
            "entry_type": self.entry_type,
        }