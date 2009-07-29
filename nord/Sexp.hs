module Sexp (Tree(..), runsexp) where
import Data.Tree
import NLP.PennTreebank (parseTree)
import Text.ParserCombinators.Parsec (parse)
runsexp s = case parse parseTree "NLP.PennTreebank" s of
              Left err -> error (show err)
              Right sexp -> sexp
