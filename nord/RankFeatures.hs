import Util
import Data.List (sort)
import Data.List.Split (splitEvery)
main = argsFilePrinter (withFileLines rank) id
rank lines =
  splitEvery 2 diffs |> map tupleise |> leftright |> map format |> (header++)
  where (header,diffs) = splitAt 2 lines
        tupleise [name,value] = (name, read value :: Double)
        format (name, value) = name ++ " " ++ show value
leftright diffs = take 5 l ++ [("************",0.0)] ++ drop (length l - 5) l
  where l = sort diffs
