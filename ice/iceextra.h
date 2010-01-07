/////
/// Extra R distance code not currently in use
/////
sample normalise_w_types(const strings& a, const strings& b,
                 int iterations=5, size_t total_types=0) {
  sample ab = countpaths(a,b);
  double len_a = a.size();
  double len_b = b.size();
  double total_n = len_a + len_b;
  double n;
  if(!total_types) n = ab.size();
  else n = total_types;
  double ci, fa, fb, f;
  for(int i = 0; i < iterations; i++) {
    for(sample::iterator i = ab.begin(); i!=ab.end(); i++) {
      ci = i->second.first + i->second.second;
      fa = i->second.first / len_a;
      fb = i->second.second / len_b;
      f = fa + fb;
      i->second.first = (ci * fa * 2.0 * n) / (f * total_n);
      i->second.second = (ci * fb * 2.0 * n) / (f * total_n);
    }
  }
  return ab;
}

bool normaliseall(double total_r, size_t total_types,
                 const dialect& a, const dialect& b) {
  // this next may be a bad idea without the ability to delete b
  // In Python and Caml I assumed the GC ate b before long.
  dialect both_ab(a);
  both_ab.insert(both_ab.end(), b.begin(), b.end()); //delete a; delete b; ??
  int gt = 0;
  for(int i=0; i < ITERATIONS; i++) {
    double perm_r =
      R_MEASURE(normalise_w_types(permutation(both_ab), permutation(both_ab), 5, total_types));
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
bool normaliseshuffle(double total_r, const dialect& a, const dialect& b) {
  int gt = 0;
  for(int i=0; i < ITERATIONS; i++) {
    pair<dialect,dialect> shuffled = shuffle(a, b);
    double shuffle_r = R_MEASURE(normalise(concat(shuffled.first), concat(shuffled.second), 5));
    cout << (total_r - shuffle_r) << ", " << flush;
    if(shuffle_r > total_r) gt++;
    if(gt > SIGNIFICANCE) return false;
  }
  cout << endl;
  return true;
}
// = ((<=) r_total)
bool compare(const dialect& dialect_a, const dialect& dialect_b) {
  sample test = normalise(concat(dialect_a), concat(dialect_b), 5);
  double total_r = R_MEASURE(test); //R_MEASURE is one of r or r_sq
  cout << total_r << endl;
  return normaliseall(total_r, test.size(), dialect_a, dialect_b);
}


// = ((<=) r_total)
bool compareshuffle(const dialect& a, const dialect& b) {
  sample test = normalise(concat(a), concat(b), 5);
  double total_r = R_MEASURE(test); //R_MEASURE is one of r or r_sq
  //cout << total_r << endl;
  return normaliseshuffle(total_r, a, b);
}
/// Find most interesting leaf-ancestor paths ///
void insertByAbsSnd(list<pair<string, double> >& l,
                 const pair<string, double>& entry) {
  double key = abs(entry.second);
  for(list<pair<string, double> >::iterator i = l.begin(); i != l.end(); i++) {
    if(key > abs(i->second)) {
      l.insert(i, entry);
      return;
    }
  }
  l.insert(l.end(), entry);
}
void max5(const entry& e) {
  list<pair<string,double> > best;
  entry::const_iterator j = e.begin();
  double leastBest = j->second;
  // of course there will always be at least 5 entries because
  // there will always be either 500 or 1000
  for(int i = 0; i < 5; i++, j++) {
    insertByAbsSnd(best, make_pair(j->first, j->second));
  }
  for(; j!=e.end(); j++) {
    if(abs(j->second) > leastBest) {
      insertByAbsSnd(best, make_pair(j->first, j->second));
      best.pop_back();
      leastBest = abs(best.back().second);
    }
  }
  for(list<pair<string,double> >::iterator i = best.begin(); i != best.end(); i++) {
    cout << i->first << ' ' << i->second << '\t';
  }
  cout << endl;
}
// best5r = maxN 5 . Dict.map (abs . uncurry (-))
void best5r(const sample& c) {
  entry halfR;
  for(sample::const_iterator i = c.begin(); i!=c.end(); i++) {
    halfR[i->first] = i->second.first - i->second.second;
  }
  max5(halfR);
}
/// ///
double average_r(const dialect& a, const dialect& b) {
  double sum = 0.0;
  for(int i = 0; i < 100; i++) {
    sample normed = normalise(permutation(a), permutation(b), 5);
    sum += R_MEASURE(normed);
    best5r(normed);
  }
  return sum / 100.0;
}
pair<double, double> r_avg_variance (const dialect& a, const dialect& b) {
#define AVG_ITERATIONS 10
  double sum = 0.0;
  vector<double> rs(AVG_ITERATIONS);
  for(int i = 0; i < AVG_ITERATIONS; i++) {
    double r_value = R_MEASURE(normalise(permutation(a), permutation(b), 5));
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
