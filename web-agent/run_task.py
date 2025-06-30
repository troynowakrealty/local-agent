import argparse
import importlib
import json
import logging
import subprocess

logging.basicConfig(
    filename='run_task.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)


def run_task(task_name, **kwargs):
    if task_name.endswith('.js'):
        cmd = ['node', f'codex_tasks/{task_name}']
        for k, v in kwargs.items():
            cmd.append(f'--{k}={v}')
        logging.info('Running node task: %s', cmd)
        result = subprocess.run(cmd, capture_output=True, text=True)
        logging.info('Result: %s', result.stdout)
        return result.stdout
    else:
        try:
            module = importlib.import_module(f'codex_tasks.{task_name}')
        except ImportError as e:
            raise RuntimeError(f'Task {task_name} not found: {e}')
        if not hasattr(module, 'main'):
            raise RuntimeError(f'Task {task_name} has no `main` function')
        logging.info('Running python task %s with %s', task_name, kwargs)
        res = module.main(**kwargs)
        logging.info('Result: %s', res)
        return res


def cli():
    parser = argparse.ArgumentParser(description='Run codex task')
    parser.add_argument('task')
    parser.add_argument('--params', default='{}')
    args = parser.parse_args()
    kwargs = json.loads(args.params)
    print(run_task(args.task, **kwargs))


if __name__ == '__main__':
    cli()
