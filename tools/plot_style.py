"""Shared Matplotlib styling for the captured GitHub light theme."""
import os
from pathlib import Path
cache = Path(__file__).resolve().parents[1]/'.tools'/'cache'
cache.mkdir(parents=True,exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR',str(cache/'matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME',str(cache))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BLUE = '#006dde'
GREEN = '#2da44e'
RED = '#e60028'
MUTED = '#59636e'
GRID = '#d8e1e8'

plt.rcParams.update({'font.family':'Liberation Sans', 'font.size':9,
                     'text.color':'#1f2328', 'axes.labelcolor':MUTED,
                     'xtick.color':MUTED, 'ytick.color':MUTED,
                     'axes.edgecolor':'#d0d7de', 'axes.linewidth':0.7,
                     'savefig.facecolor':'white'})

def border(fig, x=0.001,y=0.001,w=0.998,h=0.998):
    fig.add_artist(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0,rounding_size=0.008',
                                 transform=fig.transFigure,facecolor='white',
                                 edgecolor='#d0d7de',linewidth=.7,zorder=-1))

def axes_style(ax, right=False, vertical=False):
    ax.set_axisbelow(True)
    ax.grid(axis='both' if vertical else 'y',color=GRID,linewidth=.65,linestyle=(0,(4,3)))
    for side in ['left','top','right']:
        ax.spines[side].set_visible(False)
    ax.tick_params(axis='both',length=0,pad=10)
    if right:
        ax.yaxis.tick_right()
        ax.yaxis.set_label_position('right')

def heading(fig,title,subtitle=None):
    fig.text(.019,.945,title,fontsize=12,weight='bold',va='center')
    if subtitle:
        fig.text(.019,.900,subtitle,fontsize=9,color=MUTED,va='center')

def save(fig,folder):
    fig.savefig(folder/'generated.png',dpi=200)
    plt.close(fig)
