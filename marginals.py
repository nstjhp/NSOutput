#!/usr/bin/env python
import numpy as np

class marginals(object):
    def __init__(self, data, bins, lower_bounds=None, upper_bounds=None):
        self.logweights = data[:,0]
        self.chisq = data[:,1]
        self.parameters = data[:,2:]
        self.bins = bins
	self.numParams = np.shape(self.parameters)[1]
        # should try except here if np.shape(bounds)[0]==self.numParams
	# i.e. check that passed bounds lists are the same size as num of params
    	if lower_bounds != None:
            self.lower_bounds = np.array(lower_bounds)
        else:
            self.lower_bounds = np.array(marginals.getbounds(self,"lower"))
    	if upper_bounds != None:
	    self.upper_bounds = np.array(upper_bounds)
        else:
            self.upper_bounds = np.array(marginals.getbounds(self,"upper"))
        pass
    # def getbounds(self,direction):
    #     for i in np.shape(self.parameters)[1]:
    #         if direction==lower:
    #             bounds[i] = np.floor(np.amin(self.parameters[:, i]))
    #         elif direction==upper:
    #             bounds[i] = np.ceil(np.amax(self.parameters[:, i]))
    #         else:
    #     	raise ValueError("Bounds must either be upper or lower!")
    #     return bounds
    def getbounds(self,direction):
        bounds = np.array([None]*self.numParams, dtype=np.float64)
        if direction=="lower":
	    for i in range(self.numParams):
                bounds[i] = np.floor(np.amin(self.parameters[:, i]))
        elif direction=="upper":
	    for i in range(self.numParams):
                bounds[i] = np.ceil(np.amax(self.parameters[:, i]))
        else:
	    raise ValueError("Bounds must either be 'upper' or 'lower'!")
        return bounds

    def getbinsizes(self):
        binsizes = (self.upper_bounds - self.lower_bounds)/ \
		   np.array([float(i) for i in self.bins])
        return binsizes

    def fillbins(self):
	binheights = np.array([None]*self.numParams*np.max(self.bins), dtype=np.float64).reshape((np.max(self.bins),self.numParams))
	for i in range(self.numParams):
            binwidth = marginals.getbinsizes(self)[i]
            for j in range(self.bins[i]):
                in_bin = (((self.lower_bounds[i] + j*binwidth) <=  self.parameters[:,i]) & (self.parameters[:,i] < (self.lower_bounds[i] + (j+1)*binwidth)))
        	bin_sum = np.sum(self.logweights[in_bin])
        	binheights[j][i] = bin_sum
        return binheights
   
    def getmean(self):
	mean = {"Parameter-%s" % i:np.sum(self.logweights*self.parameters[:,i]) \
					for i in range(self.numParams)}
        return mean

    def getSD(self):
        # Need to check that mean dict exists
        SD = {"Parameter-%s" % i:np.sqrt(np.sum(self.logweights * \
             self.parameters[:,i]**2) - marginals.getmean(self)["Parameter-%s"% i]**2) \
	     for i in range(self.numParams)}
        return SD


records = np.loadtxt("REP.txt")

mmm50 = marginals(records,[50]*7,[0]*7,[150]*7)
mmm25 = marginals(records,[25]*7,[0]*7,[150]*7)
dunno = marginals(records,[100,40,20,20,20,20,20],[0]*7,[100,1000,50,50,50,50,50])
blab = marginals(records,[100,40,20,20,20,20,20])

margs = (mmm25, mmm50, dunno, blab)

print marginals(records,[60,60,20,20,20,20,20],[0]*7,[6,150,50,50,50,50,50]).fillbins()

# for marg in margs:
#     sth = marg.getbinsizes()
#     print sth
# for marg in margs:
#     sth = marg.fillbins()
#     print sth
