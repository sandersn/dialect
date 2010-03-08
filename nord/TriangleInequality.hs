import Control.Monad (msum,liftM3)
import qualified Data.Map as Map
import Data.List.Split (splitEvery)
import Util
import Consts (quoteSpace, swediaSites)
main = putStrLn . show =<< triangle
triangle = do
  ls <- readFile "dist-10-1000-r-all-interview.txt"
  let quarts = splitEvery 4 $ lines $ ls
  let d = dist (map (dedot & item) quarts |> Map.fromList)
  return $ filter (\ (x,y,z) -> d(x,y) + d(y,z) - d(x,z) < 0) sites
dedot [from,to,d,var] = [takeWhile (/='.') from,takeWhile (/='.') to,d,var]
item [from,to,d,_] = ((clean from, clean to), read d :: Double)
  where clean = takeWhile (/='.')
dist ds (x,y) = Map.findWithDefault (Map.findWithDefault 0 (y,x) ds) (x,y) ds
sites = liftM3 (,,) Consts.swediaSites Consts.swediaSites Consts.swediaSites
