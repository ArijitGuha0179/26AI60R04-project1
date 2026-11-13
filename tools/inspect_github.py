"""Inspect live GitHub charts and retain network responses for reproducibility."""
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/google-chrome', headless=True,
                                args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1600, 'height': 1200}, device_scale_factor=1)
    def response(r):
        if any(s in r.url for s in ['contributors-data', 'commit-activity-data', 'code-frequency-data', 'top-committers']):
            try:
                body = r.body()
                name = r.url.split('/')[-1].split('?')[0]
                (ROOT / 'data' / (name + '.json')).write_bytes(body)
                print(r.status, r.url, len(body), flush=True)
            except Exception as e:
                print(str(e), flush=True)
    page.on('response', response)
    for slug in ['contributors', 'commit-activity', 'code-frequency', 'top-committers']:
        page.goto('https://github.com/huggingface/diffusers/graphs/' + slug, wait_until='domcontentloaded')
        page.wait_for_timeout(20000)
        (ROOT / 'data' / (slug + '-rendered.html')).write_text(page.content())
        page.screenshot(path=str(ROOT / 'data' / (slug + '-page.png')), full_page=True)
        print(slug, page.locator('main').inner_text()[-12000:], flush=True)
    browser.close()
