import Text.XML.HaXml (xmlParse)
import Util
getTerminals = map (tagpath ["s", "graph", "terminals", "t"]) .
               tagpath ["corpus", "body", "s"]
getAttrs = concatMap (((".", "IP") :) . map pair)
    where pair elem = (utf8FromLatin1 $ attr' "word" elem,
                       replace ' ' '_' $ attr' "pos" elem)
readPOS filename = withFile filename $
    xmlParse filename & getContent & getTerminals & getAttrs
main = multiFilePrinter readPOS (\ (word,pos) -> word ++ " " ++ pos)
