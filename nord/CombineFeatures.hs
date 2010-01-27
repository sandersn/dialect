import Util ((&))
import Data.List (transpose, intercalate)
import Data.List.Split (sepBy)
import System (getArgs)
import Control.Monad ((>=>))
main =
  getArgs >>= mapM (readFile >=> lines & return) >>= combine & mapM_ putStrLn
combine = map (sepBy ["***"]) & transpose & map concat & intercalate ["***"]
