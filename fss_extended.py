import numpy as np


def get_quadrants(df_fss, precip_threshold=None, window_size_threshold=None):
    """ arguments:
    df_fss .................. pandas dataframe containing FSS data
    precip_threshold ........ float
    window_size_threshold ... int

    Splits an FSS dataframe into 4 quadrants. If no thresholds are given,
    the split attempts to make the quadrants equal size. The smaller windows
    and higher precpitation parts are rounded down if size is uneven.

    Returns:
    df_small_high ..... pandas dataframe for small scale high precipitation
    df_large_high ..... pandas dataframe for large scale high precipitation
    df_small_low ...... pandas dataframe for small scale low precipitation
    df_large_low ...... pandas dataframe for large scale low precipitation
    """
    df_small_low  = df_fss[0:df_fss.axes[0][int(np.floor(len(df_fss.axes[0])/2.))]   ][df_fss.axes[1][0:int(np.floor(len(df_fss.axes[1])/2.))   ]]
    df_small_high = df_fss[  df_fss.axes[0][int(np.floor(len(df_fss.axes[0])/2.))]+1:][df_fss.axes[1][0:int(np.floor(len(df_fss.axes[1])/2.))   ]]
    df_large_low  = df_fss[0:df_fss.axes[0][int(np.floor(len(df_fss.axes[0])/2.))]   ][df_fss.axes[1][  int(np.floor(len(df_fss.axes[1])/2.))+1:]]
    df_large_high = df_fss[  df_fss.axes[0][int(np.floor(len(df_fss.axes[0])/2.))]+1:][df_fss.axes[1][  int(np.floor(len(df_fss.axes[1])/2.))+1:]]
    return df_small_low, df_small_high, df_large_low, df_large_high


def rank_array(a,t):
    """
    dirty and cumbersome ranking funktion for a 1d numpy array

    implemented to circumnavigate the shortcomings of built-in sorting functions
    1. rank NaN with 0
    2. rank anything below the 0.5+0.5f threshold with rank 1
    3. rank perfect scores with 2
    4. rank the rest 3 and higher
       - Rank 3 ..... gold
       - Rank 4 ..... silver
       - Rank 5 ..... bronze
       - Rank 6+ .... white
    5. equal values get the same rank
    6. if N values are equal, the next N-1 tanks are skipped

    Ranks 3 and higher are valid ranks
    """
    # print("Threshold is {:7.5f} Array to rank:".format(t))
    # print(a)
    ranks = np.zeros(len(a))
    for ii in range(len(a)):
        # sort out missing vlaues (-> black)
        if np.isnan(a[ii]):
            a[ii] = -99.
            ranks[ii] = 0.
        # sort out useless values (below the no-skill threshold, -> red)
        elif a[ii] < t:
            a[ii] = -98.
            ranks[ii] = 1.
    jj = 2.
    same = 0.
    previous = -999.
    for ii in range(len(a)):
        if a.max() > -88.:
            idx = np.argmax(a)
            if a[idx] > -88.:
                # deal with perfect ranks first (-> green)
                # print("a[{}] is {}".format(idx, a[idx]))
                if a[idx] == 1.:
                    ranks[idx] = 2.
                    jj += 1.
                    a[idx] = -97.
                else:
                    # increment to 3 for gold (best rank but not perfect)
                    # if no perfect score was fond before!
                    # this will catch all other ranks
                    if jj == 2.:
                        jj += 1. 
                    if a[idx] == previous:
                        same += 1.
                    else:
                        same = 0.
                    ranks[idx] = jj - same
                    jj += 1.
                    previous = a[idx]
                    a[idx] = -88.
        else:
            break
    # for ii, rank in enumerate(ranks):
        # print("{}: {} is ranked at {}".format(ii, b[ii], rank))
    return ranks