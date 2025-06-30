#!/usr/bin/env python3
"""Simple helper to send commands to the local Flask agent."""
import argparse
import requests
from utils.ensure_agent_alive import ensure_agent_alive


def main() -> None:
    parser = argparse.ArgumentParser(description="Run command via local agent")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command to execute")
    args = parser.parse_args()

    cmd = " ".join(args.command).strip()
    if not cmd:
        parser.error("command required")

    if ensure_agent_alive():
        resp = requests.post(
            "http://localhost:5001/run-task",
            json={"command": cmd},
            timeout=30,
        )
        try:
            print(resp.json())
        except Exception:
            print(resp.text)
    else:
        print("❌ Agent failed to restart — check logs.")


if __name__ == "__main__":
    main()
