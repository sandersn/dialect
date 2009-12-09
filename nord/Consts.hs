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
swediaCounties = Map.fromList [ -- or I could just use the county code
    ("Stockholm", ["Sorunda"]),
    ("Vasterbotten", []), -- Va
    ("Norrbotten", ["Arjeplog", "Nederlulea", "Overkalix"]),
    ("Uppsala", ["Villberga"]),
    ("Sodermanland", []), -- Soe
    ("Ostergotland", ["Asby", "StAnna"]), -- Oestergoe
    ("Jonkoping", []), -- Joenkoe
    ("Kronoberg", []),
    ("Kalmar", ["Ankarsrum", "Boda", "Bredsatra", "Segerstad", "Torsås"]),
    ("Gotland", ["Faro", "Fole", "Sproge"]),
    ("Blekinge", ["Jamshog"]),
    ("Skane", ["Norra Rorum", "Bara", "Loderup", "Ossjo"]), -- Sk@n
    ("Halland", ["Frillesas", "Vaxtorp"]),
    ("Vastra_Gotaland", ["Bengtsfors", "Floby", "Orust", "Torso"]), -- Vaestra Goetalan
    ("Varmland", ["Köla"]), -- Vaer
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
    ("Varmland", ["Köla"]),
    ("Narke", ["Viby"]),
    ("Sodermanland", ["Sorunda"]),
    ("Dalsland", ["Bengtsfors"]),
    ("Bohuslan", ["Orust"]),
    ("Vastergotland", ["Torso", "Floby"]),
    ("Ostergotland", ["Asby", "StAnna"]),
    ("Halland", ["Frillesas", "Vaxtorp"]),
    ("Smaland", ["Ankarsrum", "Torsås"]),
    ("Oland", ["Boda", "Bredsatra", "Segerstad"]),
    ("Gotland", ["Faro", "Fole", "Sproge"]),
    ("Skane", ["Norra Rorum", "Ossjo", "Bara", "Loderup"]),
    ("Blekinge", ["Jamshog"])
    ]
swediaRegions = Map.fromList [ -- (Riksomr@den)
    ("Stockholm", ["Sorunda"]),
    ("EastMiddle", ["Villberga", "Asby", "StAnna", "Viby", "Skinnskatteberg"]),
    ("South", ["Jamshog", "Norra Rorum", "Bara", "Loderup", "Ossjo"]),
    ("NorthMiddle", ["Leksand", "Arsunda", "Köla"]),
    ("MiddleNorrland", ["Anundsjo", "Indal"]),
    ("UpperNorrland", ["Arjeplog", "Nederlulea", "Overkalix"]),
    ("Smaland", ["Ankarsrum", "Boda", "Bredsatra", "Segerstad", "Torsås",
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
  "Löderup",
  "Pite",
  "anu",
  "ara",
  "arjeplog",
  "ars",
  "aspås",
  "bara",
  "broby",
  "burtråsk",
  "delsbo",
  "gråsö",
  "ind",
  "lod",
  "nederkalix",
  "nysåtra",
  "oka",
  "ors",
  "pit",
  "sar",
  "sårna",
  "sorsele",
  "toh",
  "vindeln"]
