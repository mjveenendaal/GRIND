# Synthesis project
# MSc.Geomatics, TU Delft
# by: Tom Hemmes & MJ Veenendaal

###        Performance report          ###
  # Model Name:             MacBook Pro
  # Model Identifier:       MacBookPro11,2
  # Processor Name:         Intel Core i7
  # Processor Speed:        2,2 GHz
  # Number of Processors:   1
  # Total Number of Cores:  4
  # L2 Cache (per Core):    256 KB
  # L3 Cache:               6 MB
  # Memory:                 16 GB
### AHN2_Clipped.las ==     1.2M points
  # 80 seconds
### lidar.las ==            10.6k points
  # 0.7 seconds
###                                    ###


import numpy as np
from scipy import spatial
import laspy as las
import time


def importance(infile):
    point_count = 0 # tracking the number of points processed

#    if mode == "random":
#        # create random values in exponential distribution and merge with x,y,z data
#        outfile.imp = np.random.exponential(0.5, len(infile))
#
#    elif mode == "neighbour":
    # retrieve data from infile and put it in a nparray
    dataset = np.vstack([infile.X, infile.Y, infile.Z]).transpose()
    # create the KDTree to calculate Nearest Neighbours & Distances
    tree = spatial.cKDTree(dataset)
    # track the already calculated points using a set
    checked_points = set()
    # empty list to be populated with sublist [X,Y,Z,imp]
    output_list = []
        
    # setting initial values
    point_count = 0
    number_neighbors = 2 # number of neighbors searched per request == n_n
    i = 0
    number_distances = 1 # number of distances for average == n_a
    initial_length = len(dataset)
        
    def computeAVGdistance(arr_, tree_, i, n_n, n_a): 
        neighbours = tree_.query(arr_[i,], k = n_n)
        #print neighbours
        sum_distance = 0.0
        count_distance = 0
        avg_distance = 0.0
        #print "point"
        for i in range(1, n_n):
            if neighbours[1][i] in checked_points: # if it is already checked, skip the corresponding distance
                continue
            sum_distance += neighbours[0][i]
            count_distance += 1
            if count_distance == n_a:
                avg_distance += (sum_distance/n_a)
                sum_distance = 0
                break
        if avg_distance != 0.0:
            # if the for-loop added a value to the avg_distance, return [X,Y,Z,imp]
            try: return [arr_[i,][0], arr_[i,][1], arr_[i,][2], avg_distance]
            except: return [-9999, -9999, -9999, -9999] # error handling (to be improved...)
        return bool(False) # if not it will return False (so if all neighbours to a point are already checked)

#        process_time = time.time()

    while len(dataset)>0:
        if i == len(dataset): # important threshold for performance: when should you rebuild the KD-tree?
#            print "recomputing and rebuilding KD-Tree..."
                # the mask will be used to eliminate the used points from the array
#                tt = time.time()
            mask = np.ones(len(dataset), dtype=bool)
            for j in checked_points:
                mask[j] = False
            dataset = dataset[mask]
            tree = spatial.cKDTree(dataset)
#                print "KD-Tree rebuilt: containing "+str(len(dataset))+" points, in "+str(time.time()-tt)+" sec."
            checked_points.clear() # clear the used points list
            i = 0
        p_i = computeAVGdistance(dataset, tree, i, number_neighbors, number_distances)
        if p_i != False: # if all corresponding neighbors are already used. 
            output_list.append(p_i) # append [X,Y,Z,imp]
            checked_points.add(i)
            point_count +=1
        i +=1
#        if (point_count % 1000)==0: # progress tracker each % points
#           print str(point_count)+" points processed in "+str(time.time()-process_time)+" sec."
#        if len(output_list)==initial_length:
#            break

 #       print "algorithm process time: "+str(time.time()-process_time)+" sec."
        output_nparray = np.array(output_list)  

        # assign values to outfile
#        outfile.X, outfile.Y, outfile.Z, outfile.imp = output_nparray[:,0], output_nparray[:,1], output_nparray[:,2], output_nparray[:,3]
    
    return output_nparray[:10]

#def main():
#    start_time = time.time()
#
#    # infile = las.file.File("lidar.las")
#    infile = las.file.File("/run/AHN2_Clipped.las")
#
#    outfile = las.file.File("output_mj5.las", mode = "w", header = infile.header)
#    outfile.define_new_dimension(name = "imp", data_type = 9, description = "Importance value")
#
#    print "file contains "+str(len(infile))+" points"
#
#    outfile = importance(infile, outfile)
#
#    outfile.close()
#    infile.close()
#
#    print "total read+algorithm+analysis timer: "+str(time.time()-start_time)+" sec."
#
#if __name__ == "__main__":
#    main()
