import qualified Data.Set as Set
import qualified Data.Map as Map
import Data.List
import Data.Ord (comparing)
import Data.Function (on)
import Control.Monad.State
import Util
import Consts
data Tree a = Leaf a | Node a [Tree a] deriving (Show)
root tree = Node "ROOT" [Leaf "s0", tree]
leaf (Leaf _) = True
leaf (Node _ []) = True -- irregularities in buildRank, oh well
leaf _ = False

spans (Leaf a) = Set.singleton $ Set.singleton a
spans (Node _ kids) = Set.insert (Set.unions $ Set.toList kidspans) kidspans
  where kidspans = Set.unions $ map spans kids
majority trees = trees |> map (spans & Set.toList & histogram)
                        |> Map.unionsWith (+)
                        |> Map.filter (>m)
                        |> Map.keys
                        |> sortBy (comparing (negate . Set.size))
                        |> Data.List.groupBy ((==) `on` Set.size)
  where m = floor (fromIntegral (length trees) / 2)
-- functional --
buildRank span [] = ([],[])
buildRank span (rank:ranks) | Set.null span = ([],rank:ranks)
buildRank span (rank:ranks) =
  (kids++kids',if rest==[] then rests else rest:rests)
  where (kids, rest) = partition (`Set.isSubsetOf` span) rank
        (kids', rests) = buildRank (span `Set.difference` Set.unions kids) ranks
-- I hate typing consensus so I shortened it for now.
con trees = buildTree span ranks |> fst
  where ([span]:ranks) = majority (map root trees)
buildTree span [] = (Leaf span, [])
buildTree span ranks = (Node span kids', rest')
  where (kids, rest) = buildRank span ranks
        (kids', rest') =
          foldl (\ (kids,rest) span -> let (node,rest') = buildTree span rest in
                                       (node : kids, rest'))
                ([],rest) kids
-- imperative --
buildRank' span = ifM (return . (==[]) =<< get)
  (return [])
  (do (kids,rest) <- return . partition (`Set.isSubsetOf` span) =<< pop
      kids' <- buildRank' (span `Set.difference` Set.unions kids)
      when (rest /= []) $
           push rest
      return (kids++kids'))
  {- nullp <- get >>= (==[])
  if nullp
    then return []
    else do
      (kids,rest) <- return . partition (`Set.isSubsetOf` span) =<< pop
      kids' <- buildRank' (span `Set.difference` Set.unions kids)
      when (rest /= []) $
        push rest
      return (kids++kids') -}
ifM cond seq alt = do
  b <- cond
  if b then seq else alt
buildTree' span = ifM (return . (==[]) =<< get)
  (return (Leaf span))
  (buildRank' span >>= (foldM (\ l -> buildTree' >=> (:l) & return) []
                        >=> Node (Set.empty) & return))
  {- rest <- get
  if rest==[]
    then return (Leaf span)
    else do
      kids <- buildRank' span
      kids' <- foldM (\ l kid -> buildTree' kid >>= (:l) & return) [] kids
      return (Node span kids')-}
consensus trees = evalState (buildTree' span) ranks
  where ([span]:ranks) = majority (map root trees)
-- utils --
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
