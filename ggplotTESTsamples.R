library(ggplot2)
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
