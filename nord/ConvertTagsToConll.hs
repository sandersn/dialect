module ConvertTagsToConll where
import Data.List (intercalate, isPrefixOf)
import Util (withFileLines, (&), groupBy, interactTargets)
tag line = head line /= '%'
sentenceEnd line = ".\t\t" `isPrefixOf` line
convertPos (format,joiner) =
  filter tag & groupBy sentenceEnd
  & map (zipWith addColumns [1..]) & joiner
  where addColumns i = words & format i & intercalate "\t"
conllise i (w:pos:_) = [show i, w, "_", pos, pos, "_", "0", "ROOT", "_", "_"]
colise _ (w:pos:_) =  [w, pos, "_"]
main = interactTargets [("malt", (conllise,intercalate [""])),
                        ("berkeley",(colise,concatMap (++[""])))]
                       (withFileLines . convertPos)
