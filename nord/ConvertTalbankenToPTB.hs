module ConvertTalbankenToPTB where
import qualified Data.Map as Map
import Text.XML.HaXml (tag, (/>), xmlParse)
import Text.XML.HaXml.Types
import Util
import Talbanken
import Codec.Binary.UTF8.String (encodeString)

type TalbankenInput = Map.Map Id FlatNode

sentences = tagpath ["corpus", "body", "s"]
buildSentences :: [Content] -> [Tree String]
buildSentences = map buildTree . filter wellformed . map buildMap
buildMap :: Content -> (Id, Map.Map Id FlatNode)
buildMap s =
  (root, Map.fromList (map termentry terms ++ map nontermentry nonterms))
    where root = attrId "root" $ head $ tagpath ["s", "graph"] $ s
          -- for robustness, neither terms nor nonterms should be null
          terms = tagpath ["s", "graph", "terminals", "t"] s
          nonterms = tagpath ["s", "graph", "nonterminals", "nt"] s
          termentry elem = (id, FlatNode (replace ' ' '_' $ attr' "pos" elem)
                                         (ptbSafe $ attr' "word" elem) id [])
            where id = attrId "id" elem
          nontermentry elem = (id, FlatNode (attr' "cat" elem) "" id (kids elem))
            where id = attrId "id" elem
          kids = map (attrId "idref") . tagpath ["nt", "edge"]
          ptbSafe "(" = "LParen" -- should this be LRB/RRB?
          ptbSafe ")" = "RParen"
          ptbSafe s = encodeString s
wellformed (root,flat) = cat (flat Map.! root) == "ROOT"
buildTree (root,flat) = build (lookup root)
  where build (FlatNode s word id []) = Leaf s word
        build (FlatNode s "" id kids) = Node s (map (build . lookup) kids)
        lookup = (flat Map.!)
parseId :: String -> (String, Integer)
parseId s = (takeWhile (/='_') s, read . tail . dropWhile (/='_') $ s)
attrId a = snd . parseId . attr' a
parseTalbanken filename = withFile (posOfXml filename) filename
posOfXml filename = xmlParse filename & getContent & sentences & buildSentences
ptbShow (Leaf pos word) = "(" ++ pos ++ " " ++ word ++ ")"
ptbShow (Node a kids) = "("++a ++" "++ unwords (map ptbShow kids)++")"
main = interactFiles parseTalbanken ptbShow
