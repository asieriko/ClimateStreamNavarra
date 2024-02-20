#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 16:31:54 2024

@author: asier urio-larrea
"""
import matplotlib.pyplot as plt
import json
import numpy as np


def nav_contour():
    # Load contour coordinates
    with open("dataset_temp/navarra2.geojson") as json_file:
        json_data = json.load(json_file)
    coordinates_nav = json_data["features"][0]["geometry"]["coordinates"][0][0]
    xc = [i for i,j in coordinates_nav]
    yc = [j/10 for i,j in coordinates_nav]
    
    return xc, yc


def plot(X, C, M, outliers=[], ranges=None, title="title"):
    if any(outliers):
        Xo = X[outliers]

        notoutliers = np.logical_not(outliers)
        Xc = X[notoutliers]
        Mc = M[notoutliers]
        Cc = C[notoutliers]
    else:
        Xc = X
        Mc = M
        Cc = C

    uC = [c for c in np.unique(Cc)]

    for i in range(len(np.unique(uC))):
        Cc[np.where(Cc == uC[i])] = i

    cmap = plt.get_cmap("tab20b", int(np.max(C)) - int(np.min(C)) + 1)
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.gca()
    
    xc, yc = nav_contour()
    ax.plot(xc,yc)
    
    if any(outliers):
        ax.scatter(Xo[:, 0], Xo[:, 1], marker='x')
    if len(Xc > 0):
        ax.scatter(Xc[:, 0], Xc[:, 1], c=Cc, cmap=cmap, alpha=Mc)  # alpha=M  # for fuzzy borders

    ax.set_title(title)
    plt.axis('off')

    fig.savefig(f'output/{title}.png')   # save the figure to file
    plt.close(fig)    # close the figure window
