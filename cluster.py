### minimum spanning trees ###
from util.fnc import car,cdr
verts = ['utp02', 'sgl20', 'sif20', 'siz20', 'sgj20','siw20', 'sgb20', 'see26']
edges = [("utp02", "sgl20", 226.87015),
         ("utp02", "sif20", 239.3214),
         ("utp02", "siz20", 291.05685),
         ("utp02", "sgj20", 293.28705),
         ("utp02", "siw20", 347.17184),
         ("utp02", "sgb20", 570.414),
         ("utp02", "see26", 489.02435),
         ("sgl20", "sif20", 295.9317),
         ("sgl20", "siz20", 309.2869),
         ("sgl20", "sgj20", 357.0291),
         ("sgl20", "siw20", 421.30493),
         ("sgl20", "sgb20", 547.7434),
         ("sgl20", "see26", 500.0514),
         ("sif20", "siz20", 369.83728),
         ("sif20", "sgj20", 402.52115),
         ("sif20", "siw20", 397.05994),
         ("sif20", "sgb20", 570.1482),
         ("sif20", "see26", 545.6265),
         ("siz20", "sgj20", 398.09525),
         ("siz20", "siw20", 386.399),
         ("siz20", "sgb20", 591.249),
         ("siz20", "see26", 535.5345),
         ("sgj20", "siw20", 492.21973),
         ("sgj20", "sgb20", 620.3736),
         ("sgj20", "see26", 567.65),
         ("siw20", "sgb20", 592.8426),
         ("siw20", "see26", 545.2423),
         ("sgb20", "see26", 746.6446)]
answer = set([('utp02', 'see26', 489.02435000000003),
              ('utp02', 'sgl20', 226.87015),
              ('utp02', 'siw20', 347.17183999999997),
              ('utp02', 'sgj20', 293.28705000000002),
              ('utp02', 'sif20', 239.32140000000001),
              ('utp02', 'siz20', 291.05685),
              ('sgl20', 'sgb20', 547.74339999999995)])
testverts = list('abcdefghi')
testedges = [('a', 'b', 4),
           ('a', 'h', 8),
           ('b', 'h', 11),
           ('b', 'c', 8),
           ('c', 'd', 7),
           ('c', 'f', 4),
           ('c', 'i', 2),
           ('d', 'e', 9),
           ('d', 'f', 14),
           ('e', 'f', 10),
           ('f', 'g', 2),
           ('g', 'i', 6),
           ('g', 'h', 1),
           ('h', 'i', 7)]
def union(u,v,l):
    "this is total crap"
    ui = vi = 0
    for i,s in enumerate(l):
        if u in s:
            ui = i
        if v in s:
            vi = i
    if ui != vi:
        l[ui] |= l[vi]
        del l[vi]
        return True
    else:
        return False
def mklist(x):
    return [x]
def mkset(x):
    return set([x])
def mst_kruskal(verts, edges):
    a = set()
    vs = [set([v]) for v in verts]
    edges.sort(key=lambda (e1,e2,score): score)
    for u,v,w in edges:
        print vs
        print (u,v,w)
        if union(u, v, vs):
            a.add((u,v,w))
    return a
edges = {frozenset(['sgl20', 'utp02']): 226.87015,
         frozenset(['siw20', 'sgj20']): 492.21973000000003,
         frozenset(['siw20', 'see26']): 545.2423,
         frozenset(['siz20', 'sgl20']): 309.2869,
         frozenset(['see26', 'siz20']): 535.53449999999998,
         frozenset(['siw20', 'sgl20']): 421.30493000000001,
         frozenset(['see26', 'sgj20']): 567.64999999999998,
         frozenset(['sgj20', 'utp02']): 293.28705000000002,
         frozenset(['siz20', 'sgj20']): 398.09525000000002,
         frozenset(['see26', 'sif20']): 545.62649999999996,
         frozenset(['sgj20', 'sif20']): 402.52114999999998,
         frozenset(['sgb20', 'sif20']): 570.14819999999997,
         frozenset(['sgb20', 'utp02']): 570.41399999999999,
         frozenset(['siw20', 'sif20']): 397.05993999999998,
         frozenset(['siw20', 'siz20']): 386.399,
         frozenset(['see26', 'utp02']): 489.02435000000003,
         frozenset(['see26', 'sgb20']): 746.64459999999997,
         frozenset(['sgj20', 'sgb20']): 620.37360000000001,
         frozenset(['see26', 'sgl20']): 500.0514,
         frozenset(['sgj20', 'sgl20']): 357.02910000000003,
         frozenset(['siz20', 'utp02']): 291.05685,
         frozenset(['siz20', 'sgb20']): 591.24900000000002,
         frozenset(['sif20', 'utp02']): 239.32140000000001,
         frozenset(['sgb20', 'sgl20']): 547.74339999999995,
         frozenset(['siw20', 'sgb20']): 592.84259999999995,
         frozenset(['siw20', 'utp02']): 347.17183999999997,
         frozenset(['siz20', 'sif20']): 369.83728000000002,
         frozenset(['sgl20', 'sif20']): 295.93169999999998}
