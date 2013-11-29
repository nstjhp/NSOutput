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

