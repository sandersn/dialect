from util.lst import cross
import random
northern = ('Northern', 'Wales Northwest Scotland Northeast WestMidlands'.split())
southern = ('Southern', 'Southeast London EastMidlands'.split())
def each(f, l):
    for x in l:
        f(x)
def cat(((name, region), suffix)):
    f = open('%s-%s.dat' % (name,suffix), 'w')
    f.write(name + '\n')
    for loc in region:
        it = open('%s-%s.dat' % (loc, suffix))
        it.next()
        f.writelines(it)
        f.write('***\n')
    f.close()
def generate(division):
    if division=='ns':
        each(cat, cross([northern, southern], 'path trigram'.split()))
    else:
        ns = northern[1] + southern[1]
        random.shuffle(ns)
        n = ('NorthernRandom', ns[:len(northern[1])])
        s = ('SouthernRandom', ns[len(northern[1]):])
        each(cat, cross([n, s], 'path trigram'.split()))
        
if __name__=="__main__":
    generate('ns')
