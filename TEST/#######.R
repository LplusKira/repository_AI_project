#######
# HW7 #
#######

#########################
# Examples of hand outs #
# Normal distribution   #
#########################

set.seed(100)

n<-20
alpha <- .05
mu0 <- 500
sigma <- 100
m <- 10000        # number of replicates
p <- numeric(m)   # storages for p-value

for(j in 1:m){
	#number of replicates
	#storage for p-values
	x <- rnorm(n, mu0, sigma)
	ttest <- t.test(x, alternative = "greater", mu = mu0)
	p[j] <- ttest$p.value
}

p.hat <- mean(p < alpha)
se.hat <- sqrt(p.hat * (1 - p.hat) / m)
print(c(p.hat, se.hat))

# Type I Error 0.05280000
# Standard Error 0.00223634


#################################
# Chi-square distribution  df=1 #
#################################

set.seed(100)

mu0 <- 1

for(j in 1:m){
	#number of replicates
	#storage for p-values
	x <- rchisq(n, df = 1)
	ttest <- t.test(x, alternative = "greater", mu = mu0)
	p[j] <- ttest$p.value
}

p.hat <- mean(p < alpha)
se.hat <- sqrt(p.hat * (1 - p.hat) / m)
print(c(p.hat, se.hat))

# Type I Error 0.012200000
# Standard Error 0.001097778
# Type I error rate of the t-test is different from the nominal significance level α
 

#############################
# Uniform(0,2) distribution #
#############################

set.seed(100)

mu0 <- 1

for(j in 1:m){
	#number of replicates
	#storage for p-values
	x <- runif(n, min=0, max=2)
	ttest <- t.test(x, alternative = "greater", mu = mu0)
	p[j] <- ttest$p.value
}

p.hat <- mean(p < alpha)
se.hat <- sqrt(p.hat * (1 - p.hat) / m)
print(c(p.hat, se.hat))

# Type I Error 0.049700000
# Standard Error 0.002173244
# Type I error rate of the t-test is approximately equal to the nominal significance level α

####################################
#  Exponential(λ = 1) distribution #
####################################

set.seed(100)

mu0 <- 1

for(j in 1:m){
	#number of replicates
	#storage for p-values
	x <- rexp(n, rate = 1)
	ttest <- t.test(x, alternative = "greater", mu = mu0)
	p[j] <- ttest$p.value
}

p.hat <- mean(p < alpha)
se.hat <- sqrt(p.hat * (1 - p.hat) / m)
print(c(p.hat, se.hat))

# Type I Error 0.019500000
# Standard Error 0.001382742
# Type I error rate of the t-test is different from the nominal significance level α



# Conclusion
# Only Uniform(0,2) distribution holds the same property between
# Type I error and significance level α like normal distribution does