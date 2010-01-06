import Util
import Data.List.Split (splitEvery)
import Data.List (intercalate)
main = argsFilePrinter (withFileLines csved) id
csved = splitEvery 4 & map (deedle & intercalate ",")
deedle [from,to,d,var] = [takeWhile (/='.') from,takeWhile (/='.') to,d,var]
