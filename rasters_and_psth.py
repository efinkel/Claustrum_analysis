
def plot_rasters(rasters, window, bin_size, alignment):

	import scipy.io
	import os
	import numpy as np
	import pandas as pd
	from collections import Iterable
	import matplotlib.pylab as mpl
	from matplotlib import gridspec

	
	mpl.close('all')
	fig = mpl.figure(figsize=(16, 14))
	first_raster = rasters[0]
	#fig.suptitle(rasters[0].iloc[0,0] +', '+ rasters[0].iloc[0, 1] +', '+ rasters[0].iloc[0, 13], size = 22)

	trial_type = 0
	gs = gridspec.GridSpec(3, 2, height_ratios=[1, 11, 11])
	ax1 = fig.add_subplot(gs[0])
	ax2 = fig.add_subplot(gs[1], sharex=ax1, sharey=ax1)
	ax3 = fig.add_subplot(gs[2], sharex=ax1)
	ax4 = fig.add_subplot(gs[3], sharex=ax1, sharey=ax3)
	ax5 = fig.add_subplot(gs[4])
	ax6 = fig.add_subplot(gs[5], sharex = ax1, sharey=ax5)

	all_ax=[ax3,ax4]
	import matplotlib.patches as patches

	ax1.set_xlim(window[0],window[1])
	ax1.set_ylim(0,2)

	ax1.axis('off')
	ax2.axis('off')
	hists = []
	
	
	
	
	if len(rasters) == 10:
		trace_arrangement = [4,4]
	elif len(rasters) == 6:
		trace_arrangement = [4,2]
		colors = ['#9ecae1', '#3182bd', 'C1', '#fdc42a',[0.6, 0.6, 0.6], [0.7, 0.7, 0.7] ]
		ax1.set_title('Lick Trials', size = 20)
		ax2.set_title('No-Lick Trials', size = 20)
		if  alignment == 'spike_times(stim_aligned)':
			ax1.add_patch(patches.Rectangle((0,0), 0.15, 1, facecolor = 'k'))
			ax2.add_patch(patches.Rectangle((0,0), 0.15, 1, facecolor = 'k')) 
	else:
		trace_arrangement = [2,2]
		ax1.set_title('Tactile Trials', size = 20)
		ax2.set_title('Visual Trials', size = 20)
		colors = [[0.6, 0.6, 0.6], 'C0', [0.6, 0.6, 0.6], '#ff7f0e', [0.6, 0.6, 0.6]]
		if  alignment == 'spike_times(stim_aligned)':
			ax1.add_patch(patches.Rectangle((0,0), 0.15, 1, facecolor = colors[1], alpha = 0.5))
			ax2.add_patch(patches.Rectangle((0,0), 0.15, 1, facecolor = colors[3], alpha = 0.5)) 
	stim_colors = ['#08519c', '#d95f0e']

	#trace_arrangement = [2,2]
	for stim_type in range(2):
		ax = all_ax[stim_type]

		mpl.sca(ax)
		trial_total = 0
		for i in range(trace_arrangement[stim_type]):
			ras = rasters[trial_type]
			spike_counts = []
			for trial, spike in enumerate(ras[alignment]):
				spike = spike[(spike>window[0]) & (spike<=window[1])]
				mpl.vlines(spike, trial + trial_total + .5, trial + trial_total + 1.5)
				if alignment == 'spike_times(lick_aligned)':
					mpl.vlines(ras.iloc[trial]['first_lick']*-1, trial + trial_total + .5, trial + trial_total + 1.5, color = stim_colors[stim_type], linewidth = 5)
					mpl.vlines(ras.iloc[trial]['first_lick'] - ras.iloc[trial]['first_lick'], trial + trial_total + .5, trial + trial_total + 1.5, color = 'r', linewidth = 5)
					mpl.vlines(ras.iloc[trial]['last_lick'] - ras.iloc[trial]['first_lick'], trial + trial_total + .5, trial + trial_total + 1.5, color = 'm', linewidth = 5)
				elif alignment == 'spike_times(last_lick_aligned)':
					mpl.vlines(ras.iloc[trial]['last_lick']*-1, trial + trial_total + .5, trial + trial_total + 1.5, color = stim_colors[stim_type], linewidth = 5)
					mpl.vlines(ras.iloc[trial]['first_lick']-ras.iloc[trial]['last_lick'], trial + trial_total + .5, trial + trial_total + 1.5, color = 'r', linewidth = 5)
					mpl.vlines(ras.iloc[trial]['last_lick']-ras.iloc[trial]['last_lick'], trial + trial_total + .5, trial + trial_total + 1.5, color = 'm', linewidth = 5)
				else:
					mpl.vlines(ras.iloc[trial]['first_lick'], trial + trial_total + .5, trial + trial_total + 1.5, color = 'r', linewidth = 5)
					mpl.vlines(ras.iloc[trial]['last_lick'], trial + trial_total + .5, trial + trial_total + 1.5, color = 'm', linewidth = 5)

				
				spike = spike[(spike>window[0]) & (spike<=window[1])]
				edges = np.arange(window[0], window[1], bin_size)
				count, _ = np.histogram(spike,edges)
				spike_counts.append(count)
			hists.append(np.array(spike_counts))
			
			step = 0
			if trial_type == 1 or trial_type==3:
				c1= 0.5
				c2 = 1
			else:
				c1 = 0
				c2 = 0.5
			step = step +1

			ax.add_patch(patches.Rectangle((window[0],trial_total+c1), window[1]-window[0], trial + c2, facecolor = colors[trial_type], alpha = 0.5)) 
			trial_total += trial
			trial_type += 1
		mpl.autoscale(enable=True, tight=True)
		ax.spines['right'].set_visible(False)
		ax.spines['top'].set_visible(False)
		ax.xaxis.set_ticks_position('bottom')
		ax.yaxis.set_ticks_position('left')
		ax.set_xlim(window)
		mpl.xlabel('Time(s)', fontsize = 18)
		mpl.ylabel('Trials', fontsize= 18)
		
	from scipy import stats
	average_hists = []
	SE_hists =[]
	for hist in hists:
		average_hists.append(np.mean(hist, axis=0)/bin_size)
		SE_hists.append(stats.sem(hist)/bin_size)
		
	
	all_ax2 = [ax5, ax6]
	
	hist_num = 0

	colors = ['C0', '#ff7f0e']
	for i, ax in enumerate(all_ax2):

		ax.plot(edges[0:-1], average_hists[hist_num], color = [0.6,0.6,0.6])
		ax.fill_between(edges[0:-1], average_hists[hist_num]-SE_hists[hist_num],
						average_hists[hist_num]+SE_hists[hist_num], alpha = 0.5, color = [0.6,0.6,0.6])
		ax.plot(edges[0:-1], average_hists[hist_num+1], color = colors[i])
		ax.fill_between(edges[0:-1], average_hists[hist_num+1]-SE_hists[hist_num+1],
						average_hists[hist_num+1]+SE_hists[hist_num+1], alpha = 0.5, color = colors[i])
		hist_num +=2
		
		mpl.autoscale(enable=True, tight=True)
		ax.spines['right'].set_visible(False)
		ax.spines['top'].set_visible(False)
		ax.xaxis.set_ticks_position('bottom')
		ax.yaxis.set_ticks_position('left')
		ax.set_xlim(window)
		ax.set_xlabel('Time(s)', fontsize = 18)
		ax.set_ylabel('Firing Rate (Hz)', fontsize= 18)
		
		
	return fig, average_hists, SE_hists