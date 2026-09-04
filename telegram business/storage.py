"""Lead persistence.

Every captured lead is:
  1. Appended as a row to a CSV file (easy to open in Excel/Google Sheets).
  2. Emitted to the application log via the "leads" logger.

This is intentionally simple (no external database) so the project runs
out-of-the-box. Swap `save_lead` internals for a real database or CRM/webhook
call in production if needed.
"""
import csv
import logging
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone

from config import LEADS_FILE

logger = logging.getLogger("leads")

FIELDNAMES = ["timestamp", "user_id", "username", "full_name", "name", "phone"]


@dataclass
class Lead:
    timestamp: str
    user_id: int
    username: str
    full_name: str
    name: str
    phone: str


def _ensure_file() -> None:
    """Create the leads directory/file with a header row if missing."""
    directory = os.path.dirname(LEADS_FILE)
    if directory:
        os.makedirs(directory, exist_ok=True)
    if not os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def save_lead(*, user_id: int, username: str, full_name: str, name: str, phone: str) -> Lead:
    """Persist a new lead and return the stored record."""
    lead = Lead(
        timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        user_id=user_id,
        username=username or "",
        full_name=full_name or "",
        name=name,
        phone=phone,
    )

    _ensure_file()
    with open(LEADS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(asdict(lead))

    logger.info(
        "New lead captured: name=%r phone=%r user_id=%s username=%r",
        name,
        phone,
        user_id,
        username,
    )
    return lead
