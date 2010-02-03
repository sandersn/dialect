module ConvertTntToTxt where
import Util (withFileLines, (&), groupBy, interactFiles)
import Data.List.Split (split, keepDelimsR, onSublist, dropFinalBlank)
main = interactFiles (withFileLines convertWord) id
convertWord = split (keepDelimsR $ dropFinalBlank $ onSublist ["."])
              & map unwords
