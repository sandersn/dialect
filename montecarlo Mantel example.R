permute <- function (a, rowsize) {
	temp <- sample(rowsize)
	a[temp,temp]
}
vectorise <- function(a) a[lower.tri(a,diag=FALSE)]
mantel <- function (a, b, rowsize) mantelVec(a, vectorise(b), rowsize)
mantelVec <- function (a, Bvector, rowsize) {
	numpermutes <- 1000
	obs.corr <- cor(vectorise(a), Bvector)
	permuted.corr <- rep(0,numpermutes)
	permuted.corr[1] <- obs.corr
	for (i in 2:numpermutes)
	{
		permuted.corr[i] <- cor(vectorise(permute(a,rowsize)), Bvector)
	}
	sum(permuted.corr>=obs.corr)/numpermutes
}
# now do:
##pearsonsR <- cor(vectorise(sed), vectorise(ice))
#mantelSignificance <- mantel(sed, ice, 9)
## here is how to permute an array
## Oleg Kiselyov told me never to do it this way
#A<-matrix(c(11,12,13,12,22,23,13,23,33),byrow=T,nrow=3)
#temp<-sample(3)
#temp
#Aperm<-A[temp,temp]
#Aperm
## here are some realer numbers. still a 3x3 array
#A<-matrix(c(0,.56,.61,.56,0,.21,.61,.21,0),byrow=T,nrow=3)
#B<-matrix(c(0,.83,.80,.83,0,.43,.80,.43,0),byrow=T,nrow=3)
#A
#B
## this is what I WAS doing. It is wrong apparently.
#Avector <-as.vector(A[lower.tri(A,diag=FALSE)])
#Avector
#Bvector <-as.vector(B[lower.tri(B,diag=FALSE)])
#Bvector
#obs.corr <-cor(Avector,Bvector)
#obs.corr
## remember how to permute an array? Here it is again in case you #forgot
#temp<-sample(3)
#temp
#Aperm<-A[temp,temp]
#Aperm
## correlate the permutation of A with B
#Avectorp <-as.vector(Aperm[lower.tri(Aperm,diag=FALSE)])
#Avectorp
#pcorr <-cor(Avectorp,Bvector)
#pcorr
## now do this 1000 times ok
##numpermutes <-500
##  temp <-sample(3)
##  Aperm<-A[temp,temp]
##  Avectorp <-as.vector(Aperm[lower.tri(Aperm,diag=FALSE)])
##  permuted.corr[i]<-cor(Avectorp,Bvector)
#	#permuted.corr
#	#pvalue<-
#	#pvalue
#
## not sure what this is, I guess the standard multi-regression #analysis
#reg<-lm(Bvector~Avector)
#coef(reg)

