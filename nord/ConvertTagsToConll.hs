import Data.List (intercalate, isPrefixOf)
import Util (withFileLines, (&), groupBy, argsFilePrinter)
tag line = line !! 0 /= '%'
sentenceEnd line = ".\t\t" `isPrefixOf` line -- TODO: Test flipped arguments
readPos = withFileLines (filter tag & groupBy sentenceEnd
                         & map (zipWith addColumns [1..]) & intercalate ["\n"])
addColumns i = words & conllise i & intercalate "\t"
conllise i [w, pos] = [show i, w, "_", pos, pos, "_", "0", "ROOT", "_", "_"]
main = argsFilePrinter readPos id
