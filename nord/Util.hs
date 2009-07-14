module Util where
import qualified Data.ByteString.Lazy.Char8 as B
import Codec.Text.IConv (convert)
import Text.XML.HaXml (tag, (/>), txt, elm, attr, xmlParse, verbatim, showattr,
                      literal, find)
import Text.XML.HaXml.Types
import Data.List (group,sort)
import Maybe (fromMaybe)
import System (getArgs)
import Control.Arrow ((&&&))
{--- lst ---}
count :: (Ord a) => [a] -> [(a, Int)]
count = map (head &&& length) . group . sort
window n l = win l (length l)
  where win l len | n > len = []
                  | otherwise = take n l : win (tail l) (len - 1)
replace _ _ [] = []
replace src dst (x:xs) = (if src == x then dst else x) : replace src dst xs
-- if you need Pythonesque groupBy, get Data.List.Split from Hackage and do:
-- groupBy f = split $ dropFinalBlank $ keepDelimsR $ whenElt f
{--- fs ---}
withFile filename f = return . f =<< readFile filename -- see also System.IO
withFileLines filename f = return . f . lines =<< readFile filename
multiFilePrinter read show =
    getArgs >>= mapM read >>= concat & mapM_ (show & putStrLn)
{--- fnc (F# esque) ---}
f & g = g . f -- also called >>> in Control.Arrow
x |> f = f x
{--- xml and encoding. Ugh --}
tagpath = foldr1 (/>) . map tag
utf8FromLatin1 = B.pack & convert "LATIN1" "UTF-8" & B.unpack
attr' attribute c@(CElem (Elem _ as _)) = verbatim$head$show' attribute
    where show' attribute = literal (value (lookfor attribute as)) c
          lookfor x = fromMaybe (error "missing attr") . lookup x
          value (AttValue list) = concatMap attr2str list
          attr2str (Left x) = x
          attr2str (Right (RefEntity entityref)) = "&" ++ entityref ++ ";"
          attr2str (Right (RefChar charref)) = "&#" ++ show charref ++ ";"
getContent (Document _ _ e _) = CElem e
