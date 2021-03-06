import Test.HUnit
import Test.QuickCheck
import Test.QuickCheck.Batch
import Swedia
import Data.List (intercalate, isPrefixOf)
import Util
import Char (ord, chr, isSpace)
import qualified Data.Map as Map
import qualified Data.Set as Set
import qualified Consts
instance Arbitrary Char where
  arbitrary = choose (0, 256) >>= chr & return
  coarbitrary c = variant (ord c `rem` 4)
-- TODO: Test Swedia.splitter ([String] -> [[String]])
-- between --
testBetween = ["between normal" ~: between 'a' 'c' "abc" ~=? "b" ]
propBNotFound l a b = (a :: Int) `elem` l && not (b `elem` l) ==>
                  between a b l == tail (dropWhile (/=a) l)
propReconstruct l a b = (a :: Int) `elem` l ==>
                        (a : between a b l) `isPrefixOf` (dropWhile (/=a) l)
propLength l a b = (a :: Int) `elem` l ==> length l > length (between a b l)
-- newline/visible/trimsplit --
propNewLine "" = newline "" == False
propNewline s = (head s == '*') == (newline s)
propVisible "" = visible "" == True
propVisible s = (head s /= '.') == (visible s)
-- trimsplit produces a list of strings with all the same characters,
-- except whitespace, as the original string
propTrimSplit s = (trimsplit s |> concat) == (filter (not . isSpace) s)
-- groupedSites  --
testGrouped = ["all sites are used" ~: Map.keys groups ~=? Consts.swediaSites
              , "all files are used" ~:
               Set.fromList (concat (Map.elems groups))
               ~=? Set.fromList examplePaths]
  where groups = groupedSites Consts.swediaSites examplePaths
-- groupedRegions --
propNoop l = (collapse (`rem` 3) l |> Map.elems |> concat |> Set.fromList)
             == Set.fromList (l :: [Int])
-- readSwedia/splitter --
propSplitter lines =
  all (\ line -> if '*' `elem` line then ':' `elem` line else True) lines
        ==>
  ((lines
    |> dropWhile (not . newline)
    |> filter (isPrefixOf "*INT" & not)
    |> length)
   == length (splitter lines))
testReadSwedia :: String -> IO Bool
testReadSwedia f =
  readSwedia "./" f >>= head & take 3 & (==["jaha,", "jaha", "du"]) & return
