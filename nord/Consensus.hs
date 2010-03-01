import qualified Data.Set as Set
import qualified Data.Map as Map
import Data.List
import Data.Ord (comparing)
import Data.Function (on)
import Control.Monad.State
import Control.Arrow (first, second)
import Util
import Consts
data Tree a = Leaf a | Node a [Tree a] deriving (Show)
root tree = Node "ROOT" [Leaf "s0", tree]
leaf (Leaf _) = True
leaf (Node _ []) = True -- irregularities in buildNode, oh well
leaf _ = False

spans (Leaf a) = Set.singleton $ Set.singleton a
spans (Node _ kids) = Set.insert (Set.unions $ Set.toList kidspans) kidspans
  where kidspans = Set.unions $ map spans kids
majority trees = trees
               |> map (spans & Set.toList & flip zip (repeat 1) & Map.fromList)
               |> Map.unionsWith (+)
               |> Map.filter (>m)
               |> Map.keys
               |> sortBy (comparing (negate . Set.size))
  where m = floor (fromIntegral (length trees) / 2)
-- functional --
buildNode _ [] = ([],[])
buildNode span (next:rest) = if Set.isSubsetOf next span
  then first (next:) (buildNode (span `Set.difference` next) rest)
  else second (next:) (buildNode span rest)
-- I hate typing consensus so I shortened it for now.
con trees = majority (map root trees) |> buildTree |> fst
buildTree [span] = (Leaf span, [])
buildTree (span:ranks) = let (kids, rest) = buildNode span ranks in
                         first (Node span) (foldl buildKids ([],rest) kids)
  where buildKids (nodes,rest) span = first (:nodes) (buildTree (span:rest))
-- imperative --
buildNode' span =
  ifM isStackEmpty
    (return [])
    (ifM (return . (`Set.isSubsetOf` span) =<< peek)
         (liftM2 (:) peek (buildNode' . Set.difference span =<< pop))
--          (do
--            rank <- pop
--            span' <- buildNode' (span `Set.difference` rank)
--            return (rank:span'))
         (do
           rank <- pop
           span' <- buildNode' span
           push rank
           return span'))
ifM cond seq alt = do
  b <- cond
  if b then seq else alt
buildTree' span =
  ifM isStackEmpty
    (return (Leaf span))
    ((return . Node span <=< mapM buildTree') =<< buildNode' span)
--     (do
--        kids <- buildNode' span
--        nodes <- mapM buildTree' kids
--        return (Node span nodes))
consensus trees = evalState (buildTree' span) ranks
  where (span:ranks) = majority (map root trees)
-- utils --
isStackEmpty = return . (==[]) =<< get
peek = return . head =<< get
pop = do
  first:rest <- get
  put rest
  return first
push x = put . (x:) =<< get
-- test --
t1 = Node "a" [Node "b" [Node "c" [Leaf "s1", Leaf "s2"], Leaf "s3"], Leaf "s4"]
t2 = Node "a" [Node "b" [Leaf "s1", Node "c" [Leaf "s2", Leaf "s3"]], Leaf "s4"]
t3 = Node "a" [Leaf "s1", Node "b" [Node "c" [Leaf "s2", Leaf "s3"], Leaf "s4"]]
ts = [t1,t2,t3]
-- reader --
main = do
  sigs <- withFileLines findSigs "sig-10-1000-interview.csv"
  interactFiles (withFileLines (makeConsensusTree sigs & list)) qtree
qtree (Leaf a) = Set.findMax a
qtree (Node a []) = Set.findMax a
qtree (Node a kids) = "[. {" ++ left ++ "} " ++ right ++ " ]"
  where (leaves,nodes) = partition leaf kids
        left = intercalate "\\\\" (map qtree leaves)
        right = unwords (map qtree nodes)
findSigs =
  tail
  & map (replace ',' ' ' & words & tail
         & zip ["path", "trigram", "dep", "psg", "grand", "unigram", "all"]
         & filter (snd & (=="0"))
         & map fst)
  & zip ["r", "r_sq", "kl", "js", "cos"]
  & concatMap (uncurry (zip . repeat))
  & Set.fromList
makeConsensusTree sigs =
  filter (isPrefixOf "Cluster: ")
  & map rReader
  & filter (fst & (`Set.member` sigs))
  & map (snd & buildRTree)
  & con
rReader line = ((measure,features),
                splitAt (floor (fromIntegral (length ns) / 2)) ns |> uncurry zip)
  where (_:measure:features:ss) = words line
        ns = map read ss
label (Leaf a) = a
label (Node a _) = a
buildRTree tuples = last nodes
  where nodes = map buildNode tuples
        buildNode (i,j) = Node ('$':label inode++label jnode) [inode,jnode]
          where (inode,jnode) = (buildChild i, buildChild j)
        buildChild i | i < 0 = Leaf $ swediaSites !! (-i-1)
                     | otherwise = nodes !! (i-1)
