import Util (withFileLines, (&), (|>), groupBy)
import qualified Data.Map as Map
import Data.List (intercalate)
import Data.List.Split (splitOn,endBy)
import System (getArgs)
import Talbanken (FlatNode(..))
main = getArgs >>= head & withFileLines f >>= putStr
  where f = endBy [""] & map deps & intercalate "\n***\n"
deps = buildMap & buildRelations & intercalate "\n"
buildMap = map (splitOn "\t" & deconllise) & Map.fromList
deconllise [id, w, _, pos, _, _, parentId, relation, _, _] =
  (read id, FlatNode pos w (read id) [read parentId])
buildRelations flat = map (build & intercalate "-")
                          [1..fromIntegral (Map.size flat)]
  where build 0 = []
        build i = cat w : (build . head . kids $ w)
          where w = flat Map.! i
{--- DEBUG ---}
s = lines "1\tmen,\t_\tNN__SS\tNN__SS\t_\t12\tSS\t_\t_\n2\teh\t_\t++OC\t++OC\t_\t0\tROOT\t_\t_\n3\t###\t_\tNN__SS\tNN__SS\t_\t0\tROOT\t_\t_\n4\tdet\t_\tPODP\tPODP\t_\t0\tROOT\t_\t_\n5\tgick\t_\tVVPT\tVVPT\t_\t0\tROOT\t_\t_\n6\tratt\t_\tABZA\tABZA\t_\t0\tROOT\t_\t_\n7\tbra\t_\tABZA\tABZA\t_\t0\tROOT\t_\t_\n8\tdet\t_\tPODP\tPODP\t_\t10\tSS\t_\t_\n9\tdaor\t_\tID\tID\t_\t8\tHD\t_\t_\n10\t#\t_\tNNDD\tNNDD\t_\t0\tROOT\t_\t_\n11\tmed\t_\tPR\tPR\t_\t10\tOA\t_\t_\n12\tskolgangen\t_\tNNDDSS\tNNDDSS\t_\t0\tROOT\t_\t_\n13\t.\t_\tIP\tIP\t_\t12\tIP\t_\t_\n\n1\tvi\t_\tPOPPHH\tPOPPHH\t_\t0\tROOT\t_\t_\n2\thade\t_\tHVPT\tHVPT\t_\t0\tROOT\t_\t_\n3\tmiddagsrast\t_\tABZA\tABZA\t_\t0\tROOT\t_\t_\n4\t.\t_\t.\t.\t_\t0\tROOT\t_\t_\n"
sents = endBy [""] s
[sent1, sent2] = sents
