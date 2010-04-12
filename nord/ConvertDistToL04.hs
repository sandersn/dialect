import Util
import Consts
import Data.List.Split (splitEvery)
main = interactFiles (withFileLines revPair) id
revPair = (show (length swediaLabels):) . (reverse swediaLabels++)
          . (splitEvery 4 & map (!!2) & reverse)
