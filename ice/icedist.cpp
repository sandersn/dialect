#include "icecore.h"
/// average r (for real) plus a failed definition of variance ///
pair<double, double> r_avg_variance (const dialect& a, const dialect& b) {
#define AVG_ITERATIONS 10
  double sum = 0.0;
  vector<double> rs(AVG_ITERATIONS);
  for(int i = 0; i < AVG_ITERATIONS; i++) {
#ifdef FULLCORPUS
    double r_value = R_MEASURE(normalise(flatten(a, 0, a.size()),
                                         flatten(b, 0, b.size()), 5));
#else
    double r_value = R_MEASURE(normalise(permutation(a), permutation(b), 5));
#endif
    sum += r_value;
    rs.push_back(r_value);
  }
  double avg = sum / AVG_ITERATIONS;
  double variance = 0.0;
  for(int i = 0; i < AVG_ITERATIONS; i++) {
    variance += sqr(rs[i] - avg);
  }
  return make_pair(avg, variance / AVG_ITERATIONS);
}


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
