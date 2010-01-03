import Test.HUnit
import Test.QuickCheck
import Test.QuickCheck.Batch
import ConvertTagsToConll hiding (main)
import ConvertTagsToTxt hiding (main)
import Util
import Char
instance Arbitrary Char where
  arbitrary = choose (32, 128) >>= chr & return
  coarbitrary c = variant (ord c `rem` 4)
testIsTag = [True ~=? tag "foo"
            ,False ~=? tag "% it's a comment"] -- assertThrows $ tag ""
propTag s@[] = True -- fail? I don't know
propTag s@('%':_) = tag s == False
propTag s = tag s == True
testIsSentenceEnd = ["does end" ~: True ~=? sentenceEnd ".\t\tIP I guess"
                    ,"is empty" ~: False ~=? sentenceEnd ""
                    ,"doesn't end" ~: False ~=? sentenceEnd "arf\t\tsqueak"]
propSentenceEnd s@('.':'\t':'\t':_) = sentenceEnd s == True
propSentenceEnd s = sentenceEnd s == False
propWordLength l = all ((>1) . length . words) l ==>
  length l == (length $ words $ putTagsOnOneLine l)
offset _ [] = 0
offset f ls | f (last ls) = 0
            | otherwise = 1
propFilterTag ls = all ((>1) . length . words) ls ==>
  length ls - countBy tag ls + offset sentenceEnd ls
  == (length $ ConvertTagsToTxt.convertPos ls)
propGroupBy ls = all ((>1) . length . words) ls ==>
  countBy sentenceEnd ls + offset sentenceEnd ls
  == length (ConvertTagsToTxt.convertPos ls)
propAllWordLength ls = all ((>1) . length . words) ls ==>
  length ls == sum (map (length . words) (ConvertTagsToTxt.convertPos ls))

propSentenceCount ls =
  count "." ls + offset (==".") ls == length (convertWord ls)
propTotalWords ls = not (any restrict ls) ==>
  length ls == sum (map (length . words) $ convertWord ls)
  where restrict line = null line || elem ' ' line

testConllise = [["1","one","_","foo","foo","_","0","ROOT","_","_"]
                ~=? conllise 1 ["one","foo"]
               ,["\"oh no\"","one","_","foo","foo","_","0","ROOT","_","_"]
                ~=? conllise "oh no" ["one","foo"]]
testAddColumns =
  ["1\tone\t_\tfoo\tfoo\t_\t0\tROOT\t_\t_" ~=? addColumns 1 "one foo"
  ,"\"no\"\tone\t_\tfoo\tfoo\t_\t0\tROOT\t_\t_" ~=? addColumns "no" "one foo"]
main = do
  runTestTT $ TestList $ testIsTag
    ++ testIsSentenceEnd
    ++ testConllise
    ++ testAddColumns
  runTests "Tag conversions" TestOptions {no_of_tests = 100,
                                          length_of_tests = 1,
                                          debug_tests = False }
           [run propWordLength
           ,run propTag
           ,run propSentenceEnd
           ,run propFilterTag
           ,run propGroupBy
           ,run propAllWordLength
           ,run propSentenceCount
           ,run propTotalWords]
           -- , run propParens]

