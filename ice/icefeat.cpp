#include "icecore.h"
/// Feature dump ///
void dumpcomparison(const dialect& a, const dialect& b) {
  sample total = normalise(concat(a), concat(b), 5);
  for(sample::iterator i = total.begin(); i != total.end(); i++) {
    cout << i->first << endl;
    cout << i->second.first - i->second.second << endl;
  }
}

int main(int argc, char** argv) {
  if(argc==3) {
    pair<string, vector<vector<string > > > l1 = readfile(argv[1]);
    pair<string, vector<vector<string > > > l2 = readfile(argv[2]);
    cout << l1.first << endl;
    cout << l2.first << endl;
    dumpcomparison(l1.second, l2.second);
  } else {
    cout << "Not enough arguments: " << argc << endl;
  }
}