matlab = ( # (pairwise '(utp02 see26 sgb20 sgj20 sgl20 sif20 siw20 siz20))
    489.02435,
    570.414,
    293.28705,
    226.87015,
    239.3214,
    347.17184,
    291.05685,
    746.6446,
    567.65,
    500.0514,
    545.6265,
    545.2423,
    535.5345,
    547.7434,
    620.3736,
    570.1482,
    592.8426,
    591.249,
    357.0291,
    402.52115,
    492.21973,
    398.09525,
    295.9317,
    421.30493,
    309.2869,
    397.05994,
    369.83728,
    386.399,)
from util.lst import cross, avg
from util.fnc import compose, cur
from util.reflect import traced
from util.slop import memoise
def pairwise(l):
    'Only works for lists up to 1000 in size. snide Python comment goes here'
    if not l:
        return []
    else:
        return [(car(l),x) for x in cdr(l)] + pairwise(cdr(l))
def flatten(l):
    flat = []
    for x in l:
        if not isinstance(x,str):
            flat += flatten(x)
        else:
            flat.append(x)
    return flat
def maxby(f, l):
    best, bestval = car(l), f(car(l))
    for x in cdr(l):
        val = f(x)
        if val > bestval:
            best, bestval = x, val
    return best
def minby(f, l):
    best, bestval = car(l), f(car(l))
    for x in cdr(l):
        val = f(x)
        if val < bestval:
            best, bestval = x, val
    return best
def bottomup(verts, sim):
    "TODO:make sim = sum 1/d or something"
    C = set(frozenset([v]) for v in verts)
    while len(C) > 1:
        c1,c2 = minby(sim, pairwise(list(C)))
        cj = frozenset([c1, c2])
        C.remove(c1)
        C.remove(c2)
        C.add(cj)
    return C
def single((c1,c2)):
    "single link"
    return min(map(compose(edges.__getitem__, frozenset),
                   cross(flatten(c1), flatten(c2))))
def complete((c1,c2)):
    "complete link"
    return max(map(compose(edges.__getitem__, frozenset),
                   cross(flatten(c1), flatten(c2))))
def groupavg((c1,c2)):
    "group average"
    return avg(map(compose(edges.__getitem__, frozenset),
                   cross(flatten(c1), flatten(c2))))
def tolist(set, sim):
    return [(tolist(x, sim),sim(tuple(x))) \
            if len(x)==2 else tolist(x, sim) \
            if isinstance(x, frozenset) else x \
            for x in set]
tolist(bottomup(verts, single), single)== \
                       [([['sgb20'],
                          ([['see26'],
                            ([([([([['sif20'],
                                    ([['utp02'],
                                      ['sgl20']], 226.87015)],
                                   239.3214),
                                  ['siz20']], 291.05685),
                                ['sgj20']], 293.28705),
                              ['siw20']], 347.17184)], 489.02435)], 547.7434)]
tolist(bottomup(verts, groupavg), groupavg)== \
                       [([['sgb20'],
                          ([['see26'],
                            ([([([([['sif20'],
                                    ([['utp02'],
                                      ['sgl20']], 226.87015)],
                                   267.62655),
                                  ['siz20']], 323.393676),
                                ['sgj20']], 362.7331375),
                              ['siw20']], 408.831088)],
                           530.5215083)], 605.63077142857139)]
tolist(bottomup(verts, complete), complete) == \
                       [([['sgb20'],
                          ([['see26'],
                            ([([([([['sif20'],
                                    ([['utp02'],
                                      ['sgl20']], 226.87015)], 295.9317),
                                  ['siz20']], 369.83728),
                                ['sgj20']], 402.52115),
                              ['siw20']], 492.21973)],
                           567.65)], 746.6446)]
"""
Yeah, I realised after sending the diagram that it assumes a lot of background knowledge.
The distances between nodes are Levenshtein distances.
I describe these in the paper Steve and I worked on, at 
http://jones.ling.indiana.edu/cipaper.doc 
or 
http://jones.ling.indiana.edu/cipaper.pdf.
Levenshtein distance finds the number of phonetic feature changes needed to change one word into another. So kAb -> kAt  has a distance of 2: +voice to -voice and labial to coronal. I sum these distances for all 107 words in the test set.
Therefore, a distance of 291 for (utp02 -- siz20) means that 291 features had to change to make them identical.

utp02 is a name I used for "baseline speaker", which was a bad idea. I should have used "base". It's the American English dictionary pronunciation of words for the 107 word list.

To create that graph, I found the distance of every speaker from every other speaker, NOT just utp02. This is different from the paper we submitted, where the speakers were only compared to utp02. Generating all comparisons like that created a fully connected graph. Then the spanning tree algorithm kept only the links that result in the lowest total distance for the entire graph. That means the reason there is a chain
utp02 -- sgl20 -- sgb20 (227 + 547)
is that the two separate chains
utp02 -- sgl20 (227)
utp02 -- sgb20 (570)
had higher total distance. (227+547 < 227+570)

I got hierarchical clustering working yesterday, but I am still working on the diagram for it. I will send it to you when I have it done."""

