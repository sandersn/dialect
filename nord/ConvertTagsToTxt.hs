module ConvertTagsToTxt where
import Util (withFileLines, (&), groupBy, argsFilePrinter)
import Data.List.Split (split, keepDelimsR, onSublist, dropFinalBlank)
main = argsFilePrinter (withFileLines convertWord) id
convertWord = split (keepDelimsR $ dropFinalBlank $ onSublist ["."])
              & map unwords
