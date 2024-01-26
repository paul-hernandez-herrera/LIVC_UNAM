import numpy as np

def cummulative_euclidian_distance_between_points(points):
    # we assume that coordinates of points are given in the rows
    cum_dist = np.zeros(points.shape[0],)
    cum_dist[1:] = np.cumsum(np.sqrt(np.sum(np.power(np.diff(points, axis=0),2), axis = 1)))
    
    return cum_dist


        



