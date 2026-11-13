"""Convert saved GitHub responses and rendered chart values to explicit CSVs."""
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
def write(folder, name, fields, rows):
    with (ROOT / folder / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def date(epoch):
    return datetime.fromtimestamp(epoch, timezone.utc).date().isoformat()

def main():
    contributors = json.loads((ROOT/'data/contributors-data.json').read_text())
    soup = BeautifulSoup((ROOT/'data/contributors-final.html').read_text(), 'html.parser')
    names = [li.select_one('h2 a').get_text(strip=True)
             for li in soup.select('li[class*="chartListItem__"]')[:10]]
    lookup = {c['author']['login']: c for c in contributors}
    rows = []
    for rank, name in enumerate(names, 1):
        for w in lookup[name]['weeks']:
            if '2026-08-09' <= date(w['w']) <= '2026-11-08':
                rows.append(dict(rank=rank, author=name, week=date(w['w']),
                                 commits=w['c'], additions=w['a'], deletions=w['d']))
    write('fig1-contributors','raw_data.csv',list(rows[0]),rows)
    all_rows = [dict(author=c['author']['login'],week=date(w['w']),commits=w['c'],
                     additions=w['a'],deletions=w['d']) for c in contributors for w in c['weeks']]
    write('fig1-contributors','all_contributors.csv',list(all_rows[0]),all_rows)
    data = json.loads((ROOT/'data/commit-activity-data.json').read_text())
    rows = [dict(week=date(w['week']),commits=w['total'],
                 **dict(zip(['sun','mon','tue','wed','thu','fri','sat'],w['days']))) for w in data]
    write('fig2-commits','raw_data.csv',list(rows[0]),rows)
    data = json.loads((ROOT/'data/code-frequency-data.json').read_text())
    rows = [dict(week=date(w),additions=a,deletions=d) for w,a,d in data]
    write('fig3-code-frequency','raw_data.csv',list(rows[0]),rows)
    # Highcharts groups the weekly data into calendar months at this viewport.
    monthly = {}
    for w in rows:
        key = w['week'][:7]+'-01'
        bucket = monthly.setdefault(key, dict(month=key, additions=0, deletions=0))
        bucket['additions'] += w['additions']
        bucket['deletions'] += w['deletions']
    write('fig3-code-frequency','displayed_data.csv',['month','additions','deletions'],monthly.values())
    soup = BeautifulSoup((ROOT/'data/pulse-rendered.html').read_text(),'html.parser')
    rows = []
    for rank, point in enumerate(soup.select('.highcharts-point[aria-label]'),1):
        match = re.fullmatch(r'(.+), ([\d,]+)\. Commits\.',point['aria-label'])
        if match:
            name, n = match.groups()
            rows.append(dict(rank=rank,author=name,commits=int(n.replace(',','')),
                             period_start='2026-11-05',period_end='2026-11-12'))
    write('fig4-top-committers','raw_data.csv',list(rows[0]),rows)
    print('CSV export complete: 10 contributors, 52 commit weeks,',len(data),'code-frequency weeks,',len(rows),'top committers')

if __name__ == '__main__':
    main()
