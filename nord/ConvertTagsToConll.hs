import System (getArgs)
import Data.List (intercalate, isPrefixOf)
import Data.List.Split (split, dropFinalBlank, keepDelimsR, whenElt)
import Util (withFileLines, (&), groupBy)
tag line = line !! 0 /= '%'
sentenceEnd line = line `isPrefixOf` ".\t\t"
readPos = withFileLines (filter tag & groupBy sentenceEnd
                         & map (zipWith addColumns [1..]) & intercalate ["\n"])
addColumns i = words & conllise i & intercalate "\t"
conllise i [w, pos] = [show i, w, "_", pos, pos, "_", "0", "ROOT", "_", "_"]
main = System.getArgs >>= head & readPos >>= mapM_ putStrLn
