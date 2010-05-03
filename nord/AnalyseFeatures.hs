import Util
import qualified Data.Map as Map
import Text.Printf (printf)
import System (getArgs)
import Data.List (isPrefixOf, isInfixOf)
main = getArgs >>= mapM (withFileLines tail) >>= concat & scale & mapM_ putStrLn
scale lines = l |> histogram & norm (length l) & Map.filterWithKey match & format
  where l = lines |> filter (/="***")
        match :: String -> Double -> Bool
        match = redundantPossessivePronoun
norm len = Map.map (fromIntegral &  (/ fromIntegral len))
format d = map (uncurry (printf "%s %.5f")) (("TOTAL",sum (map snd l)):l)
  where l = Map.toList d
----------
possessiveArticleTrigram1 f n = any (`isInfixOf` f) bigrams
  where bigrams = ["PO-PO-NN", "PO-PO-AJ", "PO-AJ-NN"
                  , "NN-PO-NN", "NN-PO-AJ", "PO-AJ-NN"
                  , "PO-NN", "PO-AJ", "AJ-NN"]
possessiveArticleTrigram2 f n = f `elem` trigrams
  where trigrams = ["PO-PO-NN", "PO-PO-AJ", "PO-AJ-NN"
                   , "NN-PO-NN", "NN-PO-AJ", "PO-AJ-NN"]
possessiveArticleTrigram3 f n = any (`isInfixOf` f) bigrams
  where bigrams = ["PN-NN", "PO-NN", "NN-PN", "NN-PO"]
-- North: huset mitt
possessivePronounTrigram1 f n = any (`isInfixOf` f) bigrams
  where bigrams = ["NN-PO"]
-- South: mitt hus(et? I don't think so)
possessivePronounTrigram2 f n = any (`isInfixOf` f) bigrams
  where bigrams = ["PO-NN"]
redundantPossessivePronoun f n = f == "NN-PO-PN"
