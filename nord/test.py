import os
import sys
def run(cmd):
    result = os.system(cmd)
    if result: raise Exception("Error: '%s' returned code %d" % (cmd, result))
def swedia():
    try:
        run('rm Swedia.o')
    except: # ignore no *.o error
        pass
    run('ghc --make TestSwedia -main-is Main.testmain')
    run('./TestSwedia')
def convertTalbanken():
    try:
        run('rm ConvertTalbankenToPTB.o')
        run('rm ConvertTalbankenToTags.o')
    except:
        pass
    run('ghc --make TestConvertTalbanken')
    run('./TestConvertTalbanken')
def convertTags():
    try:
        run('rm ConvertTagsToTxt.o')
        run('rm ConvertTagsToConll.o')
    except:
        pass
    run('ghc --make TestConvertTags')
    run('./TestConvertTags')
def blade(runner, targets):
    for target in targets:
        print("Running target", target)
        getattr(runner, target)()
if __name__=="__main__":
    import test
    blade(test,
          sys.argv[1:] if sys.argv[1:] else 'swedia'.split())
