module ConvertMaltToFeature where
import Util (withFileLines, (&), (|>), groupBy, interactTargets, list)
import Data.Map ((!), fromList, size)
import Data.List (intercalate)
import Data.List.Split (splitOn,endBy)
import System (getArgs)
import Talbanken (FlatNode(..))
deconllise i line@[id, w, _, pos, _, _, parentId, arc, _, _] =
  (read id, FlatNode (line !! i) w (read id) [read parentId])

main = interactTargets [("node",deconllise 3), ("arc",deconllise 7)] processor
  where processor target name = withFileLines (process target name) name
process target name = endBy [""] & map deps & intercalate ["***"] & (name:)
  where deps = buildMap & buildRelations
        buildMap = map (splitOn "\t" & target) & fromList
buildRelations flat =
  map (build & intercalate "-") [1..fromIntegral (size flat)]
  where build 0 = []
        build i = cat w : build parentId
          where w @ FlatNode { kids = [parentId] } = flat ! i
