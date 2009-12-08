import Data.List (isPrefixOf, find, intercalate)
import Data.List.Split (splitOn)
import Data.Maybe (fromJust)
import Util ((|>), (&), collapse, withFileLines, splitBy)
import Directory (getDirectoryContents)
import qualified Data.Map as Map

newline ('*':_) = True
newline _ = False
visible ('.':_) = False
visible _  = True
between before after = dropWhile (/=before) & tail & takeWhile (/=after)
-- TODO: Is this  UTF-8? I'm not sure how to make sure
readSwedia path filename = withFileLines splitter (path++filename)
  where splitter = dropWhile (not . newline) &
                   splitBy newline &
                   filter (head & (`isPrefixOf` "*INT:") & not) &
                   map (intercalate " " & between ':' '%' & splitOn " ")
groupedSites paths sites = collapse (filter visible paths)
                                   (\ f -> fromJust $ find (isPrefixOf f) sites)
getGroupedSites path sites =
  getDirectoryContents path >>= groupedSites sites & return
groupedRegions paths = Map.map (groupedSites paths & Map.elems & concat)
extractTnt path sites =
 getGroupedSites path sites >>= Map.assocs & mapM_ (\ (region,files) ->
    mapM (readSwedia path) files >>=
    concat & concat & filter (/="\15") & intercalate "\n" &
    writeFile (region ++ ".t"))
