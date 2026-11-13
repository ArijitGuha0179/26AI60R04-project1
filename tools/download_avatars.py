"""Download the same public avatar assets used in GitHub's reference charts."""
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

root = Path(__file__).resolve().parents[1]
jobs=[]
for filename, folder, selector in [
    ('contributors-final.html','fig1-contributors','li[class*="chartListItem__"] img'),
    ('pulse-rendered.html','fig4-top-committers','.highcharts-xaxis-labels img')]:
    soup = BeautifulSoup((root/'data'/filename).read_text(),'html.parser')
    target = root/folder/'avatars'
    target.mkdir(exist_ok=True)
    for img in soup.select(selector):
        name = img.get('alt','').lstrip('@')
        if not name and img.find_parent('li'):
            name = img.find_parent('li').select_one('h2 a').get_text(strip=True)
        if name:
            jobs.append((img['src'],target/(name+'.png')))

def fetch(job):
    import subprocess
    url,path=job
    result=subprocess.run(['curl','-fLsS','--max-time','20',url],check=True,capture_output=True)
    Image.open(BytesIO(result.stdout)).convert('RGBA').save(path)
    print(path.name,flush=True)

with ThreadPoolExecutor(max_workers=8) as pool:
    list(pool.map(fetch,jobs))
