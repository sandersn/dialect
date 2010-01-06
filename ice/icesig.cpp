#include "icecore.h"
int main(int argc, char** argv) {
  /*
  /// TEST
  entry test;
  test["a"] = 20.0;
  test["b"] = 5.0;
  test["c"] = 7.0;
  test["d"] = 2.0;
  test["e"] = 6.0;
  test["f"] = 5.0;
  vector<string> answer = max5(test);
  cout << "Length is " << answer.size() << endl;
  for(int i = 0; i < 5; i++) {
    cout << answer[i] << endl;
  }
  /// END TEST*/
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
