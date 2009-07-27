import Util ((&), (|>), withFileLines, count)
import System (getArgs)
import Random (randomR, getStdGen, StdGen)
import Data.List.Split (splitOn)
import Data.List (foldl')
import Data.Maybe (fromMaybe)
import qualified Data.Map as Map
import Control.Monad (liftM, liftM2)
import Control.Arrow (first, second)
-- TODO: Switch to arrays, learn how to profile, learn how to write unit tests
main = testmain
testmain = do
  strings1 <- liftM lines (readFile "test1.txt")
  strings2 <- liftM lines (readFile "test2.txt")
  (putStr $ show $ r $ cmp strings1 strings2) >> (putStrLn " bork bork bork")
genmain = do
  [filename] <- getArgs
  ss <- readDat filename
  getStdGen >>= (sample ss) & fst & return >>= mapM_ putStrLn
realmain = do
  (file1:file2:_) <- getArgs
  p <- liftM2 analyse (readDat file1) (readDat file2)
  p >>= print
readDat = withFileLines (tail & splitOn ["***"]) -- should produce arrays
r = map (abs . uncurry (-)) & sum
analyse :: [[String]] -> [[String]] -> IO Int
analyse r1 r2 =
  return . sig r1 r2 . liftR2 cmp (sample r1) (sample r2) =<< getStdGen
sample :: [[a]] -> StdGen -> ([a],StdGen)
sample l = first concat . nChoices 1000 l
nChoices n l = first (map (l!!) . take n) . genRandomRs (0, length l - 1)
genRandomRs bounds = liftR2 (:) (randomR bounds) (genRandomRs bounds)
sig :: [[String]] -> [[String]] -> ([(Double,Double)],StdGen) -> Int
sig r1 r2 (base,gen) =
  countBy (> r base) . map (r . fst) $ take 100 $ iterate shuffler ([],gen)
  where shuffler (_,gen) = liftR2 cmp (sample (r1++r2)) (sample (r1++r2)) gen
cmp :: [String] -> [String] -> [(Double, Double)]
cmp r1 r2 = map ((!!5) . iterate norm . finder) (Map.toList types2)
  where types1 = histogram r1; types2 = histogram r2
        finder (f,n) = (fromIntegral $ Map.findWithDefault 0 f types1,
                        fromIntegral n)
        norm (ai,bi) = (ci * fa / f, ci * fb / f)
          where ci = ai + bi
                fa = ai / (fromIntegral $ Map.size types1)
                fb = bi / (fromIntegral $ Map.size types2)
                f = fa + fb
histogram l = foldr (\ x m -> Map.insertWith (+) x 1 m) Map.empty l
{--- utilities ---}
liftR2 f g h gen = let (res,gen') = g gen in
                    let (res',gen'') = h gen' in
                    (f res res', gen'')
countBy f = length . filter f
{--- DEBUG ---}
test = splitOn "\n" "Morgoth\na\nb\n***\na\nc"
