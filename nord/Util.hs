module Util where
import qualified Data.ByteString.Lazy.Char8 as B
import Codec.Text.IConv (convert)
import Text.XML.HaXml (tag, (/>), txt, elm, attr, xmlParse, verbatim, showattr,
                      literal, find)
import Text.XML.HaXml.Types
import Maybe (fromMaybe)
import System (getArgs)
replace _ _ [] = []
replace src dst (x:xs) = (if src == x then dst else x) : replace src dst xs
-- if you need Pythonesque groupBy, get Data.List.Split from Hackage and do:
-- groupBy f = split $ dropFinalBlank $ keepDelimsR $ whenElt f
withFile filename f = return . f =<< readFile filename -- see also System.IO
withFileLines filename f = return . f . lines =<< readFile filename
multiFilePrinter read show =
    getArgs >>= mapM read >>= concat & mapM_ (show & putStrLn)
-- F# esque --
f & g = g . f -- also called >>> in Control.Arrow
x |> f = f x
--- XML and encoding. Ugh --
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
