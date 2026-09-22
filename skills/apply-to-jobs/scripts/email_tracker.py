#!/usr/bin/env python3
"""Store minimal deduplication state for job-search email alerts.

The tracker intentionally stores metadata only. Never pass message bodies,
verification codes, assessment tokens, or signed URLs to this script.

  email_tracker.py seen --id MESSAGE_ID
  email_tracker.py add --id MESSAGE_ID --kind interview --sender NAME \
      --subject SUBJECT --received ISO_TIME [--company C] [--role R]
  email_tracker.py status
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def root() -> Path:
    value = os.environ.get("JOBS_ROOT")
    return Path(value).resolve() if value else Path(__file__).resolve().parents[3]


def state_path() -> Path:
    return root() / "private" / "email-tracker.json"


def load() -> dict:
    path = state_path()
    if not path.exists():
        return {"version": 1, "last_successful_check": None, "events": []}
    return json.loads(path.read_text())


def save(data: dict) -> None:
    path = state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    tmp.chmod(0o600)
    os.replace(tmp, path)


def fingerprint(value: str) -> str:
    return hashlib.sha256(value.strip().encode()).hexdigest()[:24]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    seen = sub.add_parser("seen")
    seen.add_argument("--id", required=True)

    add = sub.add_parser("add")
    add.add_argument("--id", required=True)
    add.add_argument("--kind", required=True, choices=(
        "interview", "recruiter-screen", "oa", "coding-assessment",
        "take-home", "offer", "deadline", "action-required",
        "auth-required", "auth-restored"))
    add.add_argument("--sender", default="")
    add.add_argument("--subject", default="")
    add.add_argument("--received", default="")
    add.add_argument("--company", default="")
    add.add_argument("--role", default="")

    sub.add_parser("status")
    checked = sub.add_parser("checked")
    checked.add_argument("--at", default="")

    args = parser.parse_args()
    data = load()
    key = fingerprint(args.id) if hasattr(args, "id") else ""

    if args.command == "seen":
        match = next((event for event in data["events"] if event["key"] == key), None)
        print(json.dumps({"seen": bool(match), "event": match}, ensure_ascii=False))
        return

    if args.command == "add":
        added = not any(event["key"] == key for event in data["events"])
        if added:
            data["events"].append({
                "key": key,
                "kind": args.kind,
                "sender": args.sender,
                "subject": args.subject,
                "received": args.received,
                "company": args.company,
                "role": args.role,
                "recorded": now(),
            })
            data["events"] = data["events"][-1000:]
            save(data)
        print(json.dumps({"added": added, "key": key}, ensure_ascii=False))
        return

    if args.command == "checked":
        data["last_successful_check"] = args.at or now()
        save(data)
        print(json.dumps({"last_successful_check": data["last_successful_check"]}))
        return

    print(json.dumps({
        "last_successful_check": data.get("last_successful_check"),
        "events": len(data.get("events", [])),
        "path": str(state_path()),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
