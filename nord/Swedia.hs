import Data.List (isPrefixOf, find, intercalate)
import Data.List.Split (split, dropDelims, whenElt, dropBlanks)
import Data.Maybe (fromJust)
import Util ((|>), (&), collapse, withFileLines, splitBy)
import Directory (getDirectoryContents)
import qualified Data.Map as Map
import qualified Consts
import Char (isSpace)

newline ('*':_) = True
newline _ = False
visible ('.':_) = False
visible _  = True
between before after = dropWhile (/=before) & tail & takeWhile (/=after)
trimsplit = split $ dropBlanks $ dropDelims $ whenElt isSpace

readSwedia path filename = withFileLines splitter (path++filename)
  where splitter = dropWhile (not . newline) &
                   splitBy newline &
                   filter (head & (isPrefixOf "*INT") & not) &
                   map (intercalate " " & between ':' '\NAK' & trimsplit)
groupedSites sites paths = collapse (filter visible paths) keymap
  where keymap f = fromJust $ find (`isPrefixOf` f) sites
getGroupedSites path sites =
  getDirectoryContents path >>= groupedSites sites & return
groupedRegions paths = Map.map (groupedSites paths & Map.elems & concat)
extractTnt path sites =
 getGroupedSites path sites >>= Map.assocs & mapM_ (\ (region,files) ->
    mapM (readSwedia path) (reverse files) >>=
    concat & concat & intercalate "\n" &
    writeFile (region ++ ".t"))
-- (reverse files) is to remain compatible with Python output
main = extractTnt Consts.swpath Consts.swediaSites >>= print
