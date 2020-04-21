import fss_functions
import fss_extended as fsse
import matplotlib.pyplot as plt
import numpy as np
import random
import seaborn as sns
import warnings
import matplotlib.colors as mplcolors

# suppress FutureWarning message spam
warnings.simplefilter(action='ignore', category=FutureWarning)

# generates ideal precipitation fields and calculates the resulting FSS
#
# blah

# random.seed(12345)  # comment for different result each time

out_subdir = "biggly/"
# random.seed(2)

def make_levels(obs,mods):
    maxmax = 0.1*np.ceil(10*max(np.max(obs),np.max(np.asarray(mods))))
    minmin = 0.1*np.floor(10*min(np.min(obs),np.min(np.asarray(mods))))
    print('minimum of precipitation fields is %5.2f' % minmin)
    print('maximum of precipitation fields is %5.2f' % maxmax)
    levels3 = np.arange(minmin, maxmax+0.01, 0.2)
    levels1 = np.arange(min(levels3), max(levels3)+0.01, 0.05)
    while len(levels1)>20:
        levels1=np.delete(levels1, np.arange(1,levels1.size, 2))
        levels3=np.delete(levels3, np.arange(1,levels3.size, 2))
        print('max of levels array are %5.2f and %5.2f' % (max(levels1),max(levels3)))
        while max(levels1) < maxmax:
            newmax1 = levels1[-1] + levels1[-1] - levels1[-2]
            print('max of levels1 is too low, appending %5.2f' % newmax1)
            levels1 = np.append(levels1, newmax1)
        while max(levels3) < maxmax:
            newmax3 = levels3[-1] + levels3[-1] - levels3[-2]
            print('max of levels3 is too low, appending %5.2f' % newmax3)
            levels3 = np.append(levels3, newmax3)
    return(levels1, levels3)    


def panel_size(n):
    lins = 1
    cols = 1
    increment_line = False
    while lins*cols < n:
        if increment_line:
            lins += 1
            increment_line = False
        else:
            cols += 1
            increment_line = True
    return lins, cols


def draw_fields(xx, yy, obs, mods, levels1, levels3, random_seed=0):
    colormap = 'GnBu'
    lins, cols = panel_size(len(mods)+1)
    fig, axs = plt.subplots(lins, cols, figsize=(8*cols, 8*lins), sharex=True, sharey=True)
    # draw pseudo obs
    jj = 0
    h_list = []
    c1 = []
    c2 = []
    c3 = []
    for line in axs:
        for ax in line:
            if jj <= len(mods):
                print('jj is '+str(jj))
                if jj == 0:
                    zz = obs
                    title_string = 'observations'
                else:
                    zz = mods[jj-1]
                    mae = np.mean(np.abs(zz-obs))
                    bias = np.mean(zz-obs)
                    title_string = 'forecast (bias = {:5.2f}, mae = {:5.2f}'.format(bias, mae)
                c1.append(ax.contourf(xx, yy, zz, levels=levels1,
                                     cmap=colormap, alpha=0.8))
                c2.append(ax.contour(xx, yy, zz, levels3,
                                     colors='black', linewidths=0.8))
                # label thicker contours
                ax.clabel(c2[-1], inline=True, fmt='%3.1f', fontsize=8)
                # thin contours
                c3.append(ax.contour(xx, yy, zz, levels=levels1,
                                     colors='black', linewidths=0.3))
                ax.clabel(c3[-1], inline=True, fmt='%3.1f', fontsize=8)
                ax.set_title(title_string)
                ax.set_xlabel('x [lenght units from center]')
                ax.set_ylabel('y [lenght units from center]')
                jj += 1
    print('saving...')
    plt.savefig(out_subdir+'{:03d}_pseudo_obs_and_model.png'.format(random_seed))
    plt.close('all')
    return 0

    # draw pseudo model
    # c2 = axs[1].contourf(xx, yy, mod, levels=levels1,
    #                      cmap=colormap, alpha=0.8)
    # c2b = axs[1].contour(xx, yy, mod, levels3,
    #                      colors='black', linewidths=0.8)
    # axs[1].clabel(c2b, inline=True, fmt='%3.1f', fontsize=8)
    # c2c = axs[1].contour(xx, yy, mod, levels=levels1,
    #                      colors='black', linewidths=0.3)
    # axs[1].clabel(c2c, inline=True, fmt='%3.1f', fontsize=8)
    # axs[1].set_title('forecast (bias = %5.2f, mae = %5.2f' % (bias, mae))
    # axs[1].set_xlabel('x [lenght units from center]')


