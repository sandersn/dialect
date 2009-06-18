import System (getArgs)
import Data.List (intercalate, isPrefixOf)
import Data.List.Split (split, dropFinalBlank, keepDelimsR, whenElt)
import Util (withFile, withFileLines, (&))
tag line = line !! 0 /= '%'
group = split $ dropFinalBlank $ keepDelimsR $ whenElt (".\t\t" `isPrefixOf`)
readPos = flip withFileLines
    (filter tag & group & map putTagsOnOneLine & intercalate "\n")
putTagsOnOneLine = map (words & (!!1)) & intercalate " "
main = System.getArgs >>= head & readPos >>= putStr
