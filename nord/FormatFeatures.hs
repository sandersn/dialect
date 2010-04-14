import Util
import System
import Text.Printf (printf)
import Control.Arrow (second)
import Data.List.Split (chunk)
fig = "\\begin{figure}\n\
      \\\setlength{\\unitlength}{1pt}\n\
      \\\begin{picture}(400,140)\n\
      \\\linethickness{2mm}\n\
      \%s\
      \\\end{picture}\n\
      \\\caption{%s %s}\n\
      \\\end{figure}\n\n"
main = interactFiles (withFileLines parse) format
  where tmp (s,_,_,_) = s
parse = chunk 13 & map struct
struct (from:to:numbers) = (from,to,take 5 ns++drop 6 ns)
 where ns' = map (words & parse) numbers
       ns = scale largest ns'
       parse [n] = ("", read n :: Double)
       parse [f,n] = (f, read n)
       largest = maximum (map (abs . snd) ns')
       scale largest = map (second scale')
       scale' n = n / largest * 180.0
format :: (String,String,[(String,Double)]) -> String
format (from,to,ns) = printf fig (fmt ns) from to
  where fmt l = unlines (map formatLine (zip [0..] l))
formatLine :: (Integer,(String,Double)) -> String
formatLine (i,(pos,n)) =
  printf "\\put(%d,%d){\\line(%s,0){%f}}\n\
          \\\put(190,%d){%s}"
    (if n < 0 then 180 else 250 :: Integer)
    (110 - i * 11)
    (if n < 0 then "-1" else "1")
    (abs n)
    (107 - i * 11)
    pos
