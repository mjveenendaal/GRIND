import numpy as np
from scipy import spatial
import laspy as las
import time

class Timer:
  def __init__(self):
    self.start = time.time()

  def restart(self):
    self.start = time.time()

  def get(self):
    end = time.time()
    m, s = divmod(end - self.start, 60)
    h, m = divmod(m, 60)
    time_str = "%02d:%02d:%02d" % (h, m, s)
    return time_str


def importances(infile):
    # Start the timer
#    timer = Timer()

    # Read the input file, init output file
#    infile = las.file.File("/media/sf_vision/data/AHN2_Clipped.las")
#    outfile = las.file.File("output.las", mode = "w", header = infile.header)
    
    # Add importance dimension to the output file
#    outfile.define_new_dimension(name = "imp",
#                        data_type = 9, description = "Importance value")

    # Copy XYZ input data to output file
#    for dimension in infile.point_format:
#        dat = infile.reader.get_dimension(dimension.name)
#        outfile.writer.set_dimension(dimension.name, dat)

    dataset = np.vstack([infile.X, infile.Y, infile.Z]).transpose()
    tree = spatial.cKDTree(dataset)
    
    r = 100.0
    importance = {}
    for point in range(len(infile)):
        if point % 1000 == 0:
            print(point)
        if point not in importance.keys():
            n = tree.query_ball_point(dataset[point,], r)
            imp = np.random.exponential(0.5,len(n))
            for i in range(len(n)):
                importance[n[i]] = imp[i]

#    outfile.imp = np.array(importance.values())

#    print("Time elapsed: %s" % timer.get() )
#    outfile.close()
    print importance
    infile.close()


#if __name__ == "__main__":
#    main()
