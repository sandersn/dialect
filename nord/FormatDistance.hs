import Util hiding (groupBy)
import Consts (quoteSpace, swediaSites)
import Data.List.Split (splitEvery)
import Data.List (intercalate, groupBy)
import Data.Function (on)
import Data.Maybe (fromJust, fromMaybe)
import qualified Data.Map as Map
import System
quoteSwedia = map quoteSpace swediaSites
main = do
  [fname, target] <- getArgs
  outlines <- withFileLines (fromJust $ lookup target formatters) fname
  mapM_ putStrLn outlines
  where formatters = [("list", csv)
                     ,("pairwise", csvtable)
                     ,("square", rtable)]
dedot [from,to,d,var] = [clean from,clean to,d,var]
  where clean = quoteSpace . takeWhile (/='.')
dFrom [from,to,d,_] = (from,d)
dFromTo [from,to,d,_] = ((from,to),d)
csv = splitEvery 4 & map (dedot & intercalate ",")
csvtable = rows & map row & (:) (intercalate "," $ "":reverse (tail quoteSwedia))
  where rows = splitEvery 4 & map (dedot & dFrom) & groupBy ((==) `on` fst)
        row l = intercalate "," $ fst (head l):map snd (reverse l)
rtable lines =
  intercalate " " quoteSwedia : map (intercalate " " . fromRow) quoteSwedia
  where ds = lines |> splitEvery 4 & map (dedot & dFromTo) & Map.fromList
        fromRow from = from : [lookupPair (from,to) ds | to <- quoteSwedia]
lookupPair (from,to) ds = case Map.lookup (from,to) ds of
                            Just d -> d
                            Nothing -> fromMaybe "0" (Map.lookup (to,from) ds)
