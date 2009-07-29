import Sexp
import Util (count, window, (|>), (&), withFileLines)
import Data.List (intercalate,find)
import Data.Maybe (fromJust)
import Control.Monad.State.Lazy (State, get, put, evalState)
import qualified Data.Map as Map
import System
main = do
    [region, target] <- getArgs
    s <- withFileLines (extract region (if target=="t" then trigrams else paths))
                       region
    putStr s
extract region target = map (tail & tail & init & runsexp)
                        & filter (/=Node "()" [])
                        & map (target & intercalate "\n")
                        & intercalate "\n***\n"
                        & ((region++"\n")++)
{-- trigrams --}
leaves (Node head []) = [head]
leaves (Node head kids) = concatMap leaves kids
trigrams = leaves & window 3 & map (intercalate "-") & filter (/="")
{--- leaf-ancestor paths --}
paths = makepaths & bracketpaths & map (map fst & intercalate "-")
gensym x f = do i <- get; put $ succ i; f (x,i)
runGensym f = evalState f 0
makepaths = runGensym . makepaths' []
  where makepaths' path (Node s []) = gensym s (\ node -> return $ [node:path])
        makepaths' path (Node s kids) = gensym s $ (\ node ->
          mapM (makepaths' (node:path)) kids >>= concat & return)
bracketpaths paths = map (bracket . reverse) paths
  where nodes = count (concat paths) |> Map.filter (>1) --also filters singletons
        edgeLeaf paths node _ = find (elem node) paths |> fromJust |> head
        bracket path = case edge path (Map.mapWithKey (edgeLeaf paths) nodes) of
          (first1,f2:first2) -> first1 ++ f2 : ("[",0) : first2
          (_,[]) ->
            case edge path (Map.mapWithKey (edgeLeaf (reverse paths)) nodes) of
              (last1, last2@(_:_)) -> last1 ++ ("]",0) : last2
              (last1, []) -> last1
edge path edges = break foundNode path
  where foundNode node = node `Map.member` edges && edges Map.! node == last path
{--- DEBUG ---}
sent = runsexp " (A (B p q) (B r s)) "
sent' = runsexp "(A (B p q r s))"
ps = makepaths sent
ps' = makepaths sent'
answer = ["A-[-B-p", "A-]-B-q", "A-B-[-r", "]-A-B-s"]
answer' = ["A-[-B-p", "A-B-q", "A-B-r", "]-A-B-s"]