def draw_fss_heatmaps(fss_scores, vmin=0, vmax=0.95, random_seed=0):
    lins, cols = panel_size(len(fss_scores))
    jj = -1
    # draw a seaborn heatmap
    f, axs = plt.subplots(lins, cols, figsize=(8*cols, 8*lins))
    for line in axs:
        for ax in line:
            if jj >= 0 and jj < len(fss_scores):
                sns.heatmap(fss_scores[jj], annot=True, fmt="4.2f", linewidths=.5, ax=ax,
                            vmin=vmin, vmax=vmax, cmap='RdYlGn')
                plt.title('FSS scores for artifical observations and forecast')
                plt.xlabel('window size [length units]')
                plt.ylabel('thresholds [automatically generated]')
            jj += 1
    plt.savefig(out_subdir+'{:03d}_FSS_scores.png'.format(random_seed))


def draw_fss_heatmap_useful(fss_scores, vmin=0, vmax=0.75, random_seed=0):
    lins, cols = panel_size(len(fss_scores))
    jj = -1
    # draw a seaborn heatmap
    f, axs = plt.subplots(lins, cols, figsize=(8*cols, 8*lins))
    print(len(fss_scores))
    for line in axs:
        for ax in line:
            if jj >= 0 and jj < len(fss_scores):
                print(jj)
                sns.heatmap(fss_scores[jj], annot=True, fmt="4.2f", linewidths=.5, ax=ax,
                            vmin=vmin, vmax=vmax, cmap='RdYlGn')
                plt.title('FSS minus usefulness threshold')
                plt.xlabel('window size [grid points]')
                plt.ylabel('threshold')
            jj += 1
    plt.savefig(out_subdir+'{:03d}_useful.png'.format(random_seed))


def make_imshow_pretty(ax, windows, thresholds):
    xticks = range(len(windows))
    yticks = range(thresholds.shape[0])
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ydict = {}
    xdict = {}
    for tt in range(thresholds.shape[0]):
        ydict[tt] = "{:.1f}".format(thresholds[tt])
    for ww, window in enumerate(windows):
        xdict[ww] = "{:d}".format(window)
    xlabels = [xticks[i] if t not in xdict.keys() else xdict[t] for i,t in enumerate(xticks)]
    ylabels = [yticks[i] if t not in ydict.keys() else ydict[t] for i,t in enumerate(yticks)]
    ax.set_xticklabels(xlabels, rotation='vertical')
    ax.set_yticklabels(ylabels)
    ax.tick_params(axis='both', which='major', labelsize=5)
    ax.grid(color='w', linewidth=1.5)
    return ax


def draw_rank_heatmap(fss_rank_array, windows, thresholds, n_mods, random_seed=0):
    fss_rank_cols = ['white']*(n_mods+3)
    max_rank = np.max(fss_rank_array)
    print(len(fss_rank_cols))
    # print("max rank is {} and color table has {} colors".format(data_list[0]['max_rank'], len(fss_rank_cols)))
    fss_rank_cols[0:5] = ['black', 'red', 'limegreen', 'gold', 'silver', 'darkorange']
    # print fss_rank_cols
    fss_cmap = mplcolors.ListedColormap(fss_rank_cols)
    lins, cols = panel_size(n_mods)
    jj = -1
    # draw a seaborn heatmap
    f, axs = plt.subplots(lins, cols, figsize=(4*cols, 4*lins)) #, dpi=160)
    for line in axs:
        for ax in line:
            if jj >= 0 and jj < n_mods:
                print(jj)
                #sns.heatmap(fss_rank_array[jj,:,:], cmap=fss_cmap, ax=ax)
                extent = (0, fss_rank_array.shape[2], fss_rank_array.shape[1], 0)
                ax.imshow(fss_rank_array[jj,:,:], cmap=fss_cmap, aspect='auto', vmin=0., vmax=max_rank,
                    extent=extent)
                #ax.grid(color='w', linewidth=1.0)
                            # vmin=vmin, vmax=vmax, cmap='RdYlGn')
                ax.set_title('FSS ranking')
                if (jj+1)/lins == cols-1:
                    ax.set_xlabel('window size [grid points]')
                if jj%cols == cols-1:
                    ax.set_ylabel('threshold')
                ax = make_imshow_pretty(ax, windows, thresholds)
            jj += 1
    plt.savefig(out_subdir+'{:03d}_ranks.png'.format(random_seed))
    
