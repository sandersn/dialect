module Swedia where
import Data.List (isPrefixOf, isSuffixOf, find, intercalate)
import Data.List.Split (split, dropDelims, whenElt, dropBlanks)
import Data.Maybe (fromJust)
import Util
import Directory (getDirectoryContents)
import qualified Data.Map as Map
import qualified Consts
import Char (isSpace)
import Control.Monad (liftM2)

stoplist = ["#", "[/-]", "##", "[/]", "eh", "+...", "###"
           , "xxx", "[//]", "[?]", "+/."]
stutterlist = [">[/]", ">[//]", ">[/-]", ">[?]", ">[///]", ">"]

main = extractTnt Consts.swpath Consts.swediaSites >>= print
extractTnt path sites =
 getGroupedSites path sites >>= Map.assocs & mapM_ (\ (region,files) ->
    mapM (readSwedia path) (reverse files) >>=
    concat & concat & intercalate "\n" &
    writeFile (region ++ ".t"))
-- (reverse files) is to remain compatible with Python output
getGroupedSites path sites =
  getDirectoryContents path >>= groupedSites sites & return
  where groupedSites sites paths = collapse keymap (filter glossed paths)
        keymap f = fromJust $ find (`isPrefixOf` f) sites
        glossed filename = dropWhile (/='.') filename == ".cha"
readSwedia path filename = withFileLines splitter (path++filename)
  where splitter = dropWhile (not . newline) &
                   splitBy newline &
                   filter (head & (isPrefixOf "*INT") & not) &
                   map (unwords & between ':' '\NAK' & trimsplit & deStutter
                        & filter (not . (`elem` stoplist)) & map decomma)
        decomma w | last w == ',' = init w
                  | otherwise = w
        newline ('*':_) = True
        newline _ = False
endStutter w = any (`isSuffixOf` w) (stutterlist ++ map (++",") stutterlist)
deStutter ws =
  case break ((=='<') . head) ws of
    (ws,[]) -> ws
    (ws,aft) -> ws ++ deStutter ((dropWhile (not . endStutter) aft) |> tail)
{-- utils --}
trimsplit = split $ dropBlanks $ dropDelims $ whenElt isSpace
f <&&> g = liftM2 (&&) f g
f <||> g = liftM2 (||) f g
