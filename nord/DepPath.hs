import Util (withFileLines, (&))
import System (getArgs)
main = getArgs >>= head & flip withFileLines f >>= putStr
  where f = undefined
