import Test.HUnit
import Test.QuickCheck
import Test.QuickCheck.Batch
import Talbanken
import ConvertTalbankenToPTB
import Control.Monad (liftM, liftM2, sequence)
import Util
import Char
import Data.List (intercalate)
import qualified Data.Map as Map
import Text.XML.HaXml (xmlParse)

-- import ConvertTalbankenToTags
instance Arbitrary Char where
  arbitrary = choose (0, 256) >>= chr & return
  coarbitrary c = variant (ord c `rem` 4)
instance Arbitrary FlatNode where
  arbitrary = do
    cat <- arbitrary
    word <- arbitrary
    id <- arbitrary
    kids <- arbitrary
    return (FlatNode cat word id kids)
  coarbitrary n = variant 0
                  . coarbitrary (cat n)
                  . coarbitrary (word n)
                  . coarbitrary (Talbanken.id n)
                  . coarbitrary (sum (kids n))
instance Arbitrary a => Arbitrary (Tree a) where
  arbitrary = oneof [liftM2 Leaf arbitrary arbitrary,
                     liftM2 Node arbitrary arbitrary]
  coarbitrary (Leaf pos word) = variant 0 . coarbitrary pos . coarbitrary word
  coarbitrary (Node a kids) =
    variant 1 . coarbitrary a . oneof . mapM coarbitrary kids
instance Show a => Show (Tree a) where
--   show (Leaf pos word) = "(" ++ show pos ++ " " ++ show word ++ ")"
--   show (Node a kids) = "("++show a++ " "++intercalate " " (map show kids)++")"

  show (Leaf pos word) = "Leaf " ++ show pos ++ " " ++ show word
  show (Node a kids) = "Node "++show a++ " ["++intercalate ", " (map show kids)++"]"
size (Leaf _ _) = 1
size (Node a kids) = 1 + (sum $ map size kids)
concatData (Leaf pos word) = [pos,word]
concatData (Node a kids) = a : concatMap concatData kids
leaves (Leaf _ _) = 1
leaves (Node _ kids) = sum $ map leaves kids
nodes (Leaf _ _) = 0
nodes (Node a kids) = 1 + (sum $ map nodes kids)
kidsize (Leaf _ _) = 0
kidsize (Node a kids) = (max 0 (length kids - 1)) + (sum $ map kidsize kids)
-- this should work but doesn't. booo.
propParens :: Tree String -> Bool
propParens tree = length s == (concatData tree |> concat |> length) + leaves tree * 3 + nodes tree * 3 + kidsize tree
  where s = ptbShow tree
counterExample = Node "" [Leaf "" "",
                          Leaf "" "",
                          Node "" [Leaf "" "",
                                   Node "" [Node "" [Node "" []]],
                                   Node "" []]]
testEmptyLeaf = "( )" ~=? ptbShow (Leaf "" "")
exampleXml = "<?xml version='1.0' encoding='ISO-8859-1'?>\
\<corpus><body><s><graph root='s1_501'>\
\<terminals>\
\<t id='s1_0' pos='foo' word='one' />\
\<t id='s1_1' pos='foo' word='two' />\
\<t id='s1_2' pos='foo' word='three' />\
\</terminals>\
\\
\<nonterminals>\
\<nt id='s1_501' cat='ROOT'>\
\  <edge idref='s1_0' />\
\  <edge idref='s1_510' />\
\</nt>\
\<nt id='s1_510' cat='NN'>\
\  <edge idref='s1_1' />\
\  <edge idref='s1_2' />\
\</nt>\
\</nonterminals>\
\</graph></s></body></corpus>"
flatParse = xmlParse "foo" & getContent & sentences & map buildMap
-- TODO: Test POS vs word placement for PTB format as read by Berkeley
testExampleParse = [[Node "ROOT" [Leaf "foo" "one", Node "NN" [Leaf "foo" "two", Leaf "foo" "three"]]] ~=? posOfXml "foo" exampleXml,
                    [(501,Map.fromList [(0,FlatNode {cat = "foo", word = "one", Talbanken.id = 0, kids = []}),
                                    (1,FlatNode {cat = "foo", word = "two", Talbanken.id = 1, kids = []}),
                                    (2,FlatNode {cat = "foo", word = "three", Talbanken.id = 2, kids = []}),
                                    (501,FlatNode {cat = "ROOT", word = "", Talbanken.id = 501, kids = [0,510]}),
                                    (510,FlatNode {cat = "NN", word = "", Talbanken.id = 510, kids = [1,2]})])]

                    ~=? flatParse exampleXml]
tests = TestList (testEmptyLeaf:testExampleParse)
testmain = do
  runTestTT tests
  runTests "PTB conversion (pure)" TestOptions {no_of_tests = 100,
                                                length_of_tests = 1,
                                                debug_tests = False }
           [run propParens]
