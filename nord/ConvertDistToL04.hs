import Util
import Consts
import Data.List.Split (splitEvery)
main = argsFilePrinter (withFileLines revPair) id
revPair = (show (length swediaSites):) . (reverse swediaSites++)
          . (splitEvery 4 & map (!!2) & reverse)
