# -*- coding: utf-8; -*-
"""
Import module function to plot dipole vectors from a typical dipole moment processed output. Data is in dataframe df
which is passed together with X,Y-coordinates to plot.
"""

# author:   'Marcel Patek'
# filename: 'plot_dip.py'
# date:      1/11/2015
# version:  '1.0'
# email:    'chemgplus@gmail.com'
# license:  'GNU-GPL3'
# usage:     plot_dip(df,'X','Y')

''' 
 * Copyright (C) 2015 Marcel Patek
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * For a copy of the GNU General Public License, 
 * see <http://www.gnu.org/licenses/>.
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from pylab import *


def plot_dip(df,X,Y):
    """ 
    Function to plot dipole vectors from a typical dipole moment processed output. Data is in dataframe df
    which is passed together with X,Y-coordinates to plot.
    
    :type pd dataframe: Pandas dataframe
    :param df, X, Y: dataframe, X,Y column headers e.g. 'newXa', 'newYa' 
    :return if -inline pylab is used, plot of the function is displayed in the notebook cell
    """
    
    '''
    Useful syntax
    headers = list(df) # list of df headers as strings
    # ['NLMO', 'Type', 'X', 'Y', 'Z', 'Tot_Dip', 'newX', 'newY', 'newXa', 'newYa']
    # values = df.columns
    # dictionary = dict(zip(headers, values))
    # XX = "{X}".format(**locals())  #-> newXa as string, no quotes
    # eval('df.' + XX) # df.newX
    '''

    x = df[X]
    y = df[Y]
    

    # Calculate total dipole
    firstX = df[X].iloc[0]
    lastX = df.tail(1)[X]
    lastX = lastX.tolist()[0]  # value only
    firstY = df[Y].iloc[0]
    lastY = df.tail(1)[Y]
    lastY = lastY.tolist()[0]
    total_dipole = np.sqrt(np.power(lastX - firstX, 2) + np.power(lastY - firstY, 2))
    total_dipole = round(total_dipole, 2)

    # Plot
    # Set rectangular plot dimensions to keep lengths proportional
    xlow = x.min()
    xhigh = x.max()
    ylow = y.min()
    yhigh = y.max()

    def lst_sort(list):
        """
        Sort list of floats by values.

        :type list: list of floats
        :param list: max and min x,y-coordinates

        :rtype: list of floats
        :return: sorted list of floats
        """
        abslist = []
        for item in list:
            abslist.append(item)
        return sorted(abslist)

    margins = lst_sort([xlow, ylow, xhigh, yhigh])

    # Now the plot code
    fig = plt.figure()  # To generate multiple distinct plots.
    plt.suptitle('Dipole Moments (D)')
    ax = []
    # set length of x,y axes
    xmin = margins[0] - 1
    xmax = margins[3] + 1
    ymin = margins[0] - 1
    ymax = margins[3] + 1
    plt.ylabel('Y')
    plt.xlabel('X')
    plt.grid(True)
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    color = 'blue'
    plt.scatter(x, y, s=80, c=color, label='NLMOs')
    for j, txt in enumerate(df['NLMO']):
        plt.annotate(txt, (x[j] - 0.1, y[j] + 0.2))
    ax = gca()
    ax.add_patch(FancyArrowPatch((firstX, firstY), (lastX, lastY), arrowstyle='->', mutation_scale=20, color='red'))
    for k in range(1, len(x)):
        ax.add_patch(
            FancyArrowPatch((x[k], y[k]), (x[k - 1], y[k - 1]), arrowstyle='<-', mutation_scale=20, color='blue'))

    plt.annotate(total_dipole,
                 xy=((firstX - lastX) / 2 * 0.9, (firstY - lastY) / 2 * 0.7),
                 color='red',
                 xycoords='data',
                 textcoords='offset points')
