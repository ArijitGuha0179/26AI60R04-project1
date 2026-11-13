"""Check plotted values against independently captured GitHub chart labels."""
import json
import re
from datetime import datetime
from pathlib import Path
import pandas as pd
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
results={}
for folder in sorted(ROOT.glob('fig[1-4]-*')):
    df=pd.read_csv(folder/'raw_data.csv')
    metadata=json.loads((folder/'reference-metadata.json').read_text())
    assert not df.empty and df.notna().all().all()
    for image in ['generated.png','reference.png']:
        with Image.open(folder/image) as im: im.verify()
    if folder.name.startswith('fig1'):
        count=0
        for rank,data in df.groupby('rank'):
            chart=metadata['charts'][rank]
            captured=[]
            for label in chart['points']:
                m=re.fullmatch(r'\w+, (.+), ([\d,]+)\. Contributions\.',label or '')
                if not m:
                    m=re.fullmatch(r'\w+, (.+), ([\d,]+)\. Commits\.',label or '')
                assert m, label
                captured.append((datetime.strptime(m[1],'%b %d, %Y').date().isoformat(),int(m[2].replace(',',''))))
            expected=list(zip(data.week,data.commits))
            assert captured==expected,(rank,captured,expected)
            count+=len(captured)
    elif folder.name.startswith('fig2'):
        values=[int(re.search(r', ([\d,]+)\. Commits\.',p)[1].replace(',','')) for p in metadata['charts'][0]['points']]
        assert values==df.commits.tolist()
        assert (df[['sun','mon','tue','wed','thu','fri','sat']].sum(axis=1)==df.commits).all()
        count=len(values)
    elif folder.name.startswith('fig3'):
        monthly=df.assign(month=df.week.str[:7]).groupby('month')[['additions','deletions']].sum()
        count=0
        for p in metadata['charts'][0]['points']:
            if not p: continue
            m=re.fullmatch(r'(\w+ \d{4}), (-?[\d,]+)\. (Additions|Deletions)\.',p)
            assert m,p
            key=datetime.strptime(m[1],'%B %Y').strftime('%Y-%m')
            assert monthly.loc[key,m[3].lower()]==int(m[2].replace(',','')),(key,p)
            count+=1
        assert count==2*len(monthly)
        assert (df.additions>=0).all() and (df.deletions<=0).all()
    else:
        captured=[]
        for p in metadata['charts'][0]['points']:
            m=re.fullmatch(r'(.+), ([\d,]+)\. Commits\.',p)
            captured.append((m[1],int(m[2].replace(',',''))))
        assert captured==list(zip(df.author,df.commits))
        count=len(captured)
    results[folder.name]={'raw_rows':len(df),'reference_values_checked':count,'max_absolute_error':0}
    print(folder.name,':',count,'reference values match exactly')
(ROOT/'validation.json').write_text(json.dumps(results,indent=2)+'\n')
