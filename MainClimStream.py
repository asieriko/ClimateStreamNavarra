#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 10:56:54 2023

@author: asier urio-larrea
"""
from pathlib import Path
import numpy as np
from sklearn import preprocessing
from TSF_DBSCAN import TSF_DBSCAN, p_object
from plots import plot


def main():
    currentPath = Path.cwd()
    dataset = "summer_data.csv"
    filePath = currentPath / "dataset_temp" / dataset
    T = 7000
    R = 10

    data = np.loadtxt(filePath, delimiter=";", skiprows=1)
    scaler = preprocessing.MinMaxScaler(feature_range = (0,1))
    scaled_data = scaler.fit_transform(data)

    tsf = TSF_DBSCAN(0.10, 0.30, 0.0015, 0.3, 1, T)
    for j in range(R):
        for i, p in enumerate(scaled_data[:(j + 1) * T]):
            point = p_object(p.tolist(), t=i)
            tsf.tsfdbscan(point)
        print(f"{len(tsf.clusters)} Clusters found. ({j}/{R})")
        
        results = np.array([x.x + list(x.get_max_cluster_membership()) for x in tsf.plist])
        X = results[:, :3]  # temp+Coordinates
        X = scaler.inverse_transform(X)[:, 1:3] # invert scaled data
        C = results[:, -2]  # Cluster
        M = results[:, -1]  # Membership

        np.savetxt(f"stream_{j}.csv",results,delimiter=";")

        if len(X[0]) == 2:  # Plot only 2D datasets
            outliers = (C == -1)
            plot(X, C, M, outliers, title=f"TSF-DBSCAN {(j+1)*T}")


if __name__ == "__main__":
    main()
