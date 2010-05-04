import Util
import qualified Data.Map as Map
import Text.Printf (printf)
import System (getArgs)
import Data.List (isPrefixOf, isInfixOf, isSuffixOf)
main = getArgs >>= mapM (withFileLines tail) >>= concat & scale & mapM_ putStrLn
scale lines = l |> histogram & norm (length l) & Map.filterWithKey match & format
  where l = lines |> filter (/="***")
        match :: String -> Double -> Bool
        match = ssacTrigram2
norm len = Map.map (fromIntegral &  (/ fromIntegral len))
format d = map (uncurry (printf "%s %.5f")) (("TOTAL",sum (map snd l)):l)
  where l = Map.toList d
----------
indefiniteProperNounsTrigram f n = "EN-PN" `isInfixOf` f
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
possessivePronounTrigram1 f n = "NN-PO" `isInfixOf` f
-- South: mitt hus(et? I don't think so)
possessivePronounTrigram2 f n = "PO-NN" `isInfixOf` f
redundantPossessivePronoun f n = f == "NN-PO-PN"
postadjectivalArticle1 f n = any (==f) trigrams
  where trigrams = ["EN-AJ-EN", "AJ-EN-NN"]
doubledefiniteTrigram f n = f == "PO-AJ-NN"
-- restrictive, similar to his survey
ssacTrigram1 f n = "AB-UK-PO"==f
-- oriented toward any coordinator that doesn't have a noun in front of it
-- meant to exclude true clefts.
ssacTrigram2 f n = "-UK-PO" `isSuffixOf` f && not (any (`isPrefixOf` f) nouns)
  where nouns = ["NN", "PO", "PR"]
