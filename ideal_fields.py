import fss_functions
import matplotlib.pyplot as plt
import numpy as np
import random
import seaborn as sns
import warnings

# suppress FutureWarning message spam
warnings.simplefilter(action='ignore', category=FutureWarning)

# generates ideal precipitation fields and calculates the resulting FSS
#
# blah

# random.seed(12345)  # comment for different result each time


# random.seed(2)

def make_levels(obs,mod):
    maxmax = 0.1*np.ceil(10*max(np.max(obs),np.max(mod)))
    minmin = 0.1*np.floor(10*min(np.min(obs),np.min(mod)))
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

def draw_fields(xx, yy, obs, mod, levels1, levels3):
    colormap = 'GnBu'
    mae = np.mean(np.abs(mod-obs))
    bias = np.mean(mod-obs)
    fig, axs = plt.subplots(1, 2, figsize=(16, 8), sharex=True, sharey=True)
    # draw pseudo obs
    c1 = axs[0].contourf(xx, yy, obs, levels=levels1,
                         cmap=colormap, alpha=0.8)
    c1b = axs[0].contour(xx, yy, obs, levels3,
                         colors='black', linewidths=0.8)
    # label thicker contours
    axs[0].clabel(c1b, inline=True, fmt='%3.1f', fontsize=8)
    # thin contours
    c1c = axs[0].contour(xx, yy, obs, levels=levels1,
                         colors='black', linewidths=0.3)
    axs[0].clabel(c1c, inline=True, fmt='%3.1f', fontsize=8)
    axs[0].set_title('observations')
    axs[0].set_xlabel('x [lenght units from center]')
    axs[0].set_ylabel('y [lenght units from center]')
    # draw pseudo model
    c2 = axs[1].contourf(xx, yy, mod, levels=levels1,
                         cmap=colormap, alpha=0.8)
    c2b = axs[1].contour(xx, yy, mod, levels3,
                         colors='black', linewidths=0.8)
    axs[1].clabel(c2b, inline=True, fmt='%3.1f', fontsize=8)
    c2c = axs[1].contour(xx, yy, mod, levels=levels1,
                         colors='black', linewidths=0.3)
    axs[1].clabel(c2c, inline=True, fmt='%3.1f', fontsize=8)
    axs[1].set_title('forecast (bias = %5.2f, mae = %5.2f' % (bias, mae))
    axs[1].set_xlabel('x [lenght units from center]')
    plt.savefig('pseudo_obs_and_model.png')
    plt.close('all')


def draw_fss_heatmaps(fss_scores, vmin=0, vmax=0.75):
    # draw a seaborn heatmap
    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(fss_scores, annot=True, fmt="4.2f", linewidths=.5, ax=ax,
                vmin=vmin, vmax=vmax, cmap='RdYlGn')
    plt.title('FSS scores for artifical observations and forecast')
    plt.xlabel('window size [length units]')
    plt.ylabel('thresholds [automatically generated]')
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


def r(minimum,maximum):
    return random.uniform(minimum,maximum)


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
        for ii in range(5):
            a1 = r(-100, 100)
            b1 = r(-100, 100)
            a2 = r(-100, 100)
            b2 = r(-100, 100)
            obs = obs + np.exp(-np.sqrt((xx - a1) ** 2 + (yy - b1) ** 2) / r(1,65))
            mod = mod + np.exp(-np.sqrt((xx - a2) ** 2 + (yy - b2) ** 2) / r(1,65))
            # normalize min to zero
        obs = 5.*(obs - np.min(obs))
        mod = 5.*(mod - np.min(mod))
    # return with max normalzed to 1
    # return (obs / np.max(obs), mod / np.max(mod))
    return (obs, mod)


def main():
    # make a meshgrid and two randoms fields
    print('generating pseudo obs and model')
    x = np.arange(-50, 51, 1)
    xx, yy = np.meshgrid(x, x)
    obs, mod = genfield(xx, yy, random_field=True)
    levels1, levels3 = make_levels(obs,mod)
    # draw the two fields
    print('drawing pseudo obs and model')
    draw_fields(xx, yy, obs, mod, levels1, levels3)
    # calculate FSS
    #levels = np.arange(0.05, 1., 0.05)
    maxmax = max(np.max(obs),np.max(mod))+0.3
    levels = np.round(levels1, decimals=1) #np.round(np.arange(0.1, maxmax, maxmax/14.),
        #decimals = 1)
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
