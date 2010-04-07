setwd('/Users/zackman/Documents/dialect/')
source('montecarlo Mantel example.R')
sink('nord/correlations-R.txt')

geo <- read.table("nord/dist-geo-R.txt", header=TRUE)
travel <- read.table("nord/dist-travel-R.txt", header=TRUE)
measures <- c('r', 'r_sq', 'kl', 'js', 'cos')
features <- c('path', 'trigram', 'dep', 'psg', 'grand',
              'unigram',
              'redep', 'deparc',
              'all')
samples <- c('1000', 'full')
norms <- c('ratio', 'freq')
for (norm in norms) {
  for (sample in samples) {
    for (measure in measures) {
      ts <- list()
      for(feature in features) {
        cat(paste(" OK: ", sample, measure, feature, norm, "\n"))
        t <- read.table(paste("nord/dist-10",
                              sample, measure, feature, norm, "R.txt", sep='-'),
                        header=TRUE)
        ts <- c(ts, list(t))
        hcl <- hclust(as.dist(t), method="ward")
        cat(paste("Cluster: "))
        cat(paste(sample, measure, feature, norm, sep=' '))
        cat(' ')
        for(i in hcl$merge) {
          cat(i); cat(" ")
        }
        cat("\n")
        pdf(file=paste("dist-10",
                       sample, measure, feature, norm,
                       "clusterward.pdf", sep='-'),
            width=9.014, height=6.931)
        plclust(hcl, hang=-1, sub="",
                xlab="", ylab=paste(sample, measure, feature, norm, sep='-'))
        dev.off()
        cat(paste("cor:", cor(vectorise(geo), vectorise(t)), '\n'))
        # cat(paste("sig:", mantel(geo, t, 33), '\n'))
        cat(paste("sig:", mantel(geo, t, 30), '\n'))
        cat(paste("cortravel:", cor(vectorise(travel), vectorise(t)), '\n'))
        cat(paste("sigtravel:", mantel(travel, t, 30), '\n'))
      }
 # I don't know R's zip, so I will just use indexing even if it is slow
 # which it's not, R's lists are actually untyped vectors not conses
 # I also don't know how R represents pairs, so I won't write a separate function
      for(i in 1:(length(ts)-1)) {
        for(j in (i+1):length(ts)) {
          cat(paste(cor(vectorise(ts[[i]]), vectorise(ts[[j]])), '(',
                  # mantel(ts[[i]], ts[[j]], 33), '),', sep=''))
                    mantel(ts[[i]], ts[[j]], 30), '),', sep=''))
        }
        cat('\n')
      }
    }
  }
}

sink()
