-- -*- coding: utf-8 -*-
module Consts where
import Data.Map as Map
import Char (chr)
umlaut = chr 0xCC : chr 0x88 : ""
ring = chr 0xCC : chr 0x8A : ""
tbpath = "/Volumes/Data/Corpora/sv/Talbanken05/FPS/"
swpath = "/Volumes/Data/Corpora/sv/SweDiaSyn/Korrekturla\204\136st/"
talbanken = [tbpath ++ "SD.tiger.xml",
             tbpath ++ "P.tiger.xml",
             tbpath ++ "IB.tiger.xml",
             tbpath ++ "G.tiger.xml"]
-- TODO: Fix "Leksand " typo
-- "Leksand", WARNING: One filename is typoed "Leksand " not "Leksand"
quoteSpace site | ' ' `elem` site = "\"" ++ site ++ "\""
                | otherwise = site
swediaCounties = Map.fromList [ -- or I could just use the county code
    ("Stockholm", ["Sorunda"]),
    ("Vasterbotten", []), -- Va
    ("Norrbotten", ["Arjeplog", "Nederlulea", "Overkalix"]),
    ("Uppsala", ["Villberga"]),
    ("Sodermanland", []), -- Soe
    ("Ostergotland", ["Asby", "StAnna"]), -- Oestergoe
    ("Jonkoping", []), -- Joenkoe
    ("Kronoberg", []),
    ("Kalmar", ["Ankarsrum", "Boda", "Bredsatra", "Segerstad", "Torsa"++ring++"s"]),
    ("Gotland", ["Faro", "Fole", "Sproge"]),
    ("Blekinge", ["Jamshog"]),
    ("Skane", ["Norra Rorum", "Bara", "Loderup", "Ossjo"]), -- Sk@n
    ("Halland", ["Frillesas", "Vaxtorp"]),
    ("Vastra_Gotaland", ["Bengtsfors", "Floby", "Orust", "Torso"]), -- Vaestra Goetalan
    ("Varmland", ["Ko"++umlaut++"la"]), -- Vaer
    ("Orebro", ["Viby"]), -- Oerebr
    ("Vastmanland", ["Skinnskatteberg"]), -- Vaestmanlan
    ("Dalarna", ["Leksand"]),
    ("Gavleborg", ["Arsunda"]), -- Gae
    ("Vasternorrland", ["Anundsjo", "Indal"]), -- Vaes
    ("Jamtland", []) -- Jaem
    ]
swediaProvinces = Map.fromList [ -- or I could just use the county code
    ("Lappland", ["Arjeplog"]),
    ("Norrbotten", ["Overkalix", "Nederlulea"]),
    ("Vasterbotten", []),
    ("Angermanland", ["Anundsjo"]),
    ("Jamtland", []),
    ("Harjedalen", []),
    ("Medelpad", ["Indal"]),
    ("Halsingland", []),
    ("Dalarna", ["Leksand"]),
    ("Gastrikland", ["Arsunda"]),
    ("Uppland", ["Villberga"]),
    ("Vastmanland", ["Skinnskatteberg"]),
    ("Varmland", ["Ko"++umlaut++"la"]),
    ("Narke", ["Viby"]),
    ("Sodermanland", ["Sorunda"]),
    ("Dalsland", ["Bengtsfors"]),
    ("Bohuslan", ["Orust"]),
    ("Vastergotland", ["Torso", "Floby"]),
    ("Ostergotland", ["Asby", "StAnna"]),
    ("Halland", ["Frillesas", "Vaxtorp"]),
    ("Smaland", ["Ankarsrum", "Torsa"++ring++"s"]),
    ("Oland", ["Boda", "Bredsatra", "Segerstad"]),
    ("Gotland", ["Faro", "Fole", "Sproge"]),
    ("Skane", ["Norra Rorum", "Ossjo", "Bara", "Loderup"]),
    ("Blekinge", ["Jamshog"])
    ]
swediaRegions = Map.fromList [ -- (Riksomr@den)
    ("Stockholm", ["Sorunda"]),
    ("EastMiddle", ["Villberga", "Asby", "StAnna", "Viby", "Skinnskatteberg"]),
    ("South", ["Jamshog", "Norra Rorum", "Bara", "Loderup", "Ossjo"]),
    ("NorthMiddle", ["Leksand", "Arsunda", "Ko"++umlaut++"la"]),
    ("MiddleNorrland", ["Anundsjo", "Indal"]),
    ("UpperNorrland", ["Arjeplog", "Nederlulea", "Overkalix"]),
    ("Smaland", ["Ankarsrum", "Boda", "Bredsatra", "Segerstad", "Torsa"++ring++"s",
               "Faro", "Fole", "Sproge"]),
    ("West", ["Bengtsfors", "Floby", "Orust", "Torso", "Frillesas", "Vaxtorp"])
    ]
