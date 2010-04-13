import ConvertTagsToConll hiding (main)
import Util
import Data.List (intercalate)
main = interactTargets [("unigram", unigram), ("trigram", trigram)] namedProcess
  where namedProcess target name = withFileLines (convert target name) name
convert target name = filter tag & splitByR sentenceEnd
                      & map (map (words & (!!1)) & target)
                      & intercalate ["***"] & (name:)
unigram = id
trigram = window 3 & map (intercalate "-")
