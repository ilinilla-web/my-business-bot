"""Lead persistence for project inquiries."""
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
    "niche",
    "task",
    "contact",
]


@dataclass
class Lead:
    timestamp: str
    user_id: int
    username: str
    full_name: str
    niche: str
    task: str
    contact: str


def _ensure_file() -> None:
    directory = os.path.dirname(LEADS_FILE)
    if directory:
        os.makedirs(directory, exist_ok=True)
    if not os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDNAMES).writeheader()


def save_lead(
    *,
    user_id: int,
    username: str,
    full_name: str,
    niche: str,
    task: str,
    contact: str,
) -> Lead:
    lead = Lead(
        timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        user_id=user_id,
        username=username or "",
        full_name=full_name or "",
        niche=niche or "",
        task=task or "",
        contact=contact or "",
    )
    _ensure_file()
    with open(LEADS_FILE, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=FIELDNAMES).writerow(asdict(lead))

    logger.info(
        "New inquiry: niche=%r task=%r contact=%r user_id=%s @%s",
        niche,
        task,
        contact,
        user_id,
        username,
    )
    print(
        "NEW INQUIRY\n"
        f"  niche:    {lead.niche}\n"
        f"  task:     {lead.task}\n"
        f"  contact:  {lead.contact}\n"
        f"  username: @{lead.username or 'N/A'}\n"
        f"  user_id:  {lead.user_id}",
        flush=True,
    )
    return lead
