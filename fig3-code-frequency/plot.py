"""Match GitHub's monthly display grouping of weekly code-frequency data."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from plot_style import *
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

def main():
    folder=Path(__file__).resolve().parent
    weekly=pd.read_csv(folder/'raw_data.csv',parse_dates=['week'])
    df=weekly.set_index('week').resample('MS')[['additions','deletions']].sum()
    fig=plt.figure(figsize=(8.96,5.25)); border(fig)
    heading(fig,'Code frequency','Additions and deletions per week')
    ax=fig.add_axes([.019,.094,.780,.752])
    ax.bar(df.index,df.additions,width=28,color=GREEN,label='Additions',edgecolor='white',linewidth=.5)
    ax.bar(df.index,df.deletions,width=28,color=RED,label='Deletions',edgecolor='white',linewidth=.5)
    ax.set_xlim(pd.Timestamp('2022-04-16'),pd.Timestamp('2026-11-16'))
    ax.set_ylim(-75000,100000)
    ax.set_yticks(range(-75000,100000,25000))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p: '0' if v==0 else f'{v/1000:g}k'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1,7]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    axes_style(ax,right=True,vertical=True)
    ax.set_ylabel('Frequency',rotation=270,labelpad=20)
    ax.legend(loc='center left',bbox_to_anchor=(1.10,.48),frameon=False,handlelength=1,handleheight=1)
    save(fig,folder)

if __name__=='__main__': main()
