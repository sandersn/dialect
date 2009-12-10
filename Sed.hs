module Sed where
import Text.Regex.Posix
import Text.CSV
import Char
import qualified Data.Map as Dct
import Data.List
import Data.Ord
import qualified Lev
--- util ---
(&) = flip (.)
dctCollapse xs k v = Dct.fromAscListWith
                       (++)
                       (sortBy (comparing fst) [(k x, [v x]) | x <- xs])
listExtract ns xs = extract ns xs 0
    where extract [] _ _ = []
          extract (n:ns) xs i =
              xs !! (n - i) : extract ns (drop (n - i) xs) n
kross (xs,ys) = do x <- xs; y <- ys; return (x,y)
both f (x,y) = (f x, f y)
pairs [] = []
pairs (x:xs) = [(x,y) | y <- xs] ++ pairs xs
average l = sum l / fromIntegral (length l)
--- read CSV ---
segment = head & dropWhile isLower & segmentName
    where segmentName s = seg++n where (seg,n,_) =
                                           s =~ "[0-9]" :: (String,String,String)
features (title:ns) = (feature title, map read ns)
    where feature s = feat where (_,_,feat) =
                                     s =~ "[0-9]" :: (String,String,String)
groupWords csv = Dct.map (fillsegments . phones) words
    where words = dctCollapse (tail csv) (head & takeWhile isLower) id
          fillsegments = Dct.mapWithKey makesegment
          phones l = Dct.map Dct.fromList (dctCollapse l segment features)
makesegment typ d =
    let size = length . head . Dct.elems $ d
    in d `Dct.union` Dct.map (replicate size) (featdict Dct.! init typ)
groupRegions regions words = Dct.map outermost regions
    where outermost range = Dct.map inner words
              where inner = Dct.map (Dct.map (listExtract (map ((-) 2) range)))
groupSedInGor = do
  csv <- parseCSVFromFile "sed.csv"
  case csv of
    Left err -> error ("oh no:" ++ show err)
    Right rows -> return $ groupRegions regions $ groupWords $ transpose rows
--- analysis ---
flatten = map (map Dct.elems . Dct.elems) . Dct.elems
analyse sed = Dct.fromList . zip edges . map (sedDistance avgregions) $ regions
    where edges = pairs (Dct.keys sed)
          regions = pairs (flatten sed)
          avgregions = average (map sedAvgTotal regions)
featureSub seg1 seg2 = fromIntegral (Dct.size(seg1 `symmetric_difference` seg2))
                       + sum (map abs (Dct.elems (Dct.intersectionWith (-) seg1 seg2)))
  where symmetric_difference d e = Dct.union (e `Dct.difference` d)
                                             (d `Dct.difference` e)
sedDistance avg = sum . map (sedLevenshtein avg) . uncurry zip
transposeWord word = transpose (map transposeSegment word)
    where transposeSegment seg = map (Dct.fromList . zip (Dct.keys seg))
                                     (transpose (Dct.elems seg))
sedLevenshtein a = average . map (levenshtein a) . kross . both transposeWord
levenshtein a (w1,w2) =
    head $ Lev._levenshtein w1 w2 a (const a, const a, featureSub)
sedAvg :: (Ord k, Fractional a) => ([Dct.Map k [a]], [Dct.Map k [a]]) -> a
sedAvg = both (concat . transposeWord) & kross & map (uncurry featureSub) & average
sedAvgTotal (region1,region2) = average (map sedAvg (zip region1 region2)) / 2.0
--- data ---
featdict = Dct.fromList [("C", Dct.fromList [("GL",0.0), ("V",0.0), ("H",0.0),
                                             ("PV",0.0), ("L",0.0)]),
                         ("V", Dct.fromList [("B",1.0), ("H",1.0),
                                             ("L",1.0), ("R",1.0)]),
                         ("R", Dct.fromList [("MN",1.5), ("PL",1.0)]),
                         ("MULT", Dct.fromList [("MULT", 1.0)]),
                         ("VC", Dct.empty)]
regions :: Dct.Map String [Int]
regions = Dct.fromList [("ne", [2..11]++[17..23]),
                        ("nw", [11..17]++[23..41]++[77..83]),
                        ("yk", [41..75]),
                        -- ++[75..77] (Isle of Man isn't on GOR map)
                        ("wm", [112..126]++[140..157]),
                        ("em", [83..112]++[126..140]++[157..172]),
                        ("ee", [172..191]++[217..238]),
                        ("se", [206..217]++[262..279]++[302..315]),
                        ("sw", [193..206]++[240..262]++[279..302]),
                        ("ld", [238..240])]
test = [["", "applV1H", "applV1L", "applC1GL", "applV2", "catcV1H", "askMULT0MULT", "askV1H", "askV1B"],
        ["", "1.0", "2.0", "3.0", "0.0", "3.0", "1.0", "2.0", "2.0"],
        ["", "1.0", "2.0", "3.0", "0.0", "3.0", "1.0", "2.0", "2.0"],
        ["", "1.0", "2.0", "3.0", "0.0", "3.0", "1.0", "2.0", "2.0"],
        ["", "1.0", "2.0", "3.0", "0.0", "3.0", "1.0", "2.0", "2.0"],
        ["", "1.0", "2.0", "3.0", "0.0", "3.0", "1.0", "2.0", "2.0"],
        ["", "1.0", "2.0", "3.0", "0.0", "3.0", "1.0", "2.0", "2.0"]]
