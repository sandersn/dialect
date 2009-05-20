import Text.XML.HaXml (tag, (/>), txt, elm, attr, xmlParse, verbatim, showattr,
                      literal, find)
import Text.XML.HaXml.Types
import Data.List (intercalate, intersperse)
import Maybe (fromMaybe)
import System (getArgs)
import Util
attr' attribute c@(CElem (Elem _ as _)) = verbatim$head$show' attribute
    where show' attribute = literal (value (lookfor attribute as)) c
          lookfor x = fromMaybe (error "missing attr") . lookup x
          value (AttValue list) = concatMap attr2str list
          attr2str (Left x) = x
          attr2str (Right (RefEntity entityref)) = "&" ++ entityref ++ ";"
          attr2str (Right (RefChar charref)) = "&#" ++ show charref ++ ";"
getContent (Document _ _ e _) = CElem e
getTerminals xml = map (tag "s" /> tag "graph" /> tag "terminals" /> tag "t")
                       (tag "corpus" /> tag "body" /> tag "s" $ xml)
getAttrs = concatMap (((".", ".") :) . map pair)
    where pair elem = (attr' "word" elem, replace ' ' '_' $ attr' "pos" elem)
readPOS filename = return.getAttrs.getTerminals.getContent.xmlParse filename
             =<< readFile filename
main = mapM_ (putStrLn . join) . concat =<< mapM readPOS =<< System.getArgs
    where join (word,pos) = word ++ ' ' : pos
