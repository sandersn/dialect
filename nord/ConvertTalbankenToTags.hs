module ConvertTalbankenToTags where
import Text.XML.HaXml (xmlParse)
import Codec.Binary.UTF8.String (encodeString)
import Util
getTerminals = map (tagpath ["s", "graph", "terminals", "t"]) .
               tagpath ["corpus", "body", "s"]
getAttrs = concatMap (((".", "IP") :) . map pair)
  where pair elem = (encodeString $ attr' "word" elem,
                     replace ' ' '_' $ attr' "pos" elem)
readPOS filename = withFile (posOfXml filename) filename
posOfXml filename = xmlParse filename & getContent & getTerminals & getAttrs
main = interactFiles readPOS (\ (word,pos) -> word ++ " " ++ pos)
