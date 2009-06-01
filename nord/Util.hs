module Util where
replace _ _ [] = []
replace src dst (x:xs) = (if src == x then dst else x) : replace src dst xs
-- if you need Pythonesque groupBy, get Data.List.Split from Hackage and do:
-- groupBy f = split $ dropFinalBlank $ keepDelimsR $ whenElt f
withFile filename f = return . f =<< readFile filename -- see also System.IO
withFileLines filename f = return . f . lines =<< readFile filename
f & g = g . f -- also called >>> in Control.Arrow
