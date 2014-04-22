library(ggplot2)
library(grid)
library(gridExtra)
library(scales)

aa = read.table("REP_6_post1Dhist.ct2")

# Both these ribbon and density calls do the same thing, I think because underlying them is geom_area

ggplot(aa, aes(x=aa$V1)) + geom_ribbon(aes(ymin=0,ymax=aa$V2), colour="red") + geom_density(aes(y=aa$V2), stat="identity", colour="hotpink")
ggplot(aa, aes(x=aa$V1)) + geom_ribbon(aes(ymin=0,ymax=aa$V2), colour="red")

aa = read.table("tempTEst.txt")

ggplot(aa, aes(x=aa$V1)) + geom_ribbon(aes(ymin=0,ymax=aa$V2, fill=aa$V3), colour="blue") + facet_wrap(~V3, scales="free", ncol=3)
ggplot(aa, aes(x=aa$V1)) + geom_ribbon(aes(ymin=0,ymax=aa$V2), fill="blue",  alpha=0.2, colour="blue") + facet_wrap(~V3, scales="free", ncol=4)


p1a = aa$V1[aa$V3=="Param0"]
p1b = aa$V2[aa$V3=="Param0"]
p1 = cbind(p1a, p1b)
p1 = as.data.frame(p1)
ggplot(p1, aes(x=p1a, y=p1b)) + geom_ribbon(aes(ymin=0,ymax=p1b),colour="blue", fill="blue", alpha=0.2) + xlim(c(1.5,2.5))

aa = read.table("tempTEst.txt")
p1a = aa$V1[aa$V3=="Param1"]
p1b = aa$V2[aa$V3=="Param1"]
p1 = cbind(p1a, p1b)
p1 = as.data.frame(p1)
ggplot(p1, aes(x=p1a, y=p1b)) + geom_ribbon(aes(ymin=0,ymax=p1b),colour="blue", fill="blue", alpha=0.2) + xlim(c(100,150))

## For plotting joints
## As per it's really hacky
## R> dput(df)
structure(list(vecA = c(0.167362654993226, 0.225819529485782, 
0.0773662728116903, 0.0238242385679533, 0.138965253102407, 0.0355335813814452, 
0.146904411360499, 0.0506477758378961, 0.0265850316841067, 0.106991250774995
), vecB = c(0.226168654967268, 0.534681712305387, 1.20534905719588, 
-0.0312841695274512, 1.19374068716764, 1.13104396036684, 0.287244487352915, 
0.650481543113057, 1.75822808330582, 1.26039031285944), vecC = c(0.37699260096997, 
0.797612932743505, 0.0619937106966972, 0.0616321787238121, 0.800629780627787, 
0.675661528948694, 0.422923491802067, 0.467219463549554, 0.756222094874829, 
0.0248561124317348), vecD = c(0.57005580724217, 0.214912765426561, 
0.45664605172351, 0.724594541126862, 0.0836113393306732, 0.471895433263853, 
0.443401863332838, 0.228204850805923, 0.839709364110604, 0.940784497419372
), vecE = c(0.1930632062722, 0.582700167316943, 0.394652341026813, 
0.66296236240305, 0.717018441297114, 0.203766095684841, 0.0204783715307713, 
0.239014612743631, 0.0834872692357749, 0.915928384987637)), .Names = c("vecA", 
"vecB", "vecC", "vecD", "vecE"), row.names = c(NA, -10L), class = "data.frame")
jj = read.table("joints.txt", header=FALSE)
## Add columns of heights and widths for tiles otherwise just get strips
## I guess have to do this by hand all the time :-(
jj$ww = 0.1
jj$hh = rep(c(0.1,0.2),times=c(100,200))
p0 = ggplot(jj)
p1 = p0 + geom_tile(data=jj, aes(x=V1, y=V2,fill=V3,height=jj$hh, width=jj$ww))
## rows ~ columns
p2 = p1 + facet_grid(V5~V4, scales="free")
## Add the points from the data set. Obvs only 1/3 of these points will be correct per facet. 
p3 = p2 + geom_point(data=df, aes(x=vecC, y=vecD), size=4, colour="hotpink") + geom_point(data=df, aes(x=vecC, y=vecE), size=4, colour="yellow") + geom_point(data=df, aes(x=vecD, y=vecE), size=4, colour="green") 
## Have to constrict to known values of parameters. This is due to a fault with the Python class always printing more bins than necessary.
p4 = p3 + ylim(c(0,1))
print(p4)


