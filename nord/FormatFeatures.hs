import Util
import System
import Text.Printf (printf)
import Control.Arrow (second)
import Data.List.Split (chunk)
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
       \\\definecolor{clusterA}{hsb}{0.627,0.98,1}\n\
       \\\definecolor{clusterB}{hsb}{0.98,1,0.96}\n\
       \\\definecolor{clusterC}{hsb}{0.16,1,1}\n\
       \\\definecolor{clusterD}{hsb}{0.5,0.94,1}\n\
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
output f s@(from,to,_) = format s |> writeFile (printf "%s-%s-%s" to from f)
parse = chunk 13 & map struct
struct (from:to:numbers) = (shorten from,shorten to,take 5 ns++drop 6 ns)
 where shorten = takeWhile (/='-')
       ns = map (words & parse) numbers |> scale
       parse [n] = ("", read n :: Double)
       parse [f,n] = (f, read n)
       scale l = map (second ((/ largest l) . (* maxwidth))) l
       largest = maximum . map (abs . snd)
format :: (String,String,[(String,Double)]) -> String
format (from,to,ns) = printf fig maxheight (fmt ns)
  where fmt l =
          unlines (map (formatLine from to) (zip (map fromIntegral [0..]) l))
formatLine :: String -> String -> (Double,(String,Double)) -> String
formatLine from to (i,(pos,n)) =
  printf "  \\uput{0.2}[0](0,%f){%s}\n\
         \  \\psline[linecolor=%s](%f,%f)(%f,%f)\n\
         \  \\uput{0.2}[0](7,%f){%.2f}\n"
    height pos
    (if n < 0 then to else from)
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
