import System (getArgs)
import Data.List (intercalate)
import Util (withFile, withFileLines, (&))
tag line = line !! 0 /= '%'
endsentence line = line !! 0 == '.'
readPos = flip withFileLines (filter tag & zipWith addColumns [1..])
-- TODO: groupBy sentences (".\t\t\tIP"),
-- then map current code, then intercalate \n\n
addColumns i = words & conllise i & intercalate "\t"
-- TODO: Add the real columns (below are guessed from Talbanken)
conllise i [w, pos] = [show i, w, "_", pos, pos, "_", "0", "ROOT", "_", "_"]
main = System.getArgs >>= head & readPos >>= mapM_ putStrLn
