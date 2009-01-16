import qualified Data.ByteString.Char8 as Str
import Text.ParserCombinators.Parsec
import Data.List
import Data.Ord
import Data.Char
main = print.map fst.detinify =<< Str.readFile "tinified-best5-path.txt"
detinify s = massage histogram
    where paths = sort . concat . map (Str.split ' ') . Str.split '\n' $ s
          histogram = (zip (nub paths) (map length . group $ paths))
          massage = tail . reverse . sortBy (comparing snd) . map decode
decode (path,count) = (Str.foldr bar 0 path, count)
    where bar n total = 223 * total + (ord n - 32)
histogram l = zip (map head ls) (map length ls)
    where ls = group . sort $ l

{-codedValues = line `endBy` eol
line = do pairs <- pair `sepBy` (char ';'); char '\n'; 
pairs = do code <- many1 (oneOf ['!'..'z'])
           char '*'
           val <- chars ('.' : ['0'..'9'])
           char ';'
           optional '\n'
           return (code, val)-}

bestpaths = [("PU,CL VB,VP MVB,V", 19684),
             ("PU,CL SU,NP NPHD,PRON", 12850),
             ("PU,CL [ SU,NP NPHD,PRON", 11073),
             ("PU,CL VB,VP [ OP,AUX", 10438),
             ("PU,CL ] VB,VP MVB,V", 9800),
             ("PU,CL [ DISMK,CONNEC", 8555),
             ("PU,NONCL DISMK,REACT ", 5602),
             ("PU,CL A,PP [ P,PREP", 7472),
             ("PU,CL A,AVP AVHD,ADV", 6659),
             ("PU,CL PAUSE,PAUSE", 3175),
             ("] PU,NONCL PAUSE,PAUSE", 2398),
             ("PU,CL DISMK,INTERJEC ", 1860),
             ("] PU,CL PAUSE,PAUSE", 6650),
             ("PU,NONCL DISMK,INTERJEC ", 2017),
             ("PU,CL [ DISMK,REACT ", 1611),
             ("PU,NONCL ELE,NP NPHD,N", 1470),
             ("PU,CL OD,CL VB,VP [ OP,AUX", 1234),
             ("PU,CL CJ,CL VB,VP MVB,V", 3207),
             ("PU,CL CJ,CL VB,VP [ OP,AUX", 2239),
             ("PU,CL CJ,CL A,PP [ P,PREP", 1415),
             ("PU,CL OD,CL ] VB,VP MVB,V", 1098),
             ("PU,NONCL [ DISMK,CONNEC", 940),
             ("PU,CL A,PP PC,NP [ DT,DTP DTCE,ART", 2706),
             ("PU,CL A,CL [ SUB,SUBP SBHD,CONJUNC", 2508),
             ("PU,NONCL [ DISMK,REACT ", 2227),
             ("PU,CL CJ,CL ] VB,VP MVB,V", 2057),
             ("PU,CL OD,NP NPHD,N", 1939),
             ("PU,CL DISMK,CONNEC", 1834),
             ("PU,CL CJ,CL [ SU,NP NPHD,PRON", 1630),
             ("PU,CL CJ,CL SU,NP NPHD,PRON", 1610)]
