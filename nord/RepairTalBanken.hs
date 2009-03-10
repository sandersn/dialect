import qualified Data.Map as Map
import Text.XML.HaXml (tag, (/>), txt, elm, attr, xmlParse, verbatim, showattr)
import Text.XML.HaXml.Types
type Id = Integer -- "s1_1" or "s1_501"
data FlatNode a = FlatNode a Id [Id] deriving (Eq, Show, Read)
data Tree a = Leaf a | Node a [Tree a] deriving (Eq, Show, Read)
type TalbankenInput = Map.Map Id (FlatNode String)

-- xml reading ok --
sentences = tag "corpus" /> tag "body" /> tag "s"
buildSentences :: [Content] -> [Tree String]
buildSentences = map (uncurry buildTree . buildMap)
buildMap :: Content -> (Id, Map.Map Id (FlatNode String))
buildMap s =
  (root, Map.fromList (map termentry terms ++ map nontermentry nonterms))
    where root = attrId "root" . head . (tag "s" /> tag "graph") $ s
          terms = tag "s" /> tag "graph" /> tag "terminals" /> tag "t" $ s
          nonterms = tag "s" /> tag "graph" /> tag "nonterminals" /> tag "nt" $ s
          termentry elem =
              let id = attrId "id" elem in
              (id, FlatNode (attr1 "pos" elem) id [])
          nontermentry elem =
              let id = attrId "id" elem in
              (id, FlatNode (attr1 "cat" elem) id (kids elem))
          kids = map (attrId "idref") . (tag "nt" /> tag "edge")
buildTree :: Id -> Map.Map Id (FlatNode String) -> Tree String
buildTree root flat = build (lookup root)
    where build (FlatNode s id []) = Leaf s
          build (FlatNode s id kids) = Node s (map (build . lookup) kids)
          lookup = (flat Map.!)
parseId :: String -> (String, Integer)
parseId s = (takeWhile (/='_') s, read . tail . dropWhile (/='_') $ s)
attrId a = snd . parseId . attr1 a
getContent (Document _ _ e _) = CElem e
attr1 attribute = verbatim . head . showattr attribute
run = return.buildSentences.sentences.getContent.
        xmlParse "SDshort.tiger.xml"=<<readFile "SDshort.tiger.xml"
main = print=<<run
