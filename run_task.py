import argparse
import importlib
import json
import logging
from pathlib import Path

logging.basicConfig(filename="run_task.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def run_task(task_name, **kwargs):
    """Dynamically load and run a task from codex_tasks."""
    try:
        module = importlib.import_module(f"codex_tasks.{task_name}")
    except ImportError as e:
        raise RuntimeError(f"Task {task_name} not found: {e}")

    if not hasattr(module, "main"):
        raise RuntimeError(f"Task {task_name} has no `main` function")

    logging.info("Running task %s with %s", task_name, kwargs)
    result = module.main(**kwargs)
    logging.info("Result: %s", result)
    return result


def cli():
    parser = argparse.ArgumentParser(description="Run registered Codex task")
    parser.add_argument("task", help="Task name inside codex_tasks package")
    parser.add_argument("--params", default="{}", help="JSON string with params")
    args = parser.parse_args()
    kwargs = json.loads(args.params)
    res = run_task(args.task, **kwargs)
    print(res)


if __name__ == "__main__":
    cli()
