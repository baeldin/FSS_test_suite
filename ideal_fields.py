import numpy as np
import fss_functions
import matplotlib.pyplot as plt
import seaborn as sns
import random

# generates ideal precipitation fields and calculates the resulting FSS
#
# blah

random.seed(12345)  # comment for different result each time


# random.seed(2)

def draw_fields(xx, yy, obs, mod):
    maxmax = max(np.max(obs),np.max(mod))+0.1
    minmin = min(np.min(obs),np.min(mod))-0.05
    colormap = 'GnBu'
    levels1 = np.round(np.arange(minmin, maxmax, maxmax/20.), decimals = 1)
    levels2 = np.round(np.arange(minmin, maxmax, maxmax/20.), decimals = 1)
    levels3 = np.round(np.arange(minmin, maxmax, maxmax/10.), decimals = 1)
    fig, axs = plt.subplots(1, 2, figsize=(12, 6), sharex=True, sharey=True)
    # draw pseudo obs
    c1 = axs[0].contourf(xx, yy, obs, levels=levels1,
                         cmap=colormap, alpha=0.8)
    c1b = axs[0].contour(xx, yy, obs, levels2,
                         colors='black', linewidths=0.8)
    # label thicker contours
    axs[0].clabel(c1b, inline=True, fmt='%3.1f', fontsize=8)
    # thin contours
    c1c = axs[0].contour(xx, yy, obs, levels=levels3,
                         colors='black', linewidths=0.3)
    axs[0].set_title('observations')
    axs[0].set_xlabel('x [lenght units from center]')
    axs[0].set_ylabel('y [lenght units from center]')
    # draw pseudo model
    c2 = axs[1].contourf(xx, yy, mod, levels=levels1,
                         cmap=colormap, alpha=0.8)
    c2b = axs[1].contour(xx, yy, mod, levels2,
                         colors='black', linewidths=0.8)
    axs[1].clabel(c2b, inline=True, fmt='%3.1f', fontsize=8)
    c2c = axs[1].contour(xx, yy, mod, levels=levels3,
                         colors='black', linewidths=0.3)
    axs[1].set_title('forecast')
    axs[1].set_xlabel('x [lenght units from center]')
    plt.savefig('pseudo_obs_and_model.png')
    plt.close('all')


def draw_fss_heatmaps(fss_scores, vmin=0, vmax=0.75):
    # draw a seaborn heatmap
    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(fss_scores, annot=True, fmt="4.2f", linewidths=.5, ax=ax,
                vmin=vmin, vmax=vmax, cmap='RdYlGn')
    plt.title('FSS scores for idealized obs and model')
    plt.xlabel('window size [length units]')
    plt.ylabel('threshold')
    plt.savefig('FSS_scores.png')


def draw_fss_heatmap_useful(fss_scores, vmin=0, vmax=0.75):
    # draw a seaborn heatmap
    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(fss_scores, annot=True, fmt="4.2f", linewidths=.5, ax=ax,
                vmin=vmin, vmax=vmax, cmap='RdYlGn')
    plt.title('FSS minus usefulness threshold')
    plt.xlabel('window size [grid points]')
    plt.ylabel('threshold')
    plt.savefig('useful.png')


def genfield(xx, yy, random_field=False):
    if not random_field:
        # example: two gaussian mountains, same size, shifted
        obs = np.exp(-np.sqrt(xx ** 2 + yy ** 2) / 5.)
        mod = np.exp(-np.sqrt((xx - 15) ** 2 + yy ** 2) / 5.)
        # obs=1-0.5*np.sin(xx/5.)
        # mod=1-0.5*np.sin(((0.5*xx+0.5*yy)-3.1415926)/5.)
    else:
        # example: sum of 5 randomly placed gaussian mountains
        obs = 0. * xx
        mod = 0. * xx
        for ii in range(3):
            a1 = random.uniform(-60, 60)
            b1 = random.uniform(-60, 60)
            a2 = random.uniform(-60, 60)
            b2 = random.uniform(-60, 60)
            obs = obs + np.exp(-np.sqrt((xx - a1) ** 2 + (yy - b1) ** 2) / 49.)
            mod = mod + np.exp(-np.sqrt((xx - a2) ** 2 + (yy - b2) ** 2) / 49.)
            # normalize min to zero
            # obs = obs - np.min(obs)
            # mod = mod - np.min(mod)
    # return with max normalzed to 1
    # return (obs / np.max(obs), mod / np.max(mod))
    return (obs, mod)


def main():
    # make a meshgrid and two randoms fields
    print('generating pseudo obs and model')
    x = np.arange(-50, 51, 1)
    xx, yy = np.meshgrid(x, x)
    obs, mod = genfield(xx, yy, random_field=True)
    # draw the two fields
    print('drawing pseudo obs and model')
    draw_fields(xx, yy, obs, mod)
    # calculate FSS
    #levels = np.arange(0.05, 1., 0.05)
    maxmax = max(np.max(obs),np.max(mod))+0.3
    levels = np.round(np.arange(0.1, maxmax, maxmax/14.),
        decimals = 1)
    # windows=[1,2,3,5,10,15,20,25,30,40,50,60,75,100,150,200]
    windows = range(10, 120, 10)
    print('calculating FSS')
    fss_scores = fss_functions.fss_strip(mod, obs, windows, levels, lparallel=True)
    # draw FSS
    print('drawing FSS')
    draw_fss_heatmaps(fss_scores)
    # get threshold and subtract from scores, then draw again
    fo_list = []
    for ll in levels:
        fo_list.append(0.5 * (1 + float((obs > ll).sum()) / float(obs.size)))
    for wins in windows:
        fss_scores[wins] = fss_scores[wins] - fo_list
    print('drawing usefullness plot')
    draw_fss_heatmap_useful(fss_scores, vmin=-0.2, vmax=0.2)


if __name__ == '__main__':
    main()
