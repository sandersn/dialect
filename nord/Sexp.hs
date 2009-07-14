module Sexp (Tree(..), runsexp) where
data Tree a = Leaf a | Tree a [Tree a] deriving (Show,Eq)
main = mapM_ (print . runsexp) ["(foo bar baz)"
                               , "foo"
                               , "(foo)"
                               , "(foo bar )"
                               , "(foo (bar))"
                               , "(foo (bar (baz bum) qux) quim)"]
runsexp s = sexp s [[]] ""
leaf = Leaf . reverse
sexp :: String -> [[Tree String]] -> String -> Tree String
sexp "()" _ _ = Leaf "()" -- special case (remember to handle this elsewhere)
sexp "" [[stack]] "" = stack
sexp "" [[]] a = leaf a -- special case
sexp "" _ _ = error "More than one thing left on the stack"
sexp ('(':s) stack "" = sexp s ([]:stack) ""
sexp ('(':s) (kids:stack) a = sexp s ([]:(leaf a:kids):stack) ""
sexp (')':s) (kids:kids':stack) a = sexp s ((Tree head sdik:kids'):stack) ""
    where Leaf head:sdik = reverse (if null a then kids else leaf a:kids)
sexp (' ':s) stack "" = sexp s stack ""
sexp (' ':s) (kids:stack) a = sexp s ((leaf a:kids):stack) ""
sexp (c:s) stack a = sexp s stack (c:a)
