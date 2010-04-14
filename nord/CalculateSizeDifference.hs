import Util
import Consts
import qualified Data.Map as Map
import Data.Maybe (fromMaybe)
quoteSwedia = map quoteSpace swediaSites
main = putStr table
table = unlines (unwords quoteSwedia:[unwords (s:row s) | s <- quoteSwedia])
  where row s = [lk (s,s') |> show | s' <- quoteSwedia]
ds = Map.fromList [((quoteSpace r,quoteSpace r'),abs (s-s'))
                  | ((r,s), (r',s')) <- pairwise swediaSizes]
lk (s,s') = case Map.lookup (s,s') ds of
              Just d -> d
              Nothing -> fromMaybe 0 (Map.lookup (s',s) ds)
