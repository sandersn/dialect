import Util
import Sexp
import Text.Regex.Posix ((=~))
main = interactFiles (withFileLines depPos) format
depPos = filter (/= "(())")
         & filter (not . (=~ "\\([^ ()]+\\)"))
         & concatMap (tail & tail & init & runsexp & wordPairs)
wordPairs (Node pos [Node word []]) = [(pos, word)]
wordPairs (Node _ kids) = concatMap wordPairs kids
format (pos, word) = word ++ "\t\t\t" ++ pos
