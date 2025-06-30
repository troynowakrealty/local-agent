import json
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except Exception:
    sync_playwright = None

try:
    from PIL import Image, ImageChops
except Exception:
    Image = None


def take_screenshot(url: str, output: Path) -> None:
    if not sync_playwright:
        raise RuntimeError('playwright is not installed')
    output.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.screenshot(path=str(output), full_page=True)
        browser.close()


def images_match(img_a: Path, img_b: Path) -> bool:
    if not Image:
        raise RuntimeError('Pillow is not installed')
    with Image.open(img_a) as a, Image.open(img_b) as b:
        diff = ImageChops.difference(a.convert('RGB'), b.convert('RGB'))
        return diff.getbbox() is None


def main(url: str, expected_image: str, screenshot_path: str = 'output/layout_actual.png') -> str:
    expected = Path(expected_image)
    if not expected.exists():
        raise FileNotFoundError(f'expected image not found: {expected}')

    screenshot = Path(screenshot_path)
    take_screenshot(url, screenshot)
    match = images_match(screenshot, expected)

    results = {
        'url': url,
        'expected': str(expected),
        'actual': str(screenshot),
        'match': match
    }
    with open('layout_check.json', 'w') as f:
        json.dump(results, f, indent=2)

    return '✅ Layout matches expected image' if match else '❌ Layout mismatch'


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Verify webpage layout against an expected image')
    parser.add_argument('url')
    parser.add_argument('expected_image')
    parser.add_argument('--screenshot', default='output/layout_actual.png')
    args = parser.parse_args()
    print(main(args.url, args.expected_image, args.screenshot))
