"""Entry point for the local multi-LLM coding workflow.

Usage:
  python ollama_workflow.py --web                  # start the Flask dashboard
  python ollama_workflow.py --health               # check configured endpoints
  python ollama_workflow.py --run "Requirement"    # run the pipeline headlessly
  python ollama_workflow.py "Requirement"          # alias of --run
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from workflow.config import ConfigError, load_config
from workflow.pipeline import Pipeline


def _run_headless(requirement: str, config_path: Optional[str]) -> int:
    try:
        config = load_config(config_path)
    except ConfigError as exc:
        print(f"Config error: {exc}", file=sys.stderr)
        return 1

    pipeline = Pipeline(config)
    result = pipeline.run(requirement)
    print("Workflow finished.")
    print(f"  run_id:    {result.run_id}")
    print(f"  status:    {result.status}")
    print(f"  duration:  {result.duration_s:.1f}s")
    print(f"  workspace: {result.workspace_dir}")
    if result.error:
        print(f"  error:     {result.error}", file=sys.stderr)
    if result.tickets:
        print(f"  tickets:   {len(result.tickets)}")
        for ticket in result.tickets:
            print(f"    - {ticket['ticket_id']} [{ticket['status']}] {ticket['title']}")
    return 0 if result.status != "failed" else 1


def _print_health(config_path: Optional[str]) -> int:
    try:
        config = load_config(config_path)
    except ConfigError as exc:
        print(f"Config error: {exc}", file=sys.stderr)
        return 1
    from webapp import collect_health

    health = collect_health(config)
    print(f"Overall: {health['status']}")
    for endpoint in health["endpoints"]:
        state = "OK" if endpoint["ok"] else f"DOWN ({endpoint['error']})"
        print(f"  endpoint {endpoint['name']}: {endpoint['url']} -> {state}")
        if endpoint["ok"]:
            print(f"    models: {', '.join(endpoint['models']) or '(none)'}")
    for role in health["roles"]:
        mark = "ready" if role["model_available"] else "MODEL MISSING"
        print(f"  role {role['role']}: {role['model']} @ {role['url']} ({mark})")
    return 0 if health["status"] == "ok" else 1


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run the local multi-LLM coding workflow.")
    parser.add_argument("requirement", nargs="?", help="the requirement to process")
    parser.add_argument("--run", dest="run", metavar="REQUIREMENT", help="run the pipeline headlessly")
    parser.add_argument("--web", action="store_true", help="start the Flask dashboard")
    parser.add_argument("--health", action="store_true", help="check configured endpoints")
    parser.add_argument("--config", default=None, help="path to config.yaml")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args(argv)

    if args.web:
        from webapp import create_app

        try:
            app = create_app(load_config(args.config))
        except ConfigError as exc:
            print(f"Config error: {exc}", file=sys.stderr)
            return 1
        app.run(host=args.host, port=args.port, debug=False)
        return 0

    if args.health:
        return _print_health(args.config)

    requirement = args.run or args.requirement
    if not requirement:
        requirement = input("What should the system do?\n> ").strip()
    if not requirement:
        print("A requirement is required.", file=sys.stderr)
        parser.print_help()
        return 1

    return _run_headless(requirement, args.config)


if __name__ == "__main__":
    raise SystemExit(main())
