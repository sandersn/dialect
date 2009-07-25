import Util ((&), (|>), withFileLines, count)
import System (getArgs)
import Random (randomRs, getStdGen, StdGen)
import Data.List.Split (splitOn)
import Data.Maybe (fromMaybe)
import qualified Data.Map as Map
import Control.Monad (liftM2)
import Control.Arrow (second)
-- TODO: Switch to arrays, learn how to profile, learn how to write unit tests
main = do
  (file1:file2:_) <- getArgs
  count <- liftM2 analyse (readDat file1) (readDat file2)
  count >>= print
readDat = withFileLines (tail & splitOn ["***"]) -- should produce arrays
r = map (abs . uncurry (-)) & sum
analyse :: [[String]] -> [[String]] -> IO Int
analyse r1 r2 =
  return . sig r1 r2 . liftR2 cmp (sample r1) (sample r2) =<< getStdGen
sample l = second concat . nChoices 1000 l
nChoices n l gen = (,) gen . map (l!!) . take n $ randomRs (0, length l - 1) gen
sig :: [[String]] -> [[String]] -> (StdGen,[(Double,Double)]) -> Int
sig r1 r2 (gen,base) =
  countBy (> r base) . map (r . snd) $ take 100 $ iterate shuffler (gen,[])
  where shuffler = fst & liftR2 cmp (sample (r1++r2)) (sample (r1++r2))
cmp :: [String] -> [String] -> [(Double, Double)]
cmp r1 r2 = map ((!!5) . iterate norm . finder) types2
  where types1 = count r1; types2 = count r2
        lhs = Map.fromList types1
        finder (f,n) = (fromIntegral (lookupDefault f 0 lhs),fromIntegral n)
        norm (ai,bi) = (ci * fa / f, ci * fb / f)
          where ci = ai + bi
                fa = ai / (fromIntegral $ length types1)
                fb = bi / (fromIntegral $ length types2)
                f = fa + fb
{--- utilities ---}
liftR2 f g h gen = let (gen',res) = g gen in
                   let (gen'',res') = h gen' in
                   (gen'',f res res')
lookupDefault k def = Map.lookup k & fromMaybe def
countBy f = length . filter f
{--- DEBUG ---}
test = splitOn "\n" "Morgoth\na\nb\n***\na\nc"
