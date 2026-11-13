"""Reproduce the first ten GitHub contributor cards from raw_data.csv."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from plot_style import *
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def main():
    folder=Path(__file__).resolve().parent
    df=pd.read_csv(folder/'raw_data.csv',parse_dates=['week'])
    fig=plt.figure(figsize=(8.96,11.69))
    for rank, data in df.groupby('rank',sort=True):
        row,col=divmod(rank-1,2)
        x=col*.509; top=1-row*.203
        border(fig,x+.001,top-.189,.490,.188)
        name=data.author.iloc[0]
        fig.text(x+.073,top-.026,name,fontsize=11.5,weight='bold',color=BLUE,va='center')
        fig.text(x+.073,top-.046,f'{data.commits.sum()} commits',fontsize=8.5,color=MUTED,va='center')
        fig.text(x+.229,top-.046,f'{data.additions.sum():,} ++',fontsize=8.2,color='#00852b',va='center')
        fig.text(x+.365,top-.046,f'{data.deletions.sum():,} --',fontsize=8.2,color='#e00020',va='center')
        fig.text(x+.426,top-.027,f'#{rank}',fontsize=8.5,color=MUTED,ha='center',va='center')
        avatar=folder/'avatars'/(name+'.png')
        if avatar.exists():
            aa=fig.add_axes([x+.019,top-.052,.045,.0345]); aa.imshow(plt.imread(avatar)); aa.axis('off')
        ax=fig.add_axes([x+.019,top-.147,.405,.077])
        ax.bar(data.week,data.commits,width=6.8,color=BLUE,edgecolor='white',linewidth=.4)
        ax.set_xlim(pd.Timestamp('2026-08-04'),pd.Timestamp('2026-11-12'))
        ax.set_ylim(0,40); ax.set_yticks([0,10,20,30])
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.tick_params(labelsize=8.5)
        axes_style(ax,right=True,vertical=True)
        ax.set_ylabel('Contributions',fontsize=8.5,rotation=270,labelpad=15)
    save(fig,folder)

if __name__=='__main__': main()
