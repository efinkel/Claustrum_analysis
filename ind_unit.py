import scipy as sp
import scipy.io
import os
import numpy as np
import pandas as pd
from collections import Iterable
import matplotlib.pylab as mpl
from IPython.html import widgets
from IPython.display import display

font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 24}

mpl.rc('font', **font)
mpl.rc('xtick', labelsize=20) 
mpl.rc('ytick', labelsize=20)
mpl.rc('axes', labelsize=20)

def plot_unit(df_dict, s_key, alignment, n, x_min, x_max):
	if s_key == 0:
		print('0')
		return
	else:
		
		df = df_dict[s_key]
		#df = pd.DataFrame(df[0], index = [)
		ind_units = df[['mouse_name', 'date', 'cluster_name']].drop_duplicates()
		
		
		mouse = df['mouse_name'] == ind_units.iloc[n,0]
		date =  df['date'] == ind_units.iloc[n,1]
		cluster_name = df['cluster_name'] == ind_units.iloc[n,2]
		current_cell = df[mouse & date & cluster_name]


		cell_TT = current_cell[(current_cell['block_type'] == 'Whisker') &\
										   (current_cell['trial_type'] == 'Stim_Som_NoCue')]
		cell_TV = current_cell[(current_cell['block_type'] == 'Whisker') &\
										   (current_cell['trial_type'] == 'Stim_Vis_NoCue')]
		cell_VV = current_cell[(current_cell['block_type'] == 'Visual') &\
										   (current_cell['trial_type'] == 'Stim_Vis_NoCue')]
		cell_VT = current_cell[(current_cell['block_type'] == 'Visual') &\
										   (current_cell['trial_type'] == 'Stim_Som_NoCue')]
		
		import rasters_and_psth as r
		rasters = [cell_VT, cell_TT, cell_TV, cell_VV]
		fig = r.plot_rasters(rasters, [x_min, x_max], 0.05, alignment)[0]
		
		return fig