umlaut = chr 0xCC : chr 0x88 : ""
ring = chr 0xCC : chr 0x8A : ""
examplePaths = [ "AnkarsrumOM_1sp.cha"
               , "AnkarsrumOM_3sp.cha"
               , "AnkarsrumYM_1sp.cha"
               , "AnundsjoOM_2OW_3sp.cha"
               , "Arjeplog.OM_1.tr.cha"
               , "ArsundaOM_1OW_1sp.cha"
               , "ArsundaOM_2OW_2sp.cha"
               , "AsbyOM_2sp.cha"
               , "AsbyOM_3sp.cha"
               , "AsbyYM_1sp.cha"
               , "BaraOM_1sp.cha"
               , "BaraOM_3sp.cha"
               , "BaraOM_4sp.cha"
               , "BengtsforsOM_1sp.cha"
               , "BengtsforsOM_2sp.cha"
               , "BengtsforsYM_2sp.cha"
               , "BodaOM_1sp.cha"
               , "BodaOM_3sp.cha"
               , "BodaOW_1sp.cha"
               , "BodaOW_2sp.cha"
               , "BredsatraOM_2sp.cha"
               , "BredsatraOM_3sp.cha"
               , "BredsatraOW_1sp.cha"
               , "FaroOM_1sp.cha"
               , "FaroOM_1sp.tra.cha"
               , "FaroOM_3sp.cha"
               , "FaroOM_3sp.tra.cha"
               , "FaroYM_1sp.cha"
               , "FaroYM_1sp.tra.cha"
               , "FlobyOM_1sp.cha"
               , "FlobyOM_2sp.cha"
               , "FlobyYM_3sp.cha"
               , "FoleOM_1sp.cha"
               , "FoleOM_1sp.tra.cha"
               , "FoleOM_2sp.cha"
               , "FoleOM_2sp.tra.cha"
               , "FoleYM_2sp.cha"
               , "FoleYM_2sp.tra.cha"
               , "FrillesasOM_2sp.cha"
               , "FrillesasOM_3sp.cha"
               , "FrillesasOW_2sp.cha"
               , "IndalOM_3sp.cha"
               , "IndalOW_2OW_3sp.cha"
               , "JamshogOM_1sp.cha"
               , "JamshogOM_2sp.cha"
               , "JamshogOW_1sp.cha"
               , "Ko"++umlaut++"laOM_2_OM_1sp.cha"
               , "Ko"++umlaut++"laOM_4sp.cha"
               , "Ko"++umlaut++"laYM_4_YM_3sp.cha"
               , "Leksand OW3s_OW4sp.cha"
               , "LeksandOM_1sp.cha"
               , "LeksandOM_3sp.cha"
               , "LoderupOM_3sp.DUBBLETT.cha"
               , "LoderupOM_3sp.cha"
               , "LoderupOW_1sp.cha"
               , "LoderupOW_2sp.cha"
               , "NederluleaOM2_OW3sp.tra.cha"
               , "Norra RorumOM_2sp.cha"
               , "Norra RorumOM_4sp.cha"
               , "Norra RorumOW_1sp.cha"
               , "OrustOM_1sp.cha"
               , "OrustOM_3sp.cha"
               , "OrustOW_3sp.cha"
               , "OrustOW_4sp.cha"
               , "OssjoOM_2sp.cha"
               , "OssjoOM_3sp.cha"
               , "OssjoOW_1sp.cha"
               , "OssjoOW_2sp.cha"
               , "OverkalixOM_3s.tra.cha"
               , "SegerstadOM_1sp.cha"
               , "SegerstadOM_2sp.cha"
               , "SegerstadYM_2sp.cha"
               , "SkinnskattebergOM_2sp.cha"
               , "SkinnskattebergOM_3sp.cha"
               , "SkinnskattebergYM_1sp.cha"
               , "SorundaOM_1sp.cha"
               , "SorundaOM_3sp.cha"
               , "SorundaYM_1sp.cha"
               , "SprogeOM_3sp.cha"
               , "SprogeOM_3sp.tra.cha"
               , "SprogeYM_2sp.cha"
               , "SprogeYM_2sp.tra.cha"
               , "StAnnaOM_2sp.cha"
               , "StAnnaOM_3sp.cha"
               , "StAnnaOW_2sp.cha"
               , "StAnnaOW_3sp.cha"
               , "Torsa"++ring++"sOM1.cha"
               , "Torsa"++ring++"sOM3.cha"
               , "Torsa"++ring++"sOW3.cha"
               , "TorsoOM_3sp.cha"
               , "TorsoOW_1sp.cha"
               , "Torso"++umlaut++"OM_2sp.cha"
               , "Torso"++umlaut++"OW_3sp.cha"
               , "VaxtorpOM_1sp.cha"
               , "VaxtorpOM_3sp.cha"
               , "VaxtorpYM_3sp.cha"
               , "VibyOM_1sp.cha"
               , "VibyOM_3sp.cha"
               , "VibyYM_2sp.cha"
               , "VillbergaOM_1sp.cha"
               , "VillbergaOM_3sp.cha"
               , "VillbergaYM_3sp.cha" ]
-- runner --
tests = TestList ((assertionPredicate (testReadSwedia "Test.cha") ~? "first 3 words") :
                  testBetween ++ testGrouped)
testmain = do
  runTestTT tests
  runTests "Swedia utilities" TestOptions { no_of_tests = 100
                                         , length_of_tests = 1
                                         , debug_tests = False }
           [run propBNotFound
           , run propReconstruct
           , run propLength
           , run propNewline
           , run propVisible
           , run propTrimSplit
           , run propSplitter
           , run propNoop]
