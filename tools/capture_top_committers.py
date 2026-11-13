"""Refresh the Pulse reference and CSV only after every avatar label loads."""
from pathlib import Path
import json
import csv
import re
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1600,'height':1200},device_scale_factor=2,color_scheme='light')
    page.goto('https://github.com/huggingface/diffusers/pulse',wait_until='domcontentloaded')
    page.locator('.highcharts-point').first.wait_for(timeout=120000)
    chart=page.locator('div[class*="ChartCardContainerBordered__"]').first
    chart.scroll_into_view_if_needed()
    page.wait_for_function('''() => {
      const imgs=[...document.querySelectorAll('.highcharts-xaxis-labels img')];
      return imgs.length>0 && imgs.every(i=>i.complete && i.naturalWidth>0);
    }''',timeout=60000)
    page.wait_for_timeout(1500)
    images=page.locator('.highcharts-xaxis-labels img').evaluate_all('''es=>es.map(i=>({author:i.alt,loaded:i.complete && i.naturalWidth>0}))''')
    points=page.locator('.highcharts-point').evaluate_all('es=>es.map(e=>e.getAttribute("aria-label"))')
    body=page.locator('main').inner_text()
    period=re.search(r'(\w+ \d+, \d{4})\s*[–—]\s*(\w+ \d+, \d{4})',body)
    assert period, 'Pulse period could not be read'
    start,end=[datetime.strptime(s,'%B %d, %Y').date().isoformat() for s in period.groups()]
    rows=[]
    for rank,label in enumerate(points,1):
        m=re.fullmatch(r'(.+), ([\d,]+)\. Commits\.',label)
        assert m,label
        rows.append(dict(rank=rank,author=m[1],commits=int(m[2].replace(',','')),period_start=start,period_end=end))
    assert [i['author'] for i in images]==[r['author'] for r in rows]
    assert all(i['loaded'] for i in images)
    folder=root/'fig4-top-committers'
    chart.screenshot(path=str(folder/'reference.png'))
    metadata={'url':page.url,'captured_at':datetime.now(timezone.utc).isoformat(),
              'period':f'{start} to {end}','scope':'Pulse chart author counts as displayed',
              'text':chart.inner_text(),'region':chart.bounding_box(),
              'category_labels':images,
              'charts':page.locator('.highcharts-container').evaluate_all('''es=>es.map(e=>({
                width:e.clientWidth,height:e.clientHeight,
                points:[...e.querySelectorAll('.highcharts-point')].map(p=>p.getAttribute('aria-label')),
                texts:[...e.querySelectorAll('text')].map(p=>p.textContent)
              }))''')}
    (folder/'reference-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    (root/'data/pulse-rendered.html').write_text(page.content())
    with (folder/'raw_data.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    print(f'Captured {len(rows)} author counts with all avatar labels loaded; period {start} to {end}.')
    print([(r['author'],r['commits']) for r in rows])
    browser.close()
