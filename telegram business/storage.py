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

FIELDNAMES = [
    "timestamp",
    "user_id",
    "username",
    "full_name",
    "name",
    "phone",
    "category",
    "task",
    "photo_file_id",
]


@dataclass
class Lead:
    timestamp: str
    user_id: int
    username: str
    full_name: str
    name: str
    phone: str
    category: str
    task: str
    photo_file_id: str


def _ensure_file() -> None:
    """Create the leads directory/file with a header row if missing."""
    directory = os.path.dirname(LEADS_FILE)
    if directory:
        os.makedirs(directory, exist_ok=True)
    if not os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def save_lead(
    *,
    user_id: int,
    username: str,
    full_name: str,
    name: str,
    phone: str,
    task: str = "",
    category: str = "",
    photo_file_id: str = "",
) -> Lead:
    """Persist a new lead, print it to the console, and return the record."""
    lead = Lead(
        timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        user_id=user_id,
        username=username or "",
        full_name=full_name or "",
        name=name,
        phone=phone,
        category=category or "",
        task=task or "",
        photo_file_id=photo_file_id or "",
    )

    _ensure_file()
    with open(LEADS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(asdict(lead))

    logger.info(
        "New lead captured: name=%r phone=%r category=%r task=%r photo=%s user_id=%s username=%r",
        name,
        phone,
        category,
        task,
        bool(photo_file_id),
        user_id,
        username,
    )
    print(
        "NEW LEAD\n"
        f"  name:     {lead.name}\n"
        f"  phone:    {lead.phone}\n"
        f"  category: {lead.category}\n"
        f"  task:     {lead.task}\n"
        f"  photo:    {lead.photo_file_id or '-'}\n"
        f"  username: @{lead.username or 'N/A'}\n"
        f"  user_id:  {lead.user_id}",
        flush=True,
    )
    return lead
