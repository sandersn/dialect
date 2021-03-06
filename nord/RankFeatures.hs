import Util
import Data.List (sort, sortBy)
import Data.List.Split (chunk)
import Data.Ord (comparing)
main = interactFiles (withFileLines rank) id
rank lines =
  chunk 2 diffs |> map tupleise |> leftright |> map format |> (header++)
  where (header,diffs) = splitAt 2 lines
        tupleise [name,value] = (name, read value :: Double)
        format (name, value) = name ++ " " ++ show value
leftright diffs = take 5 l ++ [("************",0.0)] ++ drop (length l - 5) l
  where l = sortBy (comparing snd) diffs
