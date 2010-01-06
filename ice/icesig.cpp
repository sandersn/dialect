#include "icecore.h"
int main(int argc, char** argv) {
  if(argc==2) {
    pair<string, vector<vector<string > > > l1 = readfile(argv[1]);
    cout << "Control: " << l1.first << endl;
    cout << comparepermutation(l1.second, l1.second) << endl;
  } else if (argc==3) {
    pair<string, vector<vector<string > > > l1 = readfile(argv[1]);
    pair<string, vector<vector<string > > > l2 = readfile(argv[2]);
    cout << l1.first << endl;
    cout << l2.first << endl;
    cout << comparepermutation(l1.second, l2.second) << endl;
    //cout << average_r(l1.second, l2.second) << endl;
  } else {
    cout << "Not enough arguments: " << argc << endl;
    }
  return 0;
}
