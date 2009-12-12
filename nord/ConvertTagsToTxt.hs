import System (getArgs)
import Data.List (intercalate, isPrefixOf)
import Util (withFileLines, (&), groupBy)
tag line = line !! 0 /= '%'
sentenceEnd line = line `isPrefixOf` ".\t\t"
readPos = withFileLines
  (filter tag & groupBy sentenceEnd & map putTagsOnOneLine & intercalate "\n")
putTagsOnOneLine = map (words & (!!1)) & intercalate " "
main = System.getArgs >>= head & readPos >>= putStr
