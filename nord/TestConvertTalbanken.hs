import Test.HUnit
import Test.QuickCheck
import Test.QuickCheck.Batch
import Talbanken
import ConvertTalbankenToTags hiding (main)
import ConvertTalbankenToPTB hiding (main)
import Control.Monad (liftM, liftM2, sequence)
import Util
import Char
import Data.List (intercalate)
import qualified Data.Map as Map
import Text.XML.HaXml (xmlParse)
-- background instances for QuickCheck --
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
  show (Leaf pos word) = "Leaf " ++ show pos ++ " " ++ show word
  show (Node a kids) = "Node "++show a++ " ["++intercalate ", " (map show kids)++"]"
size (Leaf _ _) = 1
size (Node a kids) = 1 + (sum $ map size kids)
concatData (Leaf pos word) = [pos,word]
concatData (Node a kids) = a : concatMap concatData kids
terminals (Leaf _ word) = [word]
terminals (Node a kids) = concatMap terminals kids
leaves (Leaf _ _) = 1
leaves (Node _ kids) = sum $ map leaves kids
nodes (Leaf _ _) = 0
nodes (Node a kids) = 1 + (sum $ map nodes kids)
kidsize (Leaf _ _) = 0
kidsize (Node a kids) = (max 0 (length kids - 1)) + (sum $ map kidsize kids)
-- this should work but doesn't. booo.
propParens :: Tree String -> Bool
propParens tree = length s == (concatData tree |> concat |> length)
                              + leaves tree * 3 + nodes tree * 3 + kidsize tree
  where s = ptbShow tree
counterExample = Node "" [Leaf "" "",
                          Leaf "" "",
                          Node "" [Leaf "" "",
                                   Node "" [Node "" [Node "" []]],
                                   Node "" []]]
testShowTree = ["( )" ~=? ptbShow (Leaf "" ""),
                "( )" ~=? ptbShow (Node "" []),
                "(foo )" ~=? ptbShow (Node "foo" []),
                "(foo ( ))" ~=? ptbShow (Node "foo" [Leaf "" ""]),
                "(foo (bar ))" ~=? ptbShow (Node "foo" [Leaf "bar" ""]),
                "(foo (bar baz))" ~=? ptbShow (Node "foo" [Leaf "bar" "baz"])]
-- end-to-end parsing test --
normal = ("<?xml version='1.0' encoding='ISO-8859-1'?>\
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
 , (501,Map.fromList [(0,FlatNode "foo" "one" 0 []),
                      (1,FlatNode "foo" "two" 1 []),
                      (2,FlatNode "foo" "three" 2 []),
                      (501,FlatNode "ROOT" "" 501 [0,510]),
                      (510,FlatNode "NN" "" 510 [1,2])])
 , Node "ROOT"
    [Leaf "foo" "one"
    , Node "NN" [Leaf "foo" "two", Leaf "foo" "three"]]
 , [(".","IP"),("one", "foo"), ("two", "foo"), ("three", "foo")])
leafless = ("<?xml version='1.0' encoding='ISO-8859-1'?>\
 \<corpus><body><s><graph root='s1_501'>\
 \<terminals>\
 \</terminals>\
 \\
 \<nonterminals>\
 \<nt id='s1_501' cat='ROOT'>\
 \  <edge idref='s1_510' />\
 \</nt>\
 \<nt id='s1_510' cat='NN'>\
 \</nt>\
 \</nonterminals>\
 \</graph></s></body></corpus>"
 , (501,Map.fromList [(501,FlatNode "ROOT" "" 501 [510])
                     ,(510,FlatNode "NN" "" 510 [])])
 , Node "ROOT" [Leaf "NN" ""]
 , [(".","IP")])
treeless = ("<?xml version='1.0' encoding='ISO-8859-1'?>\
 \<corpus><body><s><graph root='s1_0'>\
 \<terminals>\
 \<t id='s1_0' pos='ROOT' word='one' />\
 \<t id='s1_1' pos='foo' word='two' />\
 \<t id='s1_2' pos='foo' word='three' />\
 \</terminals>\
 \\
 \<nonterminals>\
 \</nonterminals>\
 \</graph></s></body></corpus>"
 , (0,Map.fromList [(0,FlatNode "ROOT" "one" 0 []),
                    (1,FlatNode "foo" "two" 1 []),
                    (2,FlatNode "foo" "three" 2 [])])
 , Leaf "ROOT" "one"
 , [(".","IP"),("one", "ROOT"),("two","foo"),("three","foo")])
-- test sentences & map buildMap
flatParse = xmlParse "foo" & getContent & sentences & map buildMap
propTerminals xml = all prop (zip (buildSentences ss) ss)
  where ss = sentences $ getContent xml
        prop (s,xml) = terminals s == map termentry (terms xml)
        terms = tagpath ["s", "graph", "terminals", "t"]
        termentry = attr' "word"
-- test all end-to-end plus intermediate stages
propsParse (xml,flat,tree,_) =
  ["xmlToFlat" ~: [flat] ~=? flatParse xml
  ,"flatToTree" ~: tree ~=? buildTree flat
  ,"xmlToTree" ~: [tree] ~=? ConvertTalbankenToPTB.posOfXml "foo" xml]
  -- Current implementation DOES add terminals in the presence of dangling edges
  -- on non-terminals
  -- It also drops terminals that are not pointed to by some nonterminal.
  -- ,TestCase $ assertBool "Doesn't add or remove terminals"
  --                            (propTerminals $ xmlParse "foo" xml)]
testParse = concatMap propsParse [normal, leafless, treeless]
-- test this now --

propsTags (xml,_,_,attrs) =
  ["xmlToAttrs" ~: attrs ~=? ConvertTalbankenToTags.posOfXml "foo" xml]
testTags = concatMap propsTags [normal, leafless, treeless]
-- TODO: What is the Haskell equivalent to assertThrows/assertRaises
testWellFormed =
  [TestCase $ assertBool "no root"
   (not $ wellformed (501,Map.fromList [(501, FlatNode "NOT-ROOT" "too" 501 [])]))]
                 -- ,"bad pointer" ~: assertErrors (wellformed (501,Map.empty))]
propIds s = '_' `elem` s && (all isDigit (tail $ dropWhile (/='_') s)) ==>
            (let (name,id) = parseId s in
              length name + length (show id) + 1 == length s)
testParseId = [("s",501) ~=? parseId "s_501"
              ,("",500) ~=? parseId "_500"
              ,("",500) ~=? parseId "_000500"
              ,("",0) ~=? parseId "_0000"] -- ,assertErrors parseId "s_"
tests = TestList (testParseId
                  ++testParse
                  ++testShowTree
                  ++testWellFormed
                  ++testTags)
main = do
  runTestTT tests
  runTests "PTB conversion (pure)" TestOptions {no_of_tests = 100,
                                                length_of_tests = 1,
                                                debug_tests = False }
           [run propIds]
           -- , run propParens]
