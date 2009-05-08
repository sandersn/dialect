module Util where
replace _ _ [] = []
replace src dst (x:xs) = (if src == x then dst else x) : replace src dst xs
