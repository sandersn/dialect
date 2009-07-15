import Sexp
import Util (count, window, (&), withFileLines)
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
extract region target = map (tail & init & runsexp)
                        & filter (/=Leaf "()")
                        & map (target & intercalate "\n")
                        & intercalate "\n***\n"
                        & ((region++"\n")++)
{-- trigrams --}
leaves (Leaf head) = [head]
leaves (Tree head kids) = concatMap leaves kids
trigrams = leaves & window 3 & map (intercalate "-") & filter (/="")
{--- leaf-ancestor paths --}
paths = makepaths & bracketpaths & map (map fst & intercalate "-")
makepaths tree = evalState (makepaths' [] tree) 0
  where makepaths' path (Leaf s) = incWith (\ i -> return [(s,i):path])
        makepaths' path (Tree s kids) = incWith $ \ i ->
          mapM (makepaths' ((s,i):path)) kids >>= concat & return
        incWith f = do i <- get; put (i+1); f i
bracketpaths paths = map (bracket . reverse) paths
  where spans = [node | (node,n) <- count (concat paths), n>1]
        edgeLeaf node = head . fromJust . find (elem node)
        firsts = Map.fromList [(node, edgeLeaf node paths) | node <- spans]
        lasts = Map.fromList
                [(node, edgeLeaf node (reverse paths)) | node <- spans]
        bracket path = case edge path firsts of
          (first1,f2:first2) -> first1 ++ f2 : ("[",0) : first2
          (_,[]) -> case edge path lasts of
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