-- these are the filenames
-- (complete with bizarro combining diacritics for Kola and Torsas)
swediaSites = [
  "Ankarsrum",
  "Anundsjo",
  -- "Arjeplog",
  "Arsunda",
  "Asby",
  "Bara",
  "Bengtsfors",
  "Boda",
  "Bredsatra",
  "Faro",
  "Floby",
  "Fole",
  "Frillesas",
  "Indal",
  "Jamshog",
  "Ko"++umlaut++"la",
  "Leksand", -- WARNING: One filename is typoed "Leksand " not "Leksand"
  "Loderup",
  -- "Nederlulea",
  "Norra Rorum",
  "Orust",
  "Ossjo",
  -- "Overkalix",
  "Segerstad",
  "Skinnskatteberg",
  "Sorunda",
  "Sproge",
  "StAnna",
  "Torsa"++ring++"s",
  "Torso",
  --"Torsö",
  "Vaxtorp",
  "Viby",
  "Villberga"]
-- these are the correct spellings for display in the dissertation
swediaLabels = [
  "Ankarsrum",
  "Anundsjö",
  -- "Arjeplog",
  "Årsunda",
  "Asby",
  "Bara",
  "Bengtsfors",
  "Böda",
  "Bredsätra",
  "Fårö",
  "Floby",
  "Fole",
  "Frillesås",
  "Indal",
  "Jämshög",
  "Köla",
  "Leksand", -- WARNING: One filename is typoed "Leksand " not "Leksand"
  "Löderup",
  -- "Nederlulea",
  "Norra Rörum",
  "Orust",
  "Össjö",
  -- "Overkalix",
  "Segerstad",
  "Skinnskatteberg",
  "Sorunda",
  "Sproge",
  "S:t Anna",
  "Torsås",
  "Torsö",
  --"Torsö",
  "Våxtorp",
  "Viby",
  "Villberga"]
swediaSitesEjkorrekturlast = [
  "Lo" ++ umlaut ++ "derup",
  -- "Löderup",
  "Pite",
  "anu",
  "ara",
  "arjeplog",
  "ars",
  "aspa"++ring++"s",
  -- "aspås",
  "bara",
  "broby",
  "burtra"++umlaut++"sk",
  "delsbo",
  "gra"++umlaut++"so"++umlaut,
  "ind",
  "lod",
  "nederkalix",
  "nysa"++umlaut++"tra",
  "oka",
  "ors",
  "pit",
  "sar",
  "sa"++umlaut++"rna",
  "sorsele",
  "toh",
  "vindeln"]
swediaSiteLocations = Map.fromList [
  ("Ankarsrum", (1014, 3622)),
  ("Anundsjo", (1254,1825)),
  ("Arjeplog", (1205,980)),
  ("Arsunda", (1080, 2722)),
  ("Asby", (814,3554)),
  ("Bara", (451, 4280)),
  ("Bengtsfors", (305,3180)),
  ("Boda", (1117,3777)),
  ("Bredsatra", (1082, 3874)),
  ("Faro", (1471, 3531)),
  ("Floby", (514, 3480)),
  ("Fole", (1382, 3622)),
  ("Frillesas", (305, 3722)),
  ("Indal", (1111,2068)),
  ("Jamshog", (694, 4080)),
  ("Ko"++umlaut++"la",(348,2960)),
  ("Leksand", (797,2677)), -- WARNING: One filename is typoed "Leksand " not "Leksand"
  ("Loderup", (594, 4325)),
  ("Nederlulea", (1734,1071)),
  ("Norra Rorum", (505, 4145)),
  ("Orust", (222, 3448)),
  ("Ossjo", (414, 4077)),
  ("Overkalix", (1808, 794)),
  ("Segerstad", (1037, 4025)),
  ("Skinnskatteberg", (897,2945)),
  ("Sorunda", (1260,3197)),
  ("Sproge", (1334, 3745)),
  ("StAnna", (1080,3422)),
  ("Torsa"++ring++"s", (957, 3988)),
  ("Torso", (585, 3265)),
  --"Torsö",
  ("Vaxtorp", (440, 4000)),
  ("Viby", (762, 3185)),
  ("Villberga", (1140, 3031))]
