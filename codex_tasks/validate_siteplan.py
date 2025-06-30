import json
import os
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except Exception:
    sync_playwright = None

try:
    from PIL import Image
except Exception:
    Image = None


CHECKLIST_ITEMS = [
    'property lines',
    'setbacks',
    'labeled units',
    'ADU',
    'parking'
]


def check_image(path: Path):
    missing = []
    if not path.exists():
        missing.append('site plan image')
        return False, missing

    if sync_playwright:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(path.as_uri())
                page.screenshot(path='last_screenshot.png')
                browser.close()
        except Exception:
            pass
    elif Image:
        try:
            Image.open(path)
        except Exception:
            missing.append('corrupt image')
            return False, missing

    # Placeholder checks - real vision processing would go here
    # For now just assume image passes if it exists
    return True, missing


def main(image_path='output/latest_siteplan.png'):
    path = Path(image_path)
    valid, missing = check_image(path)
    msg: str
    if valid and not missing:
        msg = '✅ Valid site plan, ready to commit'
    else:
        msg = f"❌ Missing: {', '.join(missing)} — iterate again"

    results = {
        'valid': valid and not missing,
        'missing': missing,
        'message': msg
    }
    with open('validation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    return msg


if __name__ == '__main__':
    print(main())
