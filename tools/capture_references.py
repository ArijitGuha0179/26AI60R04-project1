"""Capture unmodified GitHub chart regions and their accessible SVG metadata."""
import json
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/google-chrome', headless=True,
                                args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1600, 'height': 1200}, device_scale_factor=2,
                           timezone_id='UTC', color_scheme='light')
    for slug, folder, selector in [
        ('contributors', 'fig1-contributors', 'ul[class*="chartList__"]'),
        ('commit-activity', 'fig2-commits', 'react-app[data-target]'),
        ('code-frequency', 'fig3-code-frequency', 'react-app[data-target]'),
    ]:
        url = 'https://github.com/huggingface/diffusers/graphs/' + slug
        page.goto(url, wait_until='domcontentloaded')
        page.locator('.highcharts-container').first.wait_for(timeout=120000)
        page.wait_for_timeout(2000)
        root = page.locator('react-app').filter(has=page.locator('.highcharts-container')).last
        if slug == 'contributors':
            target = page.locator(selector)
        else:
            target = root
        target.screenshot(path=str(ROOT / folder / 'reference.png'))
        (ROOT / 'data' / (slug + '-final.html')).write_text(page.content())
        metadata = {'url': url, 'captured_at': datetime.now(timezone.utc).isoformat(),
                    'viewport': {'width':1600, 'height':1200}, 'device_scale_factor':2,
                    'region': target.bounding_box(), 'text': root.inner_text(),
                    'charts': page.locator('.highcharts-container').evaluate_all('''els => els.map(e => ({
                        width: e.clientWidth, height: e.clientHeight,
                        points: Array.from(e.querySelectorAll('.highcharts-point')).map(p=>p.getAttribute('aria-label')),
                        texts: Array.from(e.querySelectorAll('text')).map(p=>p.textContent)
                    }))''')}
        (ROOT / folder / 'reference-metadata.json').write_text(json.dumps(metadata, indent=2))
        if slug == 'contributors':
            target.screenshot(path=str(ROOT / 'fig4-top-committers' / 'reference.png'))
            (ROOT / 'fig4-top-committers' / 'reference-metadata.json').write_text(json.dumps(metadata, indent=2))
        print(slug, metadata['text'][:2200], flush=True)
    page.goto('https://github.com/huggingface/diffusers/pulse', wait_until='domcontentloaded')
    page.wait_for_timeout(10000)
    (ROOT / 'data' / 'pulse-rendered.html').write_text(page.content())
    print('PULSE', page.locator('main').inner_text()[-12000:], flush=True)
    browser.close()
