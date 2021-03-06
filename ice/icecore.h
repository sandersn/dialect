/* core R syntax distance code
 *
 * *ideally*, this can be #included by multiple small programs that do one
 * thing (and one thing only with syntax distance.) We'll see.
 */
#include <string>
#include <list>
#include <ext/hash_map>
#include <iostream>
#include <fstream>
#include <cmath>
#include "params.h"
#define SIGNIFICANCE ITERATIONS / 20
namespace __gnu_cxx { // culled from the internet.
  template<> // just wraps hash<char *>, which is entirely logical
  struct hash<std::string> { // and should have already been done
    hash<char *> h;
    size_t operator()(const std::string& s) const {
      return h(s.c_str());
    }
  };
}
using namespace std;
using namespace __gnu_cxx;
/* Ara */
double sum(const vector<double>& a) {
  double total = 0.0;
  for(int i=0; i < a.size(); i++)
    total += a[i];
  return total;
}
/* Hash */
hash_map<string,double, hash<string> > count (const vector<string>& a) {
  hash_map<string,double,hash<string> > h;
  for(int i=0; i < a.size(); i++) {
    h[a[i]]++;
  }
  return h;
}
/* Ice */
/* random classes from Stroustrup's 3rd edition */
class Randint {
  unsigned long randx;
public:
  Randint(long s = 0) { randx=s; }
  void seed(long s) { randx=s; }
  //magic numbers chosen to use 31 bits of a 32-bit long
  static long abs(long x) {return x & 0x7fffffff; }
  static double max() { return 2147483648.0; } // note: a double
  long draw() { return randx = randx * 1103515245 + 12345; }
  double fdraw() { return abs(draw()) / max(); } // in the interval [0,1]
  long operator()() { return abs(draw()); } // in the interval [0,2**31]
};
class Urand : public Randint { // uniform distro in the interval [0:n[
public:
  Urand(long s = 0) : Randint(s) { }
  long next(long n) { long r = long(n*fdraw()); return (r==n) ? n-1: r; }
};
template <class T> T choice(const vector<T>& l) {
  static Urand uni((unsigned)time(0));
  return l[uni.next(l.size())];
}
typedef vector<string> strings; // I can't get these two to use const string
typedef vector<vector<string> > dialect;
typedef hash_map<string, double, hash<string> > entry;
typedef hash_map<const string, pair<double,double>, hash<string> > sample; // but this is fine. ??
typedef hash_map<const string, vector<pair<double,double> >, hash<string> > samples;
typedef vector<pair<double,double> > totals;

template <class T, class U> T fst(pair<T,U> p) { return p.first; }
template <class T, class U> U snd(pair<T,U> p) { return p.second; }
template <class T> vector<T> concat(const vector<vector<T> >& as) {
  vector<T> acc;
  for(int i=0; i < as.size(); i++) {
    acc.insert(acc.end(), as[i].begin(), as[i].end());
  }
  return acc;
}
// = concat (maptimes (fun () -> choice dialect) 1000)
template <class T> vector<T> permutation(const vector<vector<T> >& dialect) {
  vector<T> acc;
  for(int i = 0; i < SAMPLES; i++) {
    vector<T> tmp = choice(dialect);
    acc.insert(acc.end(), tmp.begin(), tmp.end());
  }
  return acc;
}
// = concat
template <class T> vector<T> flatten (const vector<vector<T> >& dialect,
                                      int start, int offset) {
  vector<T> acc;
  for(int i = start; i < start + offset; i++) {
    vector<T> tmp = dialect[i];
    acc.insert(acc.end(), tmp.begin(), tmp.end());
  }
  return acc;
}
template <class T> void shuffle(vector<T>& l) {
  static Urand uni((unsigned)time(0));

  for(int i = l.size(); i > 1; i--) {
    int j = uni.next(i);
    T tmp = l[j];
    l[j] = l[i-1];
    l[i-1] = tmp;
  }
}
sample zip_ref (entry& h, entry& h2) {
  // I can't get these to be const entry&; apparently there is some
  // trouble with mixing iterator types in the h2[i->first] and h[i->first]
   sample h3;
   for(entry::const_iterator i = h.begin(); i!=h.end(); i++) {
     h3[i->first] = make_pair(i->second, h2[i->first]);
   }
   for(entry::const_iterator i = h2.begin(); i!=h2.end(); i++) {
     entry::const_iterator loc = h.find(i->first);
     if(loc==h.end()) {
       h3[i->first] = make_pair(h[i->first], i->second);
     }
   }
   return h3;
}
sample normalise(const strings& a, const strings& b,
                 int iterations=5, size_t total_types=0) {
  entry tmp1 = count(a); // Because zip_ref takes entry&, not const entry&,
  entry tmp2 = count(b); // I have to provide real l-values to zip_ref
  sample ab = zip_ref(tmp1, tmp2); // that's what Bjarne Stroustrup said anyway
  double tokens_a = a.size();
  double tokens_b = b.size();
  double tokens = tokens_a + tokens_b;
  double types = tmp1.size() + tmp2.size();
  double ci, fa, fb, f;
  for(int i = 0; i < iterations; i++) {
    for(sample::iterator i = ab.begin(); i!=ab.end(); i++) {
      ci = i->second.first + i->second.second;
      fa = i->second.first / tokens_a;
      fb = i->second.second / tokens_b;
      f = fa + fb;
      i->second.first = (ci * fa / f);
      i->second.second = (ci * fb / f);
      // WARNING:
      // Do not define RATIO_NORM and OVERUSE_NORM at the same time
      // OVERUSE_NORM is for use only in extracting features.
#ifdef RATIO_NORM
      i->second.first *= 2 * types / tokens;
      i->second.second *= 2 * types / tokens;
#endif
#ifdef OVERUSE_NORM
      ci = i->second.first + i->second.second;
      i->second.first = (i->second.first * tokens) / (ci * tokens_a);
      i->second.second = (i->second.second * tokens) / (ci * tokens_b);
#endif
    }
  }
  return ab;
}

