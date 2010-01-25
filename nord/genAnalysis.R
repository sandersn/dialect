# TODO: ops this does not get correlations or significances with
# the other distances, just with geo. Boo...
# TODO: how to specify size and filename for plclust? I don't want
# to enter 33 filenames

source('/Users/zackman/Documents/dialect/montecarlo Mantel example.R')

geo <- read.table("/Users/zackman/Documents/dialect/nord/dist-10-1000-geo-interview-R.txt", header=TRUE)

for (measure in c('r', 'r_sq', 'kl', 'js')) {
  for(feature in c('path', 'trigram', 'dep', 'unigram', 'retrigram', 'redep', 'deparc')) {
    cat(paste(" OK: ", measure, feature, "\n"))
    t <- read.table(paste("/Users/zackman/Documents/dialect/nord/dist-10-1000", measure, feature, "interview-R.txt", sep='-'), header=TRUE)
    # plclust(hclust(as.dist(t), method="ward"), hang=-1, sub="", xlab="", ylab=paste(measure, feature, sep='-'))
    cat(paste("cor:", cor(vectorise(geo), vectorise(t)), '\n'))
    cat(paste("sig:", mantel(geo, t, 33), '\n'))
  }
}
