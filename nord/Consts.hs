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
swediaSites = [
  "Ankarsrum",
  "Anundsjo",
  "Arjeplog",
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
  "Nederlulea",
  "Norra Rorum",
  "Orust",
  "Ossjo",
  "Overkalix",
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
