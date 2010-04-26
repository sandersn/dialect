-- just an analysis script. bunch of misc output munging basically --
import Util
import Text.Printf (printf)
import Data.List
import Data.List.Split (endBy, chunk)
import Control.Monad (liftM2, (>=>))
import System (getArgs)
import Data.Maybe (fromJust)
import qualified Data.Map as Map
features = ["path", "trigram", "dep", "psg", "grand",
                    "unigram", "redep", "deparc", "all"]
measures = ["r", "r_sq", "kl", "js", "cos"]
-- main = withFileLines selfcor "correlations-R.txt" >>= mapM_ putStrLn
keys = [("geo", keyGeo)
       ,("travel", keyTravel)
       ,("size", keySize)]
main = do
  [num,sample,norm,key] <- getArgs
  main' (num,sample,norm) (lookup key keys |> fromJust)
main' variant key =
  withFileLines (cor variant key) "correlations-R.txt" >>= mapM_ putStrLn
cor variant key = filter (head & ((/='0') <&&> (/='-')))
                  & chunk 8 & map (map clean & key)
                  & Map.fromList & table variant & map (('&':) & (++"\\\\"))
clean s | dropWhile (/=':') s == "" = error (s ++ " sucks for some reason")
clean s = s |> dropWhile (/=':') & tail
keyGeo [title,_,cor,sig,_,_,_,_] = (words title, (significance cor sig))
keySize [title,_,_,_,_,cor,sig] = (words title, (significance cor sig))
keyTravel [title,_,_,_,cor,sig,_,_] = (words title, (significance cor sig))

significance cor sig = printf "%.2f" (read cor :: Double) ++ stars (read sig)
  where stars n | n < 0.001 = "***"
                | n < 0.01  = "**"
                | n < 0.05  = "*"
                | otherwise = ""
table :: (String,String,String) -> Map.Map [String] String -> [String]
table (num,sample,norm) d = [intercalate " & " (map (foo f) measures) | f <- features]
  where foo feature measure = d Map.! [num,sample,measure,feature,norm]
f <&&> g = liftM2 (&&) f g
f <||> g = liftM2 (||) f g
----------
selfcor = filter (head & ((=='0') <||> (==' ') <||> (=='-')))
          & chunk 9 & map selfkey
          & Map.fromList & Map.filterWithKey desired & Map.elems
          & averageall & format
format = map (map (uncurry (printf "%.2f(%d)")) & intercalate " & ")
desired [sample,_,f,n] _ = sample=="1000" -- full is never significant
filterSigs l = [cor | (cor,sig) <- l, sig < 5.0]
averageall = transpose & map (transpose &  map (filterSigs & avg))
  where avg [] = (-9999.0, 0)
        avg l = (sum l / fromIntegral (length l), length l) -- SLOW but who cares
selfkey (title:rest) = (words $ clean title, map parseSig (drop 4 rest))
parseSig = map (pair . map (read :: String -> Double) . words) . endBy ","
  where pair [x,y] = (x,y)
        pair l = error ( "Not a two-element list:" ++ show l)
