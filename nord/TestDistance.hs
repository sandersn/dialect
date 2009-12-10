import Distance hiding (main)
import Test.QuickCheck.Batch
import Test.QuickCheck
import Control.Arrow ((&&&))
import Util
import Data.List (group, sort, nub)
import Data.List.Split (splitOn)
import qualified Data.Map as Map
{- instance Arbitrary Char where
    arbitrary     = choose ('\32', '\128')
    coarbitrary c = variant (ord c `rem` 4) -}

exampleLines = splitOn "\n" "Morgoth\na\nb\n***\na\nc"

prop_histogram_list :: [Int] -> Bool -- oops, this is a test for Util.
prop_histogram_list l = Map.toList (histogram l) == listhist l
  where listhist = sort & group & map (head &&& length)
prop_histogram_empty :: [Int] -> Bool
prop_histogram_empty l = (l == []) == (histogram l == Map.empty)

prop_r_empty :: Bool
prop_r_empty = r [] == 0.0
prop_r_one = r [(1,2)] == 1.0
prop_r_two = r [(1,2), (10,20)] == 11.0

prop_cmp_truncate :: [Int] -> [Int] -> Property
prop_cmp_truncate r1 r2 = (r2 /= [] && r1 /= []) ==>
                          length (cmp r1 r2) == length (nub r2)
prop_cmp_zeroes_r1 :: [Int] -> [Int] -> Property
prop_cmp_zeroes_r1 r1 r2 = (r2 /= [] && r1 /= []) ==>
  countBy (/=0.0) (map fst rcompare)
    == Map.size (histogram r1 `Map.intersection` histogram r2)
  where rcompare = cmp r1 r2
prop_cmp_iterate :: [Int] -> [Int] -> Property
prop_cmp_iterate r1 r2 = (r1 /= [] && r2 /= []) ==> all (\ ((a,b),(c,d)) -> abs (a - b) < abs (c - d)) $ zip (cmp r1 r2) $ map (\ (f,n) -> (fromIntegral $ Map.findWithDefault 0 f (histogram r1), fromIntegral n)) (Map.toList $ histogram r2)
  where rcompare = cmp r1 r2
main = runTests
         "The Basics"
         TestOptions {no_of_tests = 100
                     ,length_of_tests = 1
                     , debug_tests = False}
         [run prop_histogram_list
         , run prop_histogram_empty
         , run prop_r_empty
         , run prop_r_one
         , run prop_r_two
         , run prop_cmp_truncate
         , run prop_cmp_zeroes_r1
         , run prop_cmp_iterate]
