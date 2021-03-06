# -*- coding: utf-8 -*-
tbpath = '/Volumes/Data/Corpora/sv/Talbanken05/FPS/'
swpath = '/Volumes/Data/Corpora/sv/SweDiaSyn/Korrekturläst/'
talbanken = [tbpath + 'SD.tiger.xml',
             tbpath + "P.tiger.xml",
             tbpath + "IB.tiger.xml",
             tbpath + "G.tiger.xml"]
measures = ['r', 'r_sq', 'kl', 'js', 'cos']
features = ['path', 'trigram', 'dep', 'psg', 'grand',
            'unigram',
            'redep', 'deparc',
            'all']
samples = ['1000', 'full']
norms = ['ratio', 'freq']
numnorms = ['1', '5']
# TODO: Fix 'Leksand ' typo
swediaCounties = dict( # or I could just use the county code
    Stockholm = ['Sorunda'],
    Vasterbotten = [], # Vae
    Norrbotten = ['Arjeplog', 'Nederlulea', 'Overkalix'],
    Uppsala = ['Villberga'],
    Sodermanland = [], # Soed
    Ostergotland = ['Asby', 'StAnna'], # Oestergoet
    Jonkoping = [], # Joenkoep
    Kronoberg = [],
    Kalmar = ['Ankarsrum', 'Boda', 'Bredsatra', 'Segerstad', 'Torsås'],
    Gotland = ['Faro', 'Fole', 'Sproge'],
    Blekinge = ['Jamshog'],
    Skane = ['Norra Rorum', 'Bara', 'Loderup', 'Ossjo'], # Sk@ne
    Halland = ['Frillesas', 'Vaxtorp'],
    Vastra_Gotaland = ['Bengtsfors', 'Floby', 'Orust', 'Torso'], # Vaestra Goetaland
    Varmland = ['Köla'], # Vaerm
    Orebro = ['Viby'], # Oerebro
    Vastmanland = ['Skinnskatteberg'], # Vaestmanland
    Dalarna = ['Leksand'],
    Gavleborg = ['Arsunda'], # Gaev
    Vasternorrland = ['Anundsjo', 'Indal'], # Vaest
    Jamtland = [], # Jaemt
    )
swediaProvinces = dict( # or I could just use the county code
    Lappland = ['Arjeplog'],
    Norrbotten = ['Overkalix', 'Nederlulea'],
    Vasterbotten = [],
    Angermanland = ['Anundsjo'],
    Jamtland = [],
    Harjedalen = [],
    Medelpad = ['Indal'],
    Halsingland = [],
    Dalarna = ['Leksand'],
    Gastrikland = ['Arsunda'],
    Uppland = ['Villberga'],
    Vastmanland = ['Skinnskatteberg'],
    Varmland = ['Köla'],
    Narke = ['Viby'],
    Sodermanland = ['Sorunda'],
    Dalsland = ['Bengtsfors'],
    Bohuslan = ['Orust'],
    Vastergotland = ['Torso', 'Floby'],
    Ostergotland = ['Asby', 'StAnna'],
    Halland = ['Frillesas', 'Vaxtorp'],
    Smaland = ['Ankarsrum', 'Torsås'],
    Oland = ['Boda', 'Bredsatra', 'Segerstad'],
    Gotland = ['Faro', 'Fole', 'Sproge'],
    Skane = ['Norra Rorum', 'Ossjo', 'Bara', 'Loderup'],
    Blekinge = ['Jamshog'],
    )
swediaRegions = dict(
    Stockholm = ['Sorunda'],
    EastMiddle = ['Villberga', 'Asby', 'StAnna', 'Viby', 'Skinnskatteberg'],
    South = ['Jamshog', 'Norra Rorum', 'Bara', 'Loderup', 'Ossjo'],
    NorthMiddle = ['Leksand', 'Arsunda', 'Köla'],
    MiddleNorrland = ['Anundsjo', 'Indal'],
    UpperNorrland = ['Arjeplog', 'Nederlulea', 'Overkalix'],
    Smaland = ['Ankarsrum', 'Boda', 'Bredsatra', 'Segerstad', 'Torsås',
               'Faro', 'Fole', 'Sproge'],
    West = ['Bengtsfors', 'Floby', 'Orust', 'Torso', 'Frillesas', 'Vaxtorp'],
    )
# these clusters are a mixture of the 1-1000 (A) and 5-1000 (B,C)
# consensus clusters with everything else put in (D)
agreeClusters = dict(
    clusterA = ['Floby','Bengtsfors'],
    clusterB = [ 'Jamshog', 'Ossjo', 'Torsås', ],
    clusterC = [ 'Loderup',  'Bredsatra', ],
    clusterD = ['Segerstad','Köla', 'StAnna', 'Sorunda', 'Norra Rorum',
                'Villberga','Torso', 'Boda', 'Frillesas','Indal', 'Leksand',
                'Anundsjo', 'Arsunda', 'Asby',
                'Orust', 'Vaxtorp', 'Fole',
                'Sproge', 'Faro', 'Ankarsrum', 'Skinnskatteberg'],
    )
swediaSites = [
  'Ankarsrum',
  'Anundsjo',
  # 'Arjeplog',
  'Arsunda',
  'Asby',
  'Bara',
  'Bengtsfors',
  'Boda',
  'Bredsatra',
  'Faro',
  'Floby',
  'Fole',
  'Frillesas',
  'Indal',
  'Jamshog',
  'Köla',
  'Leksand', # WARNING: One filename is typoed 'Leksand ' not 'Leksand'
  'Loderup',
  # 'Nederlulea',
  'Norra Rorum',
  'Orust',
  'Ossjo',
  # 'Overkalix',
  'Segerstad',
  'Skinnskatteberg',
  'Sorunda',
  'Sproge',
  'StAnna',
  'Torsås',
  'Torso',
  #'Torsö',
  'Vaxtorp',
  'Viby',
  'Villberga',
]
swediaSitesEjkorrekturlast = [
  'Löderup',
  'Pite',
  'anu',
  'ara',
  'arjeplog',
  'ars',
  'aspås',
  'bara',
  'broby',
  'burtråsk',
  'delsbo',
  'gråsö',
  'ind',
  'lod',
  'nederkalix',
  'nysåtra',
  'oka',
  'ors',
  'pit',
  'sar',
  'sårna',
  'sorsele',
  'toh',
  'vindeln',
]
