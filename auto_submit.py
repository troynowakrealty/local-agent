import json
import subprocess
import os

BRANCH = 'auto-submission'


def main():
    if not os.path.exists('validation_results.json'):
        print('No validation results.')
        return
    with open('validation_results.json') as f:
        data = json.load(f)
    if not data.get('valid'):
        print('Validation failed, not submitting.')
        return

    subprocess.run(['git', 'checkout', '-B', BRANCH], check=False)
    subprocess.run(['git', 'add', 'validation_results.json'], check=False)
    if os.path.exists('output/latest_siteplan.png'):
        subprocess.run(['git', 'add', 'output/latest_siteplan.png'], check=False)
    subprocess.run(['git', 'commit', '-m', 'Auto commit of valid site plan'], check=False)
    subprocess.run(['git', 'push', 'origin', BRANCH], check=False)
    print('Submitted to GitHub on branch', BRANCH)


if __name__ == '__main__':
    main()
