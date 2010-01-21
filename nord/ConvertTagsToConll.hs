module ConvertTagsToConll where
import Data.List (intercalate, isPrefixOf)
import Util (withFileLines, (&), groupBy, interactFiles)
tag line = head line /= '%'
sentenceEnd line = ".\t\t" `isPrefixOf` line
convertPos = filter tag & groupBy sentenceEnd
             & map (zipWith addColumns [1..]) & intercalate ["\n"]
addColumns i = words & conllise i & intercalate "\t"
conllise i [w, pos] = [show i, w, "_", pos, pos, "_", "0", "ROOT", "_", "_"]
main = interactFiles (withFileLines convertPos) id
