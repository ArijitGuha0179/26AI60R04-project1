"""Reproduce GitHub's 52-week commits chart from the saved CSV."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from plot_style import *
import pandas as pd
import matplotlib.dates as mdates

def main():
    folder=Path(__file__).resolve().parent
    df=pd.read_csv(folder/'raw_data.csv',parse_dates=['week'])
    fig=plt.figure(figsize=(8.96,5.25)); border(fig)
    heading(fig,'Commits','Number of commits per week')
    ax=fig.add_axes([.078,.094,.903,.752])
    ax.bar(df.week,df.commits,width=6.4,color=GREEN)
    ax.set_xlim(pd.Timestamp('2025-11-09'),pd.Timestamp('2026-11-15'))
    ax.set_ylim(0,60); ax.set_yticks(range(0,61,10))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.set_ylabel('Commits',labelpad=14)
    axes_style(ax)
    save(fig,folder)

if __name__=='__main__': main()