jointData = read.table("tjoin", header=FALSE)
colnames(jointData) = c("X","Y","Z", "Xname", "Yname", "width", "height")

## tableMeanMax = read.table("lvMeanAndMax4ggplot.txt", header=TRUE)

cole= c("#272822","#880088","#FF3333","#FFEE00", "#FFFFDD")

plotFunc <- function(variable1, variable2, name1, name2) {
  jointData = jointData[jointData$Xname==paste0("Param",variable1) &
                        jointData$Yname==paste0("Param",variable2),]
  minZ = min(jointData$Z)
  maxZ = max(jointData$Z)
  diffZ = maxZ - minZ
  p0 = ggplot()
  p1 = p0 + geom_tile(data = jointData, aes(x=X, y=Y , fill = Z))
  p2 = p1 + scale_fill_gradientn(name = "Probability", colours =  cole,
    values = rescale(c(minZ, diffZ/10., diffZ/2.,  90*maxZ/100., maxZ)),
    breaks=extended_breaks(5))
  p3 = p2 + theme_nickg(9) + #theme(legend.position="none") +
      scale_y_continuous(expand=c(0,0)) + scale_x_continuous(expand=c(0,0))
  ## tmpPointMean =  geom_point(data = tableMeanMax, aes_string(x = paste0(name1,"Mean"),
  ##                 y = paste0(name2, "Mean")), shape = 21, fill = "white",
  ##   colour = NA, size = 2.5, alpha=0.8)
  ## tmpPointML =  geom_point(data = tableMeanMax, aes_string(x = paste0(name1, "ML"),
  ##                 y = paste0(name2, "ML")), shape = 23, fill = "white",
  ##   colour = NA, size = 2.5, alpha=0.8)
  ## p4 = p3 + tmpPointMean + tmpPointML
}

plotRep01 = plotFunc(0,1,"beta","alpha") + coord_cartesian(xlim=c(0,4), ylim=c(100,160))
## print(plotRep01)

plotRep02 = plotFunc(0,2,"beta","Y1 I.C.") + coord_cartesian(xlim=c(0,4), ylim=c(0,50))
## print(plotRep02)
plotRep03 = plotFunc(0,3,"beta","Y1 I.C.") + coord_cartesian(xlim=c(0,4), ylim=c(0,50))
plotRep04 = plotFunc(0,4,"beta","Y2 I.C.") + coord_cartesian(xlim=c(0,4), ylim=c(0,50))
plotRep05 = plotFunc(0,5,"beta","Y4 I.C.") + coord_cartesian(xlim=c(0,4), ylim=c(0,50))
plotRep06 = plotFunc(0,6,"beta","Y5 I.C.") + coord_cartesian(xlim=c(0,4), ylim=c(0,50))
bigplot <- grid.arrange(plotRep01, plotRep02, plotRep03, plotRep04, plotRep05, plotRep06, ncol=3, nrow=2)


## plotRep12 = plotFunc(1,2,"alpha","Y1 I.C.")# + coord_cartesian(xlim=c(100, 160), ylim=c(0,50))
## plotRep13 = plotFunc(1,3,"alpha","Y2 I.C.")# + coord_cartesian(xlim=c(100, 160), ylim=c(0,50))
## plotRep14 = plotFunc(1,4,"alpha","Y4 I.C.")# + coord_cartesian(xlim=c(100, 160), ylim=c(0,50))
## plotRep15 = plotFunc(1,5,"alpha","Y5 I.C.")# + coord_cartesian(xlim=c(100, 160), ylim=c(0,50))
## plotRep16 = plotFunc(1,6,"alpha","Y6 I.C.")# + coord_cartesian(xlim=c(100, 160), ylim=c(0,50))

