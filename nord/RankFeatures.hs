import Util
import Data.List (sort, sortBy)
import Data.List.Split (splitEvery)
import Data.Ord (comparing)
import Control.Monad (sequence, mapM_, (>=>))
import System (getArgs)
argsFilePrinter' :: (String -> IO [String]) -> IO ()
argsFilePrinter' read = getArgs >>= mapM_ (read >=> mapM_ putStrLn)
main = argsFilePrinter' (withFileLines rank)
rank lines =
  splitEvery 2 diffs |> map tupleise |> leftright |> map format |> (header++)
  where (header,diffs) = splitAt 2 lines
        tupleise [name,value] = (name, read value :: Double)
        format (name, value) = name ++ " " ++ show value
leftright diffs = take 5 l ++ [("************",0.0)] ++ drop (length l - 5) l
  where l = sortBy (comparing snd) diffs
