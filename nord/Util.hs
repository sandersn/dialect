module Util where
import Text.XML.HaXml (tag, (/>), txt, elm, attr, xmlParse, verbatim, showattr,
                      literal, find)
import Text.XML.HaXml.Types
import Data.List (group, sort, foldl')
import Data.List.Split (split, dropInitBlank, dropFinalBlank, keepDelimsR, keepDelimsL, whenElt)
import qualified Data.Map as Map
import Maybe (fromMaybe)
import System (getArgs)
import Control.Arrow ((&&&))
import Control.Monad ((>=>))
{--- lst ---}
countBy f = filter f & length
count x = filter (==x) & length
histogram :: (Ord a) => [a] -> Map.Map a Int
histogram l = foldl' (\ m x -> Map.insertWith' (+) x 1 m) Map.empty l
collapse :: (Ord k) => (a -> k) -> [a] -> Map.Map k [a]
collapse f l = Map.fromListWith (++) $ zip (map f l) (map list l)
-- this version might be faster because it's strict
collapse' f l = foldl' (\ m x -> Map.insertWith' (++) (f x) [x] m) Map.empty l
window n l = win l (length l)
  where win l len | n > len = []
                  | otherwise = take n l : win (tail l) (len - 1)
between before after = dropWhile (/=before) & tail & takeWhile (/=after)
replace _ _ [] = []
replace src dst (x:xs) = (if src == x then dst else x) : replace src dst xs
splitByR f = split $ dropFinalBlank $ keepDelimsR $ whenElt f
splitByL f = split $ dropInitBlank $ dropFinalBlank $ keepDelimsL $ whenElt f
splitsAt n [] = []
splitsAt n l = fore : splitsAt n aft where (fore,aft) = splitAt n l
list = (:[])
{--- fs ---}
withFile f = readFile >=> f & return -- see also System.IO
withFileLines f = readFile >=> lines & f & return
interactFiles read show = mapM_ (read >=> mapM_ (show & putStrLn)) =<< getArgs
interactTargets targets f = do
  [file, target] <- getArgs
  let t = fromMaybe (error $ target
                             ++ " is not a valid target in the list: "
                             ++ show (map fst targets))
                    (lookup target targets)
  f t file >>= mapM_ putStrLn
{--- fnc (F# esque) ---}
infixl 9 &
infixl 0 |>
f & g = g . f -- also called >>> in Control.Arrow
x |> f = f x
{--- xml and encoding. Ugh --}
tagpath = foldr1 (/>) . map tag
attr' attribute c@(CElem (Elem _ as _)) = verbatim$head$show' attribute
  where show' attribute = literal (value (lookfor attribute as)) c
        lookfor x = fromMaybe (error "missing attr") . lookup x
        value (AttValue list) = concatMap attr2str list
        attr2str (Left x) = x
        attr2str (Right (RefEntity entityref)) = "&" ++ entityref ++ ";"
        attr2str (Right (RefChar charref)) = "&#" ++ show charref ++ ";"
getContent (Document _ _ e _) = CElem e
