import System (getArgs)
import Data.List (intercalate, isPrefixOf)
import Data.List.Split (split, dropFinalBlank, keepDelimsR, whenElt)
import Util (withFile, withFileLines, (&))
tag line = line !! 0 /= '%'
group = split $ dropFinalBlank $ keepDelimsR $ whenElt (".\t\t" `isPrefixOf`)
readPos = flip withFileLines
    (filter tag & group & map (zipWith addColumns [1..]) & intercalate ["\n"])
addColumns i = words & conllise i & intercalate "\t"
-- TODO: Add the real columns (below are guessed from Talbanken)
conllise i [w, pos] = [show i, w, "_", pos, pos, "_", "0", "ROOT", "_", "_"]
main = System.getArgs >>= head & readPos >>= mapM_ putStrLn
