#include "icecore.h"
#include "iceextra.h"
int main(int argc, char** argv) {
  if(argc==3) {
    pair<string, vector<vector<string > > > l1 = readfile(argv[1]);
    pair<string, vector<vector<string > > > l2 = readfile(argv[2]);
    cout << l1.first << endl;
    cout << l2.first << endl;
    pair<double, double> avg_variance = r_avg_variance(l1.second, l2.second);
    cout << avg_variance.first << endl;
    cout << avg_variance.second << endl;
  } else {
    cout << "Not enough arguments: " << argc << endl;
  }
}