besttrigrams = [("NPHD,PRON OP,AUX MVB,V", 12193),
                ("DTCE,PRON NPHD,N AJHD,ADJ", 57),
                ("DISMK,REACT  DISMK,REACT  NPHD,PRON", 84),
                ("P,PREP DTCE,ART NPHD,N", 10645),
                ("AJHD,ADJ NPHD,N DISMK,CONNEC", 152),
                ("AVHD,ADV NPHD,NUM PAUSE,PAUSE", 18),
                ("MVB,V DTCE,ART NPHD,N", 5934),
                ("DTCE,ART NPHD,N P,PREP", 6770),
                ("NPHD,PRON MVB,V AVHD,ADV", 5093),
                ("DISMK,CONNEC NPHD,N AVHD,ADV", 39),
                ("DTCE,ART AJHD,ADJ NPHD,N", 5748),
                ("NPHD,PRON MVB,V NPHD,PRON", 3971),
                ("NPHD,N P,PREP NPHD,N", 5931),
                ("EXOP,EXTHERE  SBHD,CONJUNC DTCE,ART", 1),
                ("COAP,CONNEC NPHD,PRON DISMK,CONNEC", 6),
                ("NPHD,PRON DISMK,INTERJEC  DTCE,ART", 14),
                ("AVHD,ADV INVOP,V NPHD,N", 22),
                ("DISMK,FRM  NPHD,PRON OP,AUX", 399),
                ("COOR,CONJUNC MVB,V NPHD,PRON", 389),
                ("MVB,V P,PREP AJHD,ADJ", 388),
                ("NPHD,NADJ OP,AUX MVB,V", 29),
                ("TO,PRTCL MVB,V NPHD,N", 404),
                ("DISMK,CONNEC INTOP,AUX NPHD,PRON", 151),
                ("MVB,V NPHD,PRON DTCE,ART", 378),
                ("DISMK,REACT  DISMK,REACT  DISMK,REACT ", 375),
                ("OP,AUX MVB,V NPHD,PRON", 2860),
                ("MVB,V DISMK,FRM  DTPE,PRON", 2),
                ("MVB,V NPHD,N COOR,CONJUNC", 401),
                ("NPHD,NUM P,PREP DTCE,ART", 401),
                ("NPHD,PRON AVHD,ADV AVHD,ADV", 368),
                ("NPHD,N P,PREP DTCE,ART", 5705),
                ("PAUSE,PAUSE DISMK,INTERJEC  DTPS,PRON", 4),
                ("INDET,?  INTOP,AUX NPHD,PRON", 3),
                ("DISMK,CONNEC COAP,CONNEC NPHD,N", 3),
                ("OP,AUX DISMK,FRM  DISMK,FRM ", 10),
                ("AJHD,ADJ DISMK,INTERJEC  P,PREP", 8),
                ("AVB,AUX MVB,V OP,AUX", 5),
                ("AVHD,ADV NPHD,N MVB,V", 152),
                ("AVHD,ADV DTCE,ART AJHD,ADJ", 395),
                ("DTPS,NUM NPHD,N NPHD,PRON", 394),
                ("MVB,V AVHD,ADV COOR,CONJUNC", 379),
                ("NPHD,N MVB,V SBHD,CONJUNC", 371),
                ("DTPS,NUM NPHD,N AVHD,ADV", 364),
                ("DTCE,ART NPHD,N NPHD,N", 351),
                ("NPHD,N NPHD,PRON MVB,V", 2371),
                ("P,PREP NPHD,N PAUSE,PAUSE", 1857),
                ("NPHD,PRON NPHD,PROFM NPHD,PRON", 1),
                ("NPHD,PRON SBHD,PRTCL DTCE,PRON", 1),
                ("DISMK,FRM  INDET,?  NPHD,PRON", 1),
                ("DISMK,CONNEC MVB,V TO,PRTCL", 3),
                ("NPHD,PRON COOR,CONJUNC AVHD,ADV", 83),
                ("COOR,CONJUNC NPHD,NUM P,PREP", 56),
                ("NPHD,PRON AVHD,ADV NPHD,PRON", 150),
                ("DISMK,CONNEC NPHD,PRON NPHD,PRON", 148),
                ("NPHD,N PAUSE,PAUSE DTCE,ART", 148),
                ("AJHD,ADJ SBHD,CONJUNC NPHD,PRON", 361),
                ("MVB,V NPHD,PRON DISMK,REACT ", 21),
                ("MVB,V NPHD,PRON TO,PRTCL", 352),
                ("DISMK,INTERJEC  AVHD,ADV DTCE,ART", 38),
                ("NPHD,PRON AVHD,ADV OP,AUX", 343),
                ("AJHD,ADJ NPHD,N P,PREP", 3571),
                ("P,PREP DTCE,PRON NPHD,N", 3320),
                ("NPHD,N OP,AUX MVB,V", 2746),
                ("NPHD,PRON MVB,V P,PREP", 2570),
                ("OP,AUX MVB,V AVHD,ADV", 2484),
                ("MVB,V DTCE,ART AJHD,ADJ", 2405),
                ("P,PREP DTCE,ART AJHD,ADJ", 2215),
                ("SBHD,CONJUNC NPHD,PRON OP,AUX", 2190),
                ("DTCE,ART NPHD,N MVB,V", 2178),
                ("AJHD,ADJ NPHD,N PAUSE,PAUSE", 2008),
                ("DISMK,CONNEC NPHD,PRON OP,AUX", 1949),
                ("OP,AUX AVB,AUX MVB,V", 1947),
                ("NPHD,N NPHD,PRON OP,AUX", 1698),
                ("NPHD,N MVB,V AVHD,ADV", 1618),
                ("P,PREP AJHD,ADJ NPHD,N", 1561),
                ("NPHD,PRON MVB,V NPHD,N", 1250),
                ("P,PREP NPHD,N COOR,CONJUNC", 1191)]