"""Plus something else earlier
Motor theory
Historical linguitics
depuis ca, the semester finally starts

Look for mismatches between production and perception.
Maybe in dialect -ahem- literature.
Ken has seen 3 cases himself.
Hunting is our job. Call up references on Wednesday. Eh.
Jungsun is also doing some work on this (dialects).
Topic ideas are due late February. Yes, I knew this.

did you get the right response y of the set Y of alternatives?
Wiener's quote: "the most important piece of information in perception
is that the signal isn't gibberish"
why economisation? he doesn't know...
how do we knows it's there? <-> there is a lot of motor evidence for it
  but it's not immediately obvious that you're pushed against a physical limit
  when speaking. People operate well within their physiological limits.
how do we measure it?

He says:
The phonology is internalised knowledge, and is needed to know how to boost the
probability of correct perception in cases of increased noise (or other
unfavourable environment)"""
"""Dissertation defence by Brian Riordan

---Liberman et al---

- perception is mediated by production
  - processes are common
  - functionally motoric

- Coarticulation is really three things -
(1) coproduction - temporal overlap in production - eg si/su variation in s
(2) sequencing effects - in di/du, the transition d->i is different from d->u
(3) articulatory tuning - ki vs ku (may just be (1) again)

- gesture -> motor plan -> motor execution ->
    invariant neurological activity corresponding to subphonemic unit.
  - encoder has information that is useful for decoder
  - Another reason is Occam's razor. Why have two systems if you can use
    only one.

- dichotic listening effects -> speech/non-speech
- rapidity of speech
- optimised for transmission (rate) (causes coproduction)

---Liberman and Mattingly---
nobody likes modules any more. Fodor ruled the 80s apparently

---model---
production = (acoustic_output = intent |> x |> y |> z |> ka)
(x |> y) is neuro
(z |> ka) is physiological
perception = combine x y z ka -- in some way, not specified
phonology = shared part of perception and production: the gestures, in a word
"""
"""Keith Johnson's paper is about how exemplar models are supposed to work.
It fits in nicely with Pierrehumbert's toy model.
Ohala tomorrow

Fowler 1986
- perception is to recover events from RL
- perception doesn't require (a) inference (b) hypothesis testing
    [Stevens and SPE both require (b)]
- events are in the signal. no exceptions
  if it's not, we need inference...something like Lindblum's signal
  complementation. In contrast, the signal is very clear.
  * people are good at perceiving it
- attention to the signal can be modulated (id est, amped up or down)
  * perceptual system
  * action system <-- could be 'ignore'. this is also where frequency effects
    would be implemented
distal event -> medium -> receiver
events interact with medium and receiver interact with the medium, only in
ways that we are sensitive to (eg IR isn't perceived very well).
  anything that is a _potential_ cue IS a cue.

oh right. this is the 'realist' part: you don't perceive the
lightwaves coming in (vision) or the soundwaves coming in (speech).
you perceive the object in
the distance (vision) or the person talking to you (speech).
actually you perceive the vocal tract.. or phonetically structure syllables??

- affordances : what is it good for. FUNCTIONALISM
(not linguistic def of functionalism, but a generalised variant of it)

You might be able to find evidence against this if you can find
production/perception mismatches that show perception/perception ISN'T perfect
and that some inference has to be going on in one side or the other.
"""
"""
Experiment ideas:
    Test a MI speaker as soon as they arrive at IU for ae/AE distinction
    Test again at end of spring semester
    Test again after summer break.
    -------
    Allow a listener to acclimate to another talker
    Have the talker ask a question "Do you like apples?"
    Have the listener repeat the question as a sentence: "I like apples"
    Did the listener change
    Investiage splits, mergers and shifts
    For extra fun, lie about the origin of the speaker. If the listener is from
    Bloomington, tell them a MI speaker is from N Indiana, or a S Indiana
    speaker is from Kentucky. What changes? Does the perception alter? Does
    the production change around?

    ---Project proposal---
    Set up a loop quite similar to many of the models discussed in the
    seminar so far. See Ohala for the clearest diagram of this.
    The talker starting the loop will be of some dialect area with a contrast
    not shared by the speaker. For example, the o/O distinction. The listener
    will be asked to repeat the talker's productions with some slight variation
    The question is whether the talker will produce any variation in the
    segment that has been merged relative to the other talker?
    Similar studies have been done with artificially modified speech (19xx).
    Dialect perception studies have used similar methods to look at
    different questions (20xx). An interlingual study has looked at a similar
    question of VOT in
    Three interesting variations present themselves. First, to test a shift
    such as ae/AE, which does not require recognising a split/merger. Second,
    to reverse the direction to see if partial merger happens. Third, to
    bias dialect perceptions by labelling the talker as coming from some
    location which is perceived to have the same (or different) characteristics
    as the listener's dialect.
"""
