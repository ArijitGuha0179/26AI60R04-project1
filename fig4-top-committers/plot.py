"""Reproduce the actual Pulse Top committers chart, including avatar labels."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from plot_style import *
import pandas as pd
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def main():
    folder=Path(__file__).resolve().parent
    df=pd.read_csv(folder/'raw_data.csv')
    fig=plt.figure(figsize=(4.40,2.07)); border(fig)
    fig.text(.038,.86,'Top committers',fontsize=12,weight='bold',va='center')
    ax=fig.add_axes([.159,.25,.803,.430])
    ax.bar(np.arange(len(df)),df.commits,width=.5,color='#137e56')
    ax.set_xlim(-.5,len(df)-.5); ax.set_ylim(0,40); ax.set_yticks([0,20,40])
    ax.set_xticks([]); ax.set_ylabel('Commits',labelpad=5)
    axes_style(ax)
    for i,name in enumerate(df.author):
        image=plt.imread(folder/'avatars'/(name+'.png'))
        icon=OffsetImage(image,zoom=12/image.shape[0],resample=True)
        ab=AnnotationBbox(icon,(i,0),xybox=(0,-16),xycoords='data',boxcoords='offset points',
                          frameon=True,pad=.03,bboxprops={'edgecolor':'#d0d7de','linewidth':.5})
        ax.add_artist(ab)
    save(fig,folder)

if __name__=='__main__': main()
