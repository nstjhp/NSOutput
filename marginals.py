#!/usr/bin/env python
import numpy as np
from itertools import combinations as iter_combi
import sys

class Marginals(object):
    """This class calculates the marginal probability of all parameters 
    from the output of a MultiNest run of nested sampling.
    MultiNest produces a file of called [root].txt which contains 2 + num. of 
    parameters columns.
    Col 1: normalised log-probabilities
    Col 2: -2*loglikelihoods
    Col 3:n corresponding parameter sets

    This class bins the probabilities and produces output that can go
    straight into ggplot in R without faffing about! 

    TODO:
    So many things!!!
    Make a superclass called sth like NSOutput (make Marginals etc. sub-classes)
    Get the best-fit param set; def get_best_fit(self) (sub-class, use super?)
    Calculate joint probabilities too (sub-class it?)
    Documentation (ReST?)
    Put in some try/except blocks that actually work.
    See if can get the __str__ to do what I want (can't return a list)
    Ensure it's Python 3 compatible
    Discover if you can call class method without typing the classname
    Get emacs to not put tabs, just 4 space indents (avoids M-x untabify)
    Credible intervals using other MultiNest file?"""
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
	"""Find the upper and lower bounds of the parameter values if the 
	user didn't supply the ones they want to use."""
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
	"""Find the widths of each bin. Designed to allow different bin 
	widths per parameter."""
        binwidths = (self.upper_bounds - self.lower_bounds)/ \
                   np.array([float(i) for i in self.bins])
        return binwidths

    def fill_bins(self):
	"""Fill the bins with the probability weights. Does the most 
	important work!"""
        # binheights = np.array([None]*self.numParams*np.max(self.bins), 
        #            dtype=np.float64).reshape((np.max(self.bins),self.numParams))
        binheights = np.zeros((np.max(self.bins),self.numParams))
        all_binwidths = Marginals.getbinwidths(self)
        for i in range(self.numParams):
            binwidth = all_binwidths[i]
            for j in range(self.bins[i]):
                in_bin = (((self.lower_bounds[i] + j*binwidth) <=  
                         self.parameters[:,i]) & (self.parameters[:,i] < 
                         (self.lower_bounds[i] + (j+1)*binwidth)))
		#print(i,j,in_bin)
                bin_sum = np.sum(self.logweights[in_bin])
		#print(i,j,bin_sum)
                binheights[j][i] = bin_sum
        #print "mysum",np.nansum(binheights)
        return binheights
   
    def fill_joint_bins(self):
        """Fill the joint bins with the probability weights. Does the most 
        important work!"""
        binheights = np.zeros((np.max(self.bins), np.max(self.bins),
                               len(list(iter_combi(range(self.numParams),2)))))
        all_binwidths = Marginals.getbinwidths(self)
        all_pairs = list(iter_combi(range(self.numParams),2))
        in_bin = np.zeros([np.max(self.bins), len(self.logweights)], dtype=bool)
        #in_bin = np.zeros([np.max(self.bins), np.max(self.bins)], dtype=bool)
        bin_sum = np.zeros([np.max(self.bins), np.max(self.bins)])
        #print(in_bin)
        for pair_index, pair in enumerate(all_pairs):
            binwidthX = all_binwidths[pair[0]]
            binwidthY = all_binwidths[pair[1]]
            for indX in range(self.bins[pair[0]]):
                for indY in range(self.bins[pair[1]]):
                    #print pair, indX, indY
                    in_bin[indX][:] = ((((self.lower_bounds[pair[0]] + indX*binwidthX) <= self.parameters[:,pair[0]]) & \
                                           (self.parameters[:,pair[0]] < (self.lower_bounds[pair[0]] + (indX + 1)*binwidthX))) &\
                                          (((self.lower_bounds[pair[1]] + indY*binwidthY) <= self.parameters[:,pair[1]]) & \
                                           (self.parameters[:,pair[1]] < (self.lower_bounds[pair[1]] + (indY + 1)*binwidthY))))
                    #print in_bin[0][:]
                    #if indY==9: sys.exit()
                    bin_sum[indX][indY] = np.sum(self.logweights[in_bin[indX][:]])
                    #print bin_sum
                    binheights[indX][indY][pair_index] = bin_sum[indX][indY]
        return binheights

    def getmean(self):
	"""Calculates mean average of each parameter and returns a dictionary"""
        mean = {"Parameter-%s" % i:np.sum(self.logweights*self.parameters[:,i])
                                        for i in range(self.numParams)}
        return mean

    def getSD(self):
	"""Calculates the standard deviation of each parameter"""
        # Need to check that mean dict exists OR maybe not......
        SD = {"Parameter-%s" % i:np.sqrt(np.sum(self.logweights * \
             self.parameters[:,i]**2) - Marginals.getmean(self)["Parameter-%s"% 
                i]**2) for i in range(self.numParams)}
        return SD

    def print_marginals(self):
	"""Currently prints out the results in the format required.
        It's possible the binned probabilities need to be divided by their
        binwidths either in fillbins() or in a separate function. Do this to
        normalise properly (i.e. so area = 1)."""
        bin_heights = Marginals.fill_bins(self)
        bin_widths = Marginals.getbinwidths(self)
        for parameter in range(np.shape(bin_heights)[1]):
            for index, probability in enumerate(bin_heights):
                print("{:g}\t{:g}\tParam{:d}".format(self.lower_bounds[
                      parameter] + bin_widths[parameter]*(index + 0.5),
                      probability[parameter]/bin_widths[parameter], parameter))
        return  

    def print_joints(self):
	"""Currently does ??????
        It's possible the binned probabilities need to be divided by their
        binwidths either in fillbins() or in a separate function. Do this to
        normalise properly (i.e. so area = 1)."""
        bin_heights = Marginals.fill_joint_bins(self)
        bin_widths = Marginals.getbinwidths(self)
        all_pairs = list(iter_combi(range(self.numParams),2))

        for pair_index, pair in enumerate(all_pairs):
            parameterX = pair[0]
            parameterY = pair[1]
            bin_widthX = bin_widths[parameterX]
            bin_widthY = bin_widths[parameterY]
            for index, probability in enumerate(bin_heights):
                for another_index in range(len(bin_heights)):
                    #print index, another_index, probability[another_index][pair_index]
                    print("{:g}\t{:g}\t{:g}\tParam{:d}\tParam{:d}".format(self.lower_bounds[parameterX] + bin_widthX*(index + 0.5), self.lower_bounds[parameterY] + bin_widthY*(another_index + 0.5), probability[another_index][pair_index]/bin_widthX/bin_widthY, parameterX, parameterY))

        return

    # def __str__(self):
    #     this_is_wrong = []
    #     for parameter in range(np.shape(Marginals.fillbins(self))[1]):
    #         for index, probability in enumerate(Marginals.fillbins(self)):
    #           thing = "{:g}\t{:g}\tParam{:d}".format(self.lower_bounds[parameter] + Marginals.getbinwidths(self)[parameter]*(index + 0.5), probability[parameter], parameter)
    #           this_is_wrong.append(thing)
    #     return this_is_wrong


if __name__=="__main__":
    records = np.loadtxt("linearModel.txt")##REP.txt")
    nickneeds = Marginals(records,[100]*2)##,[0.,-.75],[0.3,1.])
     
    ##records = np.loadtxt("simpleData.txt")##linearModel.txt")##REP.txt")
    ##nickneeds = Marginals(records,[10]*2)##,[0.,-.75],[0.3,1.])

    ##newrecords = np.column_stack((records,abs(records[:,2] - records[:,3])))
    ##nickneeds = Marginals(newrecords,[10,10,5])

    ##records = np.loadtxt("REP.txt")
    ##nickneeds = Marginals(records, [320, 120, 100, 100, 100, 100, 100], 
    ##             [0,100,0,0,0,0,0], [6,160,50,50,50,50,50])

    #nickneeds.print_marginals()
    nickneeds.print_joints()


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


        # if lower_bounds != None:
        #     try:
        #         print "HERE", lower_bounds, self.numParams
        #         #len(lower_bounds)==self.numParams
        #         lower_bounds[self.numParams]
        #         self.lower_bounds = np.array(lower_bounds)
        #     except IndexError: print "shitthebed*******************"
        #     # except Exception as e:
        #     #     print "Feeerrucckkkk", e
