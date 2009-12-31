import Test.HUnit
import Test.QuickCheck
import Test.QuickCheck.Batch
-- import Path hiding (main) -- NLP.PennTreebank not installed on peregrin
import DepPath hiding (main)
import Util
import Talbanken (FlatNode(..))
import Char
import Data.List.Split (endBy)
import Data.List (intercalate)
import qualified Data.Map as Map
instance Arbitrary Char where
  arbitrary = choose (32, 128) >>= chr & return
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

propProcessSameSentences ls = count "" ls == count "***" (lines $ process ls)
propProcessSameWords ls = length ls == length (lines $ process ls)

testProcessSames = ["sents" ~: True ~=? propProcessSameSentences talbankenSample
                   ,"words" ~: True ~=? propProcessSameWords talbankenSample]
talbankenSample = lines "1\tmen,\t_\tNN__SS\tNN__SS\t_\t12\tSS\t_\t_\n2\teh\t_\t++OC\t++OC\t_\t0\tROOT\t_\t_\n3\t###\t_\tNN__SS\tNN__SS\t_\t0\tROOT\t_\t_\n4\tdet\t_\tPODP\tPODP\t_\t0\tROOT\t_\t_\n5\tgick\t_\tVVPT\tVVPT\t_\t0\tROOT\t_\t_\n6\tratt\t_\tABZA\tABZA\t_\t0\tROOT\t_\t_\n7\tbra\t_\tABZA\tABZA\t_\t0\tROOT\t_\t_\n8\tdet\t_\tPODP\tPODP\t_\t10\tSS\t_\t_\n9\tdaor\t_\tID\tID\t_\t8\tHD\t_\t_\n10\t#\t_\tNNDD\tNNDD\t_\t0\tROOT\t_\t_\n11\tmed\t_\tPR\tPR\t_\t10\tOA\t_\t_\n12\tskolgangen\t_\tNNDDSS\tNNDDSS\t_\t0\tROOT\t_\t_\n13\t.\t_\tIP\tIP\t_\t12\tIP\t_\t_\n\n1\tvi\t_\tPOPPHH\tPOPPHH\t_\t0\tROOT\t_\t_\n2\thade\t_\tHVPT\tHVPT\t_\t0\tROOT\t_\t_\n3\tmiddagsrast\t_\tABZA\tABZA\t_\t0\tROOT\t_\t_\n4\t.\t_\t.\t.\t_\t0\tROOT\t_\t_\n"
sents = endBy [""] talbankenSample
[sent1, sent2] = sents
conll1 = [(["1", "ich", "", "PRON", "", "", "2", "", "", ""]
          , (1, FlatNode "PRON" "ich" 1 [2]))
         ,(["2", "liebe", "", "V", "", "", "0", "", "", ""]
          , (2, FlatNode "V" "liebe" 2 [0]))
         ,(["3", "bergen", "", "NNP", "", "", "2", "", "", ""]
          , (3, FlatNode "NNP" "bergen" 3 [2]))]
map1 = Map.fromList $ map snd conll1
deps1 = ["PRON-V","V","NNP-V"]
testsDeconllise (l,flat) = flat ~=? deconllise l
testBuildMap = map1 ~=? buildMap (map (intercalate "\t" . fst) conll1)
testBuildRelations = deps1 ~=? buildRelations map1
testBuilders = testBuildMap : testBuildRelations : map testsDeconllise conll1

main = do
  runTestTT $ TestList $ testProcessSames ++ testBuilders
  runTests "Path building" TestOptions {no_of_tests = 100
                                       ,length_of_tests = 1
                                       ,debug_tests = False}
           [run propProcessSameSentences
           ,run propProcessSameWords]