## plotRep23 = plotFunc(2,3,"Y1 I.C.","Y2 I.C.")# + coord_cartesian(xlim=c(0, 50), ylim=c(0,50))

## plotRep24 = plotFunc(2,4,"Y1 I.C.","Y4 I.C.")# + coord_cartesian(xlim=c(0,50), ylim=c(0,50))
## plotRep25 = plotFunc(2,5,"Y1 I.C.","Y5 I.C.")# + coord_cartesian(xlim=c(0,50), ylim=c(0,50))
## plotRep26 = plotFunc(2,6,"Y1 I.C.","Y6 I.C.")# + coord_cartesian(xlim=c(0,50), ylim=c(0,50))

## #print(plotRep23)

## plotRep34 = plotFunc(3,4,"Y2 I.C.","Y4 I.C.")# + coord_cartesian(xlim=c(0,50), ylim=c(0,50))
## plotRep35 = plotFunc(3,5,"Y2 I.C.","Y5 I.C.")# + coord_cartesian(xlim=c(0,50), ylim=c(0,50))
## plotRep36 = plotFunc(3,6,"Y2 I.C.","Y6 I.C.")# + coord_cartesian(xlim=c(0,50), ylim=c(0,50))
                           
## plotRep45 = plotFunc(4,5,"Y4 I.C.","Y5 I.C.")# + coord_cartesian(xlim=c(0,50), ylim=c(0,50))
## plotRep46 = plotFunc(4,6,"Y4 I.C.","Y6 I.C.")# + coord_cartesian(xlim=c(0,50), ylim=c(0,50))
                           
## plotRep56 = plotFunc(5,6,"Y5 I.C.","Y6 I.C.")# + coord_cartesian(xlim=c(0,50), ylim=c(0,50))

bigplot <- grid.arrange(plotRep01, plotRep02, plotRep03, plotRep04, plotRep05, plotRep06, ncol=3, nrow=2)
## ##ggsave("RepJointsGrid2.pdf",
##    arrangeGrob(plotRep23, plotRep24, plotRep25, plotRep26, plotRep27, plotRep28,
##               plotRep34, plotRep35, plotRep36, plotRep37, plotRep38,
##               plotRep45, plotRep46, plotRep47, plotRep48,
##              plotRep56, plotRep57, plotRep58,
##              plotRep67,plotRep68,
##               plotRep78,           
##                 nrow = 7, ncol=3), width= 7.5, height=10)


## Lydia
aa = read.table("lydia.marginals")
ggplot(aa, aes(x=aa$V1)) + geom_ribbon(aes(ymin=0,ymax=aa$V2), fill="blue",  alpha=0.2, colour="blue") + facet_wrap(~V3, scales="free", ncol=2)

jointData = read.table("lydia.joints")
colnames(jointData) = c("X","Y","Z", "Xname", "Yname", "width", "height")

plotRep01 = plotFunc(0,1,"beta","alpha") 
plotRep02 = plotFunc(0,2,"beta","Y1 I.C.")
plotRep03 = plotFunc(0,3,"beta","Y1 I.C.") 
plotRep12 = plotFunc(1,2,"alpha","Y1 I.C.")
plotRep13 = plotFunc(1,3,"alpha","Y2 I.C.")
plotRep23 = plotFunc(2,3,"Y1 I.C.","Y2 I.C.")
bigplot <- arrangeGrob(plotRep01, plotRep02, plotRep03,
                       plotRep12, plotRep13 ,plotRep23, ncol=3)
print(bigplot)
