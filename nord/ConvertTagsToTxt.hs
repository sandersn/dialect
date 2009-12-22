import Data.List (intercalate, isPrefixOf)
import Util (withFileLines, (&), groupBy, argsFilePrinter)
import Data.List.Split (split, keepDelimsR, onSublist, dropFinalBlank)
tag line = head line /= '%'
sentenceEnd line = line `isPrefixOf` ".\t\t"
readPos = withFileLines
  (filter tag & groupBy sentenceEnd & map putTagsOnOneLine)
putTagsOnOneLine = map (words & (!!1)) & intercalate " "
main = argsFilePrinter readWords id
-- OR, input from .t: --
readWords = withFileLines
  (split (keepDelimsR $ dropFinalBlank $ onSublist ["."])
   & map (intercalate " "))
