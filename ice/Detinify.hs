import Text.ParserCombinators.Parsec
import Text.ParserCombinators.Parsec.Char
import Data.List
import Data.Ord
import Data.Function (on)
import Data.Char
import Data.Either (rights)
import Control.Monad (liftM2, mzero)
import Numeric
main = print.map avg.cluster.map parseLines.lines
     =<< readFile "tinified-best5-path.txt"
    where cluster = histogram (==) fst.concat.rights
          avg = liftPair (decode.fst.head) (average.map snd)
average l = sum l / fromIntegral (length l)
histogram p key = groupBy (p `on` key).sortBy (comparing key)
decode path = foldr (\ c total -> 223 * total + (ord c - 32)) 0 path
liftPair f g a = (f a, g a)

parseLines = parse line "ok computer"
line = pair `endBy` (char '\t')
pair = liftM2 (,) (many1 (noneOf " \t")) (char ' ' >> number)
number = do s <- getInput
            case readSigned readFloat s of
              [(n, s')] -> setInput s' >> return n
              _ -> mzero

bestpaths =sortBy (comparing snd)
            [(("PU,CL CJ,CL SU,NP NPHD,PRON", 1610), 34.386099999999999)
           , (("PU,CL [ DISMK,REACT ", 1611), 23.120699999999999)
           , (("PU,CL CJ,CL [ SU,NP NPHD,PRON", 1630), 23.843800000000002)
           , (("] PU,CL VB,VP MVB,V", 1685), 24.755500000000001)
           , (("] PU,CL A,AVP AVHD,ADV", 1759), 30.924299999999999)
           , (("PU,CL DISMK,CONNEC", 1834), 28.138100000000001)
           , (("PU,CL DISMK,INTERJEC ", 1860), 28.711218181818182)
           , (("PU,CL [ DISMK,INTERJEC ", 1966), 25.888849999999998)
           , (("PU,NONCL DISMK,INTERJEC ", 2017), 25.12088)
           , (("PU,CL OD,CL VB,VP MVB,V", 2046), -21.20335)
           , (("PU,CL CS,NP [ DT,DTP DTCE,ART", 2090), 26.666399999999999)
           , (("PU,CL OD,NP [ DT,DTP DTCE,ART", 2286), -21.3429)
           , (("PU,CL A,CL VB,VP MVB,V", 2301), -19.2925)
           , (("PU,CL A,CL SU,NP NPHD,PRON", 2322), 18.196300000000001)
           , (("] PU,NONCL PAUSE,PAUSE", 2398), -30.739742857142861)
           , (("PU,CL ] SU,NP NPHD,N", 2853), -26.229749999999999)
           , (("PU,CL PAUSE,PAUSE", 3175), 31.073055555555559)
           , (("PU,CL CJ,CL VB,VP MVB,V", 3207), -12.490666666666664)
           , (("PU,NONCL DISMK,REACT ", 5602), 44.045899999999996)
           , (("] PU,CL PAUSE,PAUSE", 6650), 25.836588888888887)
           , (("PU,CL A,AVP AVHD,ADV", 6659), 15.9057)
           , (("PU,CL A,PP [ P,PREP", 7472), 41.766370000000002)
           , (("PU,CL [ DISMK,CONNEC", 8555), 50.947025000000004)
           , (("PU,CL ] VB,VP MVB,V", 9800), 75.412035999999986)
           , (("PU,CL VB,VP [ OP,AUX", 10438), 74.7334125)
           , (("PU,CL [ SU,NP NPHD,PRON", 11073), 87.509215789473686)
           , (("PU,CL SU,NP NPHD,PRON", 12850), 93.917162637362651)
           , (("PU,CL VB,VP MVB,V", 19684), 142.44978085106376)
           , (("PU,CL OD,CL SU,NP NPHD,PRON", 773), -18.326000000000001)
           , (("] PU,NONCL ELE,NP NPHD,N", 912), -20.405999999999999)
           , (("PU,CL OD,CL [ SUB,SUBP SBHD,CONJUNC", 930), -27.523399999999999)
           , (("PU,CL OD,CL ] VB,VP MVB,V", 1098), -20.106200000000001)
           , (("] PU,CL CS,AJP AJHD,ADJ", 1211), 20.442499999999999)
           , (("PU,CL OD,CL VB,VP [ OP,AUX", 1234), -28.2287)
           , (("PU,CL DISMK,FRM ", 1259), 22.309649999999998)
           , (("PU,CL CS,NP NPHD,N", 1325), 20.8065)]

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

