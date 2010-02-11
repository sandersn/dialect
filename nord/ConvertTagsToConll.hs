module ConvertTagsToConll where
import Data.List (intercalate, isPrefixOf)
import Util (withFileLines, (&), groupBy, interactTargets)
tag line = head line /= '%'
sentenceEnd line = ".\t\t" `isPrefixOf` line
convertPos format = filter tag & groupBy sentenceEnd
                    & map (zipWith addColumns [1..]) & intercalate ["\n"]
  where addColumns i = words & format i & intercalate "\t"
conllise i column = show i : colise i column
colise _ (w:pos:_) = [w, "_", pos, pos, "_", "0", "ROOT", "_", "_"]
main = interactTargets [("malt", conllise), ("berkeley",colise)]
                       (withFileLines . convertPos)
