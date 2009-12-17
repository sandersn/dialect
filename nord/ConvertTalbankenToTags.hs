import Text.XML.HaXml (xmlParse)
import Codec.Binary.UTF8.String (encodeString)
import Util
getTerminals = map (tagpath ["s", "graph", "terminals", "t"]) .
               tagpath ["corpus", "body", "s"]
getAttrs = concatMap (((".", "IP") :) . map pair)
  where pair elem = (encodeString $ attr' "word" elem,
                     replace ' ' '_' $ attr' "pos" elem)
readPOS filename = withFile posOfXml filename
  where posOfXml = xmlParse filename & getContent & getTerminals & getAttrs
main = argsFilePrinter readPOS (\ (word,pos) -> word ++ " " ++ pos)
