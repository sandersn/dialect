module Lev where
import qualified Data.Map as Dct
import Control.Monad (liftM)
enum = zip [0..]
takeFail 0 _ = Just []
takeFail _ [] = Nothing
takeFail n (x:xs) = liftM (x:) (takeFail (n - 1) xs)
window n l = case takeFail n l of
             Nothing -> []
             Just xs -> xs : window n (tail l)
-- _levenshtein :: (Enum b, Num b, Ord b) =>
                -- [t] -> [a] -> b -> (a -> b, t -> b, a -> t -> b) -> [b]
_levenshtein ss ts indel (ins,del,sub) =
    let initial l = [0,indel..indel * fromIntegral (length l)]
    in foldl (\ table (i,s) ->
              (foldl (\ row (t,[prev,prev']) ->
                      minimum [ins t + head row, del s + prev', sub s t + prev]
                      : row)
                     [i]
-- doesn't work without double reverse. i suspect only (window 2) needs reverse
                     (zip ts . window 2 {- . reverse-} $ table)))
             (initial ts) {-(reverse (initial ts))-} (zip (tail (initial ss)) ss)
