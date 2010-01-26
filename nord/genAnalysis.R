# TODO: oops this does not get correlations or significances with
# the other distances, just with geo. Boo...

setwd('/Users/zackman/Documents/dialect/')
source('montecarlo Mantel example.R')
sink('nord/dist-10-1000-correlations-interview-R.txt')

geo <- read.table("nord/dist-10-1000-geo-interview-R.txt", header=TRUE)

for (measure in c('r', 'r_sq', 'kl', 'js')) {
  for(feature in c('path', 'trigram', 'dep',
                   'unigram', 'retrigram', 'redep', 'deparc')) {
    cat(paste(" OK: ", measure, feature, "\n"))
    t <- read.table(paste("nord/dist-10-1000",
                          measure, feature, "interview-R.txt", sep='-'),
                    header=TRUE)
    pdf(file=paste("dist-10-1000", measure, feature, "clusterward.pdf", sep='-'),
        width=9.014, height=6.931)
    plclust(hclust(as.dist(t), method="ward"),
            hang=-1, sub="", xlab="", ylab=paste(measure, feature, sep='-'))
    dev.off()
    cat(paste("cor:", cor(vectorise(geo), vectorise(t)), '\n'))
    cat(paste("sig:", mantel(geo, t, 33), '\n'))
  }
}

sink()
