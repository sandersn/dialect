module ConvertTagsToTxt where
import Data.List (isPrefixOf)
import Util (withFileLines, (&), groupBy, argsFilePrinter)
import Data.List.Split (split, keepDelimsR, onSublist, dropFinalBlank)
tag line = head line /= '%'
sentenceEnd line = ".\t\t" `isPrefixOf` line
convertPos = filter tag & groupBy sentenceEnd & map putTagsOnOneLine
putTagsOnOneLine = map (words & (!!1)) & unwords
main = argsFilePrinter (withFileLines convertWord) id
-- OR, input from .t: --
convertWord = split (keepDelimsR $ dropFinalBlank $ onSublist ["."])
              & map unwords
