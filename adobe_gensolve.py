# -*- coding: utf-8 -*-
"""adobe_gensolve.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lnfxqBOAqmXqAVEEiQOBVyvvJQTG5rjW
"""



import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance

def read_csv(csv_path):
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
    path_XYs = []
    for i in np.unique(np_path_XYs[:, 0]):
        npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
        XYs = []
        for j in np.unique(npXYs[:, 0]):
            XY = npXYs[npXYs[:, 0] == j][:, 1:]
            XYs.append(XY)
        path_XYs.append(XYs)
    return path_XYs

def plot(paths_XYs):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    colours = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    for i, XYs in enumerate(paths_XYs):
        c = colours[i % len(colours)]
        for XY in XYs:
            ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)
    ax.set_aspect('equal')
    plt.show()

# Example usage
paths_XYs = read_csv('frag0.csv')
plot(paths_XYs)






def is_straight_line(XY, tolerance=1e-2):
    if len(XY) < 2:
        return False
    dists = distance.pdist(XY)
    return np.all(np.abs(dists - dists[0]) < tolerance)

def is_circle(XY, tolerance=1e-2):
    if len(XY) < 3:
        return False
    center = np.mean(XY, axis=0)
    radii = np.linalg.norm(XY - center, axis=1)
    return np.all(np.abs(radii - radii[0]) < tolerance)

def is_ellipse(XY, tolerance=1e-2):
    # Simplified check for ellipses using covariance
    if len(XY) < 5:
        return False
    cov = np.cov(XY.T)
    eigenvalues, _ = np.linalg.eigh(cov)
    return np.all(eigenvalues > tolerance)

def is_rectangle(XY, tolerance=1e-2):
    if len(XY) != 4:
        return False
    dists = distance.pdist(XY)
    dists.sort()
    return np.all(np.abs(dists[0] - dists[1]) < tolerance) and \
           np.all(np.abs(dists[2] - dists[3]) < tolerance)

def identify_shapes(paths_XYs):
    shapes = {'lines': [], 'circles': [], 'ellipses': [], 'rectangles': []}
    for XYs in paths_XYs:
        for XY in XYs:
            if is_straight_line(XY):
                shapes['lines'].append(XY)
            elif is_circle(XY):
                shapes['circles'].append(XY)
            elif is_ellipse(XY):
                shapes['ellipses'].append(XY)
            elif is_rectangle(XY):
                shapes['rectangles'].append(XY)
    return shapes

def print_identified_shapes(shapes):
    for shape_type, shape_list in shapes.items():
        print(f"{shape_type.capitalize()}: {len(shape_list)} identified")

shapes = identify_shapes(paths_XYs)
print_identified_shapes(shapes)