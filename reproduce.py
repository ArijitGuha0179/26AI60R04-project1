"""Regenerate the four figures offline from committed CSV files."""
from pathlib import Path
import runpy

root=Path(__file__).resolve().parent
for folder in sorted(root.glob('fig[1-4]-*')):
    runpy.run_path(str(folder/'plot.py'),run_name='__main__')
    print('Generated',folder.name+'/generated.png')