double r(const sample& c) {
  double total = 0.0;
  for(sample::const_iterator i=c.begin(); i!=c.end(); i++) {
    total += abs(i->second.first - i->second.second);
  }
  return total;
}
inline double sqr(double d) { // or std::pow in cmath
  return d*d;
}
double r_sq(const sample& c) {
  double total = 0.0;
  for(sample::const_iterator i=c.begin(); i!=c.end(); i++) {
    total += sqr(i->second.first - i->second.second);
  }
  return total;
}
// this is actually KL symmetric divergence because it measures
// KL(P||Q) + KL(Q||P)
double kl(const sample& c) {
  double total = 0.0;
  for(sample::const_iterator i=c.begin(); i!=c.end(); i++) {
    if(i->second.first != 0 && i->second.second != 0) {
      total += i->second.first * log(i->second.first / i->second.second);
      total += i->second.second * log(i->second.second / i->second.first);
    }
  }
  return total;
}

// this is Jensen-Shannon divergence, which is based on KL divergence
double js(const sample& c) {
  double total = 0.0;
  for(sample::const_iterator i=c.begin(); i!=c.end(); i++) {
    double middle = (i->second.first + i->second.second) / 2;
    if(i->second.first != 0)
      total += i->second.first * log(i->second.first / middle) / 2;
    if(i->second.second != 0)
      total += i->second.second * log(i->second.second / middle) / 2;
  }
  return total;
}
double cos(const sample& c) {
  double a_sq = 0.0;
  double b_sq = 0.0;
  double total = 0.0;
  for(sample::const_iterator i=c.begin(); i!=c.end(); i++) {
    a_sq += i->second.first * i->second.first;
    b_sq += i->second.second * i->second.second;
    total += i->second.first * i->second.second;
  }
  return 1 - total / (sqrt(a_sq) * sqrt(b_sq));
}
// = ((<=) r_total)
bool comparepermutation(const dialect& a, const dialect& b) {
  dialect both_ab(a);
  both_ab.insert(both_ab.end(), b.begin(), b.end());
  int gt = 0;
  for(int i=0; i < ITERATIONS; i++) {
#ifdef FULLCORPUS
    sample total = normalise(flatten(a,0,a.size()), flatten(b,0,b.size()), 1);
#else
    sample total = normalise(permutation(a), permutation(b), 1);
#endif
    double total_r = R_MEASURE(total);
    // size_t total_types = total.size();
#ifdef FULLCORPUS
    shuffle(both_ab);
    double perm_r =
      R_MEASURE(normalise(flatten(both_ab, 0, a.size()),
                          flatten(both_ab, a.size(), b.size()), 1));
#else
    double perm_r =
      R_MEASURE(normalise(permutation(both_ab), permutation(both_ab), 1));
#endif
    if(perm_r > total_r) {
      cout << '-' << flush;
      gt++;
      if(gt > SIGNIFICANCE) return false;
    } else
      cout << '.' << flush;
  }
  cout << endl;
  return true;
}

pair<string, vector<vector<string> > > readfile(const char* filename) {
  ifstream f(filename);
  if(!f) {
    cout << filename << " is not found." << endl;
    throw filename;
  }
  string lang;
  getline(f,lang);
  vector<vector<string> > sss;
  vector<string> ss;
  string s;
  while(f) {
    getline(f,s);
    if(s=="***") {
      sss.push_back(ss);
      ss = vector<string>();
    } else {
      ss.push_back(s);
    }
  }
  sss.push_back(ss);
  return make_pair(lang, sss);
}
