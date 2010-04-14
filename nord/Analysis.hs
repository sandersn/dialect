-- just an analysis script. bunch of misc output munging basically --
import Util
import Text.Printf (printf)
import Data.List
import Data.List.Split (endBy, chunk)
import Control.Monad (liftM2)
import qualified Data.Map as Map
features = ["path", "trigram", "dep", "psg", "grand",
                    "unigram", "redep", "deparc", "all"]
measures = ["r", "r_sq", "kl", "js", "cos"]
-- main = withFileLines selfcor "correlations-R.txt" >>= mapM_ putStrLn
main = main' "full" "ratio"
main' sample norm = withFileLines (cor sample norm keySize) "correlations-R.txt"
                    >>= mapM_ putStrLn
cor sample norm key = filter (head & ((/='0') <&&> (/='-')))
                  & chunk 7 & map (map clean & key)
                  & Map.fromList & table sample norm & map (('&':) & (++"\\\\"))
clean s | dropWhile (/=':') s == "" = error (s ++ " sucks for some reason")
clean s = s |> dropWhile (/=':') & tail
key [title,_,geocor,geosig,travelcor,travelsig,sizecor,sizesig] =
  (words title, (significance geocor geosig,significance travelcor travelsig))
keySize [title,_,_,_,_,sizecor,sizesig] =
  (words title, ("", significance sizecor sizesig))
significance cor sig = printf "%.2f" (read cor :: Double) ++ stars (read sig)
  where stars n | n < 0.001 = "***"
                | n < 0.01  = "**"
                | n < 0.05  = "*"
                | otherwise = ""
table :: String -> String -> Map.Map [String] (String,String) -> [String]
table sample norm d = [intercalate " & " (map (foo f) measures) | f <- features]
  where foo feature measure = d Map.! [sample,measure,feature,norm] |> snd
                              -- fst chooses geo, snd chooses travel
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
----------
-- This is some code to find parameter sets without significant correlation
-- with corpus size.
-- TODO: It would be cool to also filter out the ones with non-significant
-- distances.
{- main = do
  cors <- return . chunk 3 . lines =<< readFile "cor-size.txt"
  let sigs = Map.fromList (map parse' cors)
  mapM_ putStrLn . Map.keys . Map.filter (snd & (>=0.05)) $ sigs
parse' [cor,sig,title] = (title,(parse cor, parse sig))
parse = words |> (!!1) |> (read :: String -> Double) -}

-- so, oh look, Perl 6 has a data structure that implicitly lifts operations
-- into the list monad. OH GREAT. Like I wouldn't rather do that explicitly
-- myself.

-- This is why Perl is stupid, and if you want a big language, Haskell
-- is far better. What makes your language big? And what's at its core?
-- Haskell is built up from small principles so the language looks
-- like it was meant for building things on. Perl feels like you're building a
-- structure on top of a slum.

-- Also the people running it are smart Brits instead of crazy Californians.

-- This is *exactly* like the flattened lists from Perl $EARLY (1? I'm not sure)
-- it's something you want to do sometimes, so naturally Perl builds it in for
-- you. Everywhere. (And wrong, in this case. You really want two operators,
-- 'flatten once' and 'repeat an operation for all levels of a list')