swediaSizes = [
  ("Ankarsrum", 630),
  ("Anundsjo", 1144),
  -- ("Arjeplog", 321),
  ("Arsunda", 937),
  ("Asby", 693),
  ("Bara", 696),
  ("Bengtsfors", 663),
  ("Boda", 1029),
  ("Bredsatra", 360),
  ("Faro", 659),
  ("Floby", 557),
  ("Fole", 727),
  ("Frillesas", 572),
  ("Indal", 1126),
  ("Jamshog", 301),
  ("Ko"++umlaut++"la", 528),
  ("Leksand", 923), -- WARNING: One filename is typoed "Leksand " not "Leksand"
  ("Loderup", 429),
  -- ("Nederlulea", 103),
  ("Norra Rorum", 546),
  ("Orust", 1067),
  ("Ossjo", 481),
  -- ("Overkalix", 409),
  ("Segerstad", 837),
  ("Skinnskatteberg", 730),
  ("Sorunda", 768),
  ("Sproge", 381),
  ("StAnna", 876),
  ("Torsa"++ring++"s", 374),
  ("Torso", 956),
  --"Torsö",
  ("Vaxtorp", 903),
  ("Viby", 431),
  ("Villberga", 680)]
swediaWords = [
  ("Ankarsrum", 7708),
  ("Anundsjo", 11897),
  -- ("Arjeplog", ),
  ("Arsunda", 8933),
  ("Asby", 7171),
  ("Bara", 10724),
  ("Bengtsfors", 7423),
  ("Boda", 17425),
  ("Bredsatra", 6938),
  ("Faro", 8260),
  ("Floby", 6392),
  ("Fole", 9920),
  ("Frillesas", 9634),
  ("Indal", 13090),
  ("Jamshog", 8661),
  ("Ko"++umlaut++"la", 10133),
  ("Leksand", 10676), -- WARNING: One filename is typoed "Leksand " not "Leksand"
  ("Loderup", 7850),
  -- ("Nederlulea", ),
  ("Norra Rorum", 9160),
  ("Orust", 11409),
  ("Ossjo", 12275),
  -- ("Overkalix", ),
  ("Segerstad", 9746),
  ("Skinnskatteberg", 9529),
  ("Sorunda", 11144),
  ("Sproge", 4399),
  ("StAnna", 13156),
  ("Torsa"++ring++"s", 9217),
  ("Torso", 15577),
  --"Torsö",
  ("Vaxtorp", 11353),
  ("Viby", 6734),
  ("Villberga", 11479)]
swediaPopulations = [
  ("Ankarsrum", 1568),
  ("Anundsjo", 5060),
  -- ("Arjeplog", ),
  ("Arsunda", 2161),
  ("Asby", 626),
  ("Bara", 3639),
  ("Bengtsfors", 11614),
  ("Boda", 942),
  ("Bredsatra", 266),
  ("Faro", 634),
  ("Floby", 1432),
  ("Fole", 347),
  ("Frillesas", 1943),
  ("Indal", 1961),
  ("Jamshog", 11764),
  ("Ko"++umlaut++"la", 1521),
  ("Leksand", 15340), -- WARNING: One filename is typoed "Leksand " not "Leksand"
  ("Loderup", 923),
  -- ("Nederlulea", ),
  ("Norra Rorum", 526),
  ("Orust", 15175),
  ("Ossjo", 522),
  -- ("Overkalix", ),
  ("Segerstad", 103),
  ("Skinnskatteberg", 4093),
  ("Sorunda", 4714),
  ("Sproge", 139),
  ("StAnna", 2350),
  ("Torsa"++ring++"s", 7639),
  ("Torso", 556),
  --"Torsö",
  ("Vaxtorp", 2377),
  ("Viby", 3088),
  ("Villberga", 1255)]
swediaWordsPerSentence = [("Ankarsrum",12.234920634920634)
                         ,("Anundsjo",10.399475524475525)
                         ,("Arsunda",9.533617929562434)
                         ,("Asby",10.347763347763347)
                         ,("Bara",15.408045977011493)
                         ,("Bengtsfors",11.196078431372548)
                         ,("Boda",16.933916423712343)
                         ,("Bredsatra",19.272222222222222)
                         ,("Faro",12.534142640364188)
                         ,("Floby",11.47576301615799)
                         ,("Fole",13.645116918844566)
                         ,("Frillesas",16.842657342657343)
                         ,("Indal",11.625222024866785)
                         ,("Jamshog",28.774086378737543)
                         ,("Ko\204\136la",19.19128787878788)
                         ,("Leksand",11.566630552546046)
                         ,("Loderup",18.2983682983683)
                         ,("Norra Rorum",16.776556776556777)
                         ,("Orust",10.692596063730084)
                         ,("Ossjo",25.51975051975052)
                         ,("Segerstad",11.643966547192354)
                         ,("Skinnskatteberg",13.053424657534247)
                         ,("Sorunda",14.510416666666666)
                         ,("Sproge",11.545931758530184)
                         ,("StAnna",15.018264840182649)
                         ,("Torsa\204\138s",24.644385026737968)
                         ,("Torso",16.293933054393307)
                         ,("Vaxtorp",12.572535991140642)
                         ,("Viby",15.624129930394432)
                         ,("Villberga",16.88088235294118)]
