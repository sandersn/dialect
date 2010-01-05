module DepPath where
import Util (withFileLines, (&), (|>), groupBy, argsFilePrinter, list)
import Data.Map ((!), fromList, size)
import Data.List (intercalate, intersperse)
import Data.List.Split (splitOn,endBy)
import System (getArgs)
import Talbanken (FlatNode(..))
main = argsFilePrinter namedProcessor Prelude.id
  where namedProcessor name = withFileLines ((name:) . process) name
process = endBy [""] & map deps & intersperse "***"
deps = buildMap & buildRelations & intercalate "\n"
buildMap = map (splitOn "\t" & deconllise) & fromList
deconllise [id, w, _, pos, _, _, parentId, _, _, _] =
  (read id, FlatNode pos w (read id) [read parentId])
buildRelations flat =
  map (build & intercalate "-") [1..fromIntegral (size flat)]
  where build 0 = []
        build i = cat w : build parentId
          where w @ FlatNode { kids = [parentId] } = flat ! i
