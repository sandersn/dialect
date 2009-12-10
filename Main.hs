module Main where
import qualified Sed
main :: IO ()
main = print . Sed.analyse =<< Sed.groupSedInGor
