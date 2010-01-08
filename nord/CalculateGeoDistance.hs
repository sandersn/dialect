import Consts
import Util
import qualified Data.Map as Map
main = mapM_ putStrLn (concatMap format (pairwise swediaSites))
pairwise l = [(x,y) | (i,x) <- zip [1..] l, y <- drop i l]
format (from,to) = [from,to,show $ distance from to, "IGNORED"]
distance from to = sqrt ((x-x')**2 + (y-y')**2)
  where (x,y) = both fromIntegral $ swediaSiteLocations Map.! from
        (x',y') = both fromIntegral $ swediaSiteLocations Map.! to
both f (x,y) = (f x, f y) -- isn't this in Control.Arrow somewhere?
