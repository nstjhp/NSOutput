#!/usr/bin/env python
import numpy as np

class Marginals(object):
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
            self.lower_bounds = np.array(Marginals.getbounds(self,"lower"))
        if upper_bounds != None:
            self.upper_bounds = np.array(upper_bounds)
        else:
            self.upper_bounds = np.array(Marginals.getbounds(self,"upper"))
        pass
    # def getbounds(self,direction):
    #     for i in np.shape(self.parameters)[1]:
    #         if direction==lower:
    #             bounds[i] = np.floor(np.amin(self.parameters[:, i]))
    #         elif direction==upper:
    #             bounds[i] = np.ceil(np.amax(self.parameters[:, i]))
    #         else:
    #           raise ValueError("Bounds must either be upper or lower!")
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

    def getbinwidths(self):
        binwidths = (self.upper_bounds - self.lower_bounds)/ \
                   np.array([float(i) for i in self.bins])
        return binwidths

    def fillbins(self):
        # binheights = np.array([None]*self.numParams*np.max(self.bins), 
        #            dtype=np.float64).reshape((np.max(self.bins),self.numParams))
        binheights = np.zeros((np.max(self.bins),self.numParams))
        for i in range(self.numParams):
            binwidth = Marginals.getbinwidths(self)[i]
            for j in range(self.bins[i]):
                in_bin = (((self.lower_bounds[i] + j*binwidth) <=  
                         self.parameters[:,i]) & (self.parameters[:,i] < 
                         (self.lower_bounds[i] + (j+1)*binwidth)))
                bin_sum = np.sum(self.logweights[in_bin])
                binheights[j][i] = bin_sum
        #print "mysum",np.nansum(binheights)
        return binheights
   
    def getmean(self):
        mean = {"Parameter-%s" % i:np.sum(self.logweights*self.parameters[:,i])
                                        for i in range(self.numParams)}
        return mean

    def getSD(self):
        # Need to check that mean dict exists
        SD = {"Parameter-%s" % i:np.sqrt(np.sum(self.logweights * \
             self.parameters[:,i]**2) - Marginals.getmean(self)["Parameter-%s"% 
                i]**2) for i in range(self.numParams)}
        return SD

    def print_marginals(self):
        for parameter in range(np.shape(Marginals.fillbins(self))[1]):
            for index, probability in enumerate(Marginals.fillbins(self)):
                print("{:g}\t{:g}\tParam{:d}".format(self.lower_bounds[
                      parameter] + Marginals.getbinwidths(self)[parameter]*(
                      index + 0.5), probability[parameter]/
                      Marginals.getbinwidths(self)[parameter], parameter))
        return  

    # def __str__(self):
    #     this_is_wrong = []
    #     for parameter in range(np.shape(Marginals.fillbins(self))[1]):
    #         for index, probability in enumerate(Marginals.fillbins(self)):
    #           thing = "{:g}\t{:g}\tParam{:d}".format(self.lower_bounds[parameter] + Marginals.getbinwidths(self)[parameter]*(index + 0.5), probability[parameter], parameter)
    #           this_is_wrong.append(thing)
    #     return this_is_wrong


if __name__=="__main__":
    records = np.loadtxt("REP.txt")
    nickneeds =  Marginals(records, [320, 120, 100, 100, 100, 100, 100], 
                 [0,100,0,0,0,0,0], [4,160,50,50,50,50,50])

    nickneeds.print_marginals()



# for parameter in range(np.shape(nickneeds.fillbins())[1]):
#     for index, probability in enumerate(nickneeds.fillbins()):
#         print "{:g}\t{:g}\tParam{:d}".format(nickneeds.lower_bounds[parameter] +
#               nickneeds.getbinwidths()[parameter]*(index + 0.5
#               ), probability[parameter], parameter)


#np.savetxt("tempTEst.txt", nickneeds.print_marginals())

# for qq in range(np.shape(wotiwant)[1]):
#     for z in range(np.shape(wotiwant)[0]):
#       print '%f' % (wotiwant[z][qq]),z,qq# printing lists in python/from ipython without []


# mmm50 = Marginals(records,[50]*7,[0]*7,[150]*7)
# mmm25 = Marginals(records,[25]*7,[0]*7,[150]*7)
# dunno = Marginals(records,[100, 40, 20, 20, 20, 20, 20], [0]*7, 
#                         [100,1000,50,50,50,50,50])
# blab = Marginals(records,[100,40,20,20,20,20,20])

# margs = (mmm25, mmm50, dunno, blab, nickneeds)

# for marg in margs:
#     sth = marg.getbinwidths()
#     print sth
# for marg in margs:
#     sth = marg.fillbins()
#     print sth
