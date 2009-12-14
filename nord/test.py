import os
import sys
def run(cmd):
    result = os.system(cmd)
    if result: raise Exception("Error: '%s' returned code %d" % (cmd, result))
def swedia():
    run('rm Swedia.o')
    run('ghc --make TestSwedia -main-is Main.testmain')
    run('./TestSwedia')
def blade(runner, targets):
    for target in targets:
        print("Running target", target)
        getattr(runner, target)()
if __name__=="__main__":
    import test
    blade(test,
          sys.argv[1:] if sys.argv[1:] else 'swedia'.split())
