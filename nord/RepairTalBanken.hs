import qualified Data.Map as Map
import Text.XML.HaXml (tag, (/>), xmlParse)
import Text.XML.HaXml.Types
import Util
import Data.List (intercalate)
type Id = Integer -- "s1_1" or "s1_501"
data FlatNode = FlatNode { cat :: String,
                           word :: String,
                           id :: Id,
                           kids::[Id] } deriving (Eq, Show, Read)
data Tree a = Leaf a a | Node a [Tree a] deriving (Eq, Show, Read)
dat (Leaf a _) = a
dat (Node a _) = a
children (Leaf _ _) = []
children (Node _ kids) = kids
type TalbankenInput = Map.Map Id FlatNode

-- xml reading ok --
sentences = tagpath ["corpus", "body", "s"]
buildSentences :: [Content] -> [Tree String]
buildSentences = map (uncurry buildTree . buildMap)
buildMap :: Content -> (Id, Map.Map Id FlatNode)
buildMap s =
  (root, Map.fromList (map termentry terms ++ map nontermentry nonterms))
    where root = attrId "root" . head . (tag "s" /> tag "graph") $ s
          terms = tagpath ["s", "graph", "terminals", "t"] s
          nonterms = tagpath ["s", "graph", "nonterminals", "nt"] s
          termentry elem =
              let id = attrId "id" elem in
              (id, FlatNode (replace ' ' '_' $ attr' "pos" elem)
                            (utf8FromLatin1 $ attr' "word" elem) id [])
          nontermentry elem =
              let id = attrId "id" elem in
              (id, FlatNode (attr' "cat" elem) "" id (kids elem))
          kids = map (attrId "idref") . (tag "nt" /> tag "edge")
buildTree :: Id -> Map.Map Id FlatNode -> Tree String
buildTree root flat = build (lookup root)
    where build (FlatNode s word id []) = Leaf s word
          build (FlatNode s "" id kids) = Node s (map (build . lookup) kids)
          lookup = (flat Map.!)
parseId :: String -> (String, Integer)
parseId s = (takeWhile (/='_') s, read . tail . dropWhile (/='_') $ s)
attrId a = snd . parseId . attr' a
run filename = withFile filename $
    xmlParse filename & getContent & sentences & buildSentences
ptb (Leaf pos word) = "(" ++ pos ++ " " ++ word ++ ")"
ptb (Node a kids) = "(" ++ a ++ " " ++ intercalate " " (map ptb kids) ++ ")"
main = multiFilePrinter run ptb
------- yet another uncrosser ------------
example = Node ("S", 555)
          [Node ("VP",510)
           [Node ("NP",502)
            [Leaf ("DET",0) ("Das",0), Leaf ("N",1) ("Buch",1), Leaf ("PRON",4) ("ihm",4)]
           , Leaf ("V",2) ("gegeben",2)
           , Leaf ("PART",5) ("habe",5)]
          , Node ("NP",501) [Leaf ("PRON",3) ("ich",3)]]
sexample = spanTree example
spanTree :: Tree (String, Integer) -> Tree (Integer, Integer)
spanTree (Leaf (_,i) _) = Leaf (i,i+1) (i,i+1)
spanTree (Node _ kids) = Node (minimum starts, maximum ends) trees
    where trees = map spanTree kids
          starts = map (fst . dat) trees
          ends = map (snd . dat) trees
uncross' :: [Tree (Integer,Integer)] -> [Tree (Integer,Integer)]
uncross' [] = []
uncross' (Leaf a w : siblings) = Leaf a w : uncross' siblings
uncross' (Node a kids : siblings) = uncross''.both depair.span continuous.pairs
                                    $ kids
    where uncross'' (co,[]) = co ++ uncross' siblings
          uncross'' (co,disco) = co ++ uncross' (insert siblings disco)
pairs l = zip l (tail l)
both f (x,y) = (f x, f y)
continuous (t, t') = snd (dat t) == fst (dat t')
depair l = (fst $ head l) : map snd l
insert = (++) -- insert has to stick disco in siblings somewhere and then uncross
         -- it all. Not necessarily in that order.
{-uncross (Node a kids) = Node a (uncross' kids)
uncross l = l
uncross' :: [Siblings] -> [Siblings] -- but uncrossed
-- OK the problem is that insert might need to drop disco down a couple of levels into siblings
-- in other words, the first step is the check what siblings disco belongs IN or AFTER
-- then you may have to insert down, ie repeat the insert for the chosen sibling's kids
-- ... told you there might be a lot of consing!
insert siblings disco = let (before,actual:after) = splitBy ((lhs disco) >) siblings in
    if rhs disco > lhs actual then -- or something like this
       before ++ actual : disco ++ after -- um..you get the idea
    else
       before ++ (insert (kids actual) disco : after) -- whoo CONS! -}
       -- also this recursive step should do some uncrossing of before and after, right?

{- The idea is that you start at the leftmost kid of a Node.
   You take as much as is continuous and you cons that onto the rest of the siblings+disco
   after that has all been uncrossed.
   co : uncross (insert disco siblings)
   except that uncross has to take additional arguments?
   also some uncrossings may have to burrow arbitrarily deep. I'm not sure of the limit yet.
   Anyway you'd have to do it either way, bottom-up or top-down, so at least top-down it's
   easier to maintain pointers to it all even if there is a lot of consing involved.

   actually now that I sleep on it, I'm not sure about arbitrary deepness. I think that's
   needed only if you want to try Wolfgang's bottom-up style. Adriane Boyd's split style
   just attaches the disco part as a sibling to the co part I think.
-}