def r(minimum,maximum):
    return random.uniform(minimum,maximum)


def genfield(xx, yy, n_mods=2, random_seed=1):
    # example: sum of 5 randomly placed gaussian mountains
    random.seed = random_seed
    obs = 0. * xx
    dispersion = 50
    for ii in range(15):
        a1 = r(-dispersion, dispersion)
        b1 = r(-dispersion, dispersion)
        obs = obs + np.exp(-np.sqrt((xx - a1) ** 2 + (yy - b1) ** 2) / r(5,15))
    mods = []
    for kk in range(n_mods):
        mod_tmp = 0. * xx
        for ll in range(15):
            a2 = r(-dispersion, dispersion)
            b2 = r(-dispersion, dispersion)
            mod_tmp = mod_tmp + np.exp(-np.sqrt((xx - a2) ** 2 + (yy - b2) ** 2) / r(5,15))
        mod_tmp = 5.*(mod_tmp - np.min(mod_tmp))
        mods.append(mod_tmp)
    # normalize min to zero
    obs = 5.*(obs - np.min(obs))
    # return with max normalzed to 1
    # return (obs / np.max(obs), mod / np.max(mod))
    return (obs, mods)


def main():
    # make a meshgrid and two randoms fields
    print('generating pseudo obs and model')
    x = np.arange(-50, 51, 1)
    xx, yy = np.meshgrid(x, x)
    n_mods = 48
    for seed in range(10,13):
        obs, mods = genfield(xx, yy, n_mods=n_mods, random_seed=seed)
        levels1, levels3 = make_levels(obs,mods)
        # draw the two fields
        print('drawing pseudo obs and model')
        draw_fields(xx, yy, obs, mods, levels1, levels3, random_seed=seed)
        # calculate FSS
        #levels = np.arange(0.05, 1., 0.05)
        maxmax = max(np.max(obs),np.max(np.asarray(mods)))+0.3
        levels = np.round(levels1, decimals=1).flatten() #np.round(np.arange(0.1, maxmax, maxmax/14.),
            #decimals = 1)
        # windows=[1,2,3,5,10,15,20,25,30,40,50,60,75,100,150,200]
        windows = range(10, 120, 10)
        print('calculating FSS')
        fss_scores = []
        for mod in mods:
            fss_scores.append(fss_functions.fss_strip(mod, obs, windows, levels, lparallel=True))
        # draw FSS
        print('drawing FSS')
        draw_fss_heatmaps(fss_scores, random_seed=seed)
        # get threshold and subtract from scores, then draw again
        fss_array = np.zeros([n_mods, len(levels), len(windows)])
        for ii, fss in enumerate(fss_scores):
            fss_array[ii,:,:] = fss.to_numpy()
        fss_rank_array = np.zeros(fss_array.shape)
        fo_list = []
        for ll in levels:
            fo_list.append(0.5 * (1 + float((obs > ll).sum()) / float(obs.size)))
        for tt, threshold in enumerate(levels):
            for ww, window in enumerate(windows):
                fss_rank_array[:, tt, ww] = fsse.rank_array(fss_array[:, tt, ww], fo_list[tt])
        draw_rank_heatmap(fss_rank_array, windows, levels, n_mods, random_seed=seed)
        for fss_score in fss_scores:
            for wins in windows:
                fss_score[wins] = fss_score[wins] - fo_list
        print('drawing usefullness plot')
        draw_fss_heatmap_useful(fss_scores, vmin=-0.2, vmax=0.2, random_seed=seed)
        

if __name__ == '__main__':
    main()
