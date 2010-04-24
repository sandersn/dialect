import Util
import System
import Text.Printf (printf)
import Control.Arrow (second)
import Data.List.Split (chunk)
-- latex clusterA-clusterD-feat-5-1000-r-trigram-ratio.txt && dvips -Ppdf clusterA-clusterD-feat-5-1000-r-trigram-ratio.dvi && ps2pdf clusterA-clusterD-feat-5-1000-r-trigram-ratio.ps && open clusterA-clusterD-feat-5-1000-r-trigram-ratio.pdf
fig = "\\documentclass{article}\n\
       \\\usepackage[dvips]{geometry}\n\
       \\\usepackage{pstricks}\n\
       \\\geometry{papersize={85mm,45mm},total={85mm,45mm}}\n\
       \\\addtolength{\\topmargin}{-1.4in}\n\
       \\\addtolength{\\textheight}{3.6in}\n\
       \\\setlength{\\parindent}{0cm}\n\
       \\\pagestyle{empty}\n\
       \\\begin{document}\n\
       \\\thispagestyle{empty}\n\
       \\\definecolor{LeftColor}{hsb}{0.9,0.87,1}\n\
       \\\definecolor{RightColor}{hsb}{1.0,0.86,1}\n\
       \\\psset{linewidth=4pt}\n\
       \\\begin{pspicture}(%f,8.0)\n\
       \ %s\n\
       \\\end{pspicture}\n\
       \%%\\setlength{\\unitlength}{1pt}\n\
       \\\end{document}\n\n"
maxwidth = 3.0
maxheight = 3.20
offset = 3.0
main = do
  [f] <- getArgs
  readFile f >>= lines & parse & return >>= mapM_ (output f)
output f (from,to,ns) = format ns |> writeFile (printf "%s-%s-%s" from to f)
parse = chunk 13 & map struct
struct (from:to:numbers) = (shorten from,shorten to,take 5 ns++drop 6 ns)
 where ns' = map (words & parse) numbers
       ns = scale largest ns'
       parse [n] = ("", read n :: Double)
       parse [f,n] = (f, read n)
       largest = maximum (map (abs . snd) ns')
       scale largest = map (second scale')
       scale' n = n / largest * maxwidth
       shorten = takeWhile (/='-')
format :: [(String,Double)] -> String
format ns = printf fig maxheight (fmt ns)
  where fmt l = unlines (map formatLine (zip (map fromIntegral [0..]) l))
formatLine :: (Double,(String,Double)) -> String
formatLine (i,(pos,n)) =
  printf "  \\uput{0.2}[0](0,%f){%s}\n\
         \  \\psline[linecolor=%s](%f,%f)(%f,%f)\n\
         \  \\uput{0.2}[0](7,%f){%.2f}\n"
    height pos
    (if n < 0 then "RightColor" else "LeftColor")
    offset height (offset + abs n) height height n
  where height = maxheight - i * (maxheight / 10)
    {-(if n < 0 then 180 else 250 :: Integer)
    (110 - i * 11)
    (if n < 0 then "-1" else "1")
    (abs n)
    (107 - i * 11)
    pos
"\\put(%d,%d){\\line(%s,0){%f}}\n\
          \\\put(190,%d){%s}" -}
