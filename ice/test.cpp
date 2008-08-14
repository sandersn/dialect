#include <iostream>
#include "icectrl.cpp"
strings fillstr(entry& e) {
  // oh this is so stupid. Normalise requires strings, which it then countpaths
  // for me. So I have to take my clean-room hashes and recreate the strings so
  //  that normalise can turn them back into hashes.
  strings ss;
  for(entry::const_iterator i = e.begin(); i!=e.end(); i++) {
    for(int j = 0; j < (int)i->second; j++) {
      ss.push_back(i->first);
    }
  }
  return ss;
}
  /**
   * Tested so far:
   * read_file
   * count
   * concat
   * Though I should probably test them with real data and compare to
   * Python-checked answers
   * entry typedef
   * zip_ref
   * r, r_sq
   * Have not tested:
   * Major numerical imbalances (between large and small1 and small2)
   * Major imbalance in number of zeros
   * Specifically, the first question is relevant in deciding whether to cat
   * the full corpora or to sample them (in icectrl.cpp:compare:166)
   *
   * The paper claims that the last 'variety' stage of normalisation is not
   * necessary since it is a linear transformation and is only useful in ranking
   * the most telling trigrams. I am not even sure it is helpful for that...
   * This is run by the lines 105-108 and the expression
   * 2.0 * n / total_n in 115,116
   *
   * Hey! The r measure of normalise(concat(a), concat(b)) is really similar to
   * The r of normalise(concat(shuffle(a,b,size=a), shuffle(a,b,size=b)))
   * This is all wrong! It's like 247966 vs 247087. It's a tiny tiny bit lower
   * when it should be much lower. If London and Scotland ARE different
   *
   * TODO: Test shuffle on a short list. If it works, then try to figure out
   * another reason that compareshuffle gets the answer backward.
   */
int main(int argc, char** argv) {
  /*pair<string, dialect > test = readfile("test.dat");
  cout << test.first << endl;
  cout << test.second[1][1] << endl;
  for(dialect::const_iterator i=test.second.begin(); i!=test.second.end(); i++) {
    cout << "***";
    for(vector<string>::const_iterator j = i->begin(); j!=i->end(); j++) {
      cout << "|" << *j << "|";
    }
  }
  cout << endl;
  entry h;
  h["a"] = 15.0;
  h["b"] = 10.0;
  //h["c"] = 5.0;
  //h["d"] = 1.0;
  entry d;
  d["a"] = 90.0;
  d["b"] = 10.0;
  //d["c"] = 4.0;
  //d["e"] = 2.0;
  cout << "----zipped-----" << endl;
  sample s = zip_ref(h,d);
  for(sample::const_iterator i = s.begin(); i!=s.end(); i++) {
    cout << i->second.first << "|  |" << i->second.second << endl;
  }
  cout << "------r unscaled-------" << endl;
  cout << r(s) << endl;
  cout << "-----r^2 unscaled------" << endl;
  cout << r_sq(s) << endl;
  // normalisation:
  double totalh = 22.0;
  double totald = 27.0;
  cout << "-----normalised-------" << endl;
  sample hd = normalise(fillstr(d), fillstr(h));
  cout << r(hd) << endl;
  for(sample::const_iterator i = hd.begin(); i!=hd.end(); i++) {
    cout << i->first << ":" << i->second.first << ","
         << i->second.second << endl;
  }
  // is,js = [1,2,3,4],[5,6,7]
  vector<int> is;
  vector<int> js;
  is.push_back(1);
  is.push_back(2);
  is.push_back(3);
  is.push_back(4);
  js.push_back(5);
  js.push_back(6);
  js.push_back(7);
  pair<vector<int>, vector<int> > ijs = shuffle(is, js);
  cout << "shuffled is";
  for(int i = 0; i < is.size(); i++)
    cout << ijs.first[i];
  cout << "shuffled js";
  for(int i = 0; i < js.size(); i++)
    cout << ijs.second[i];
  dialect maclisp;
  dialect interlisp;
  vector<string> v;
  v.push_back("a");
  v.push_back("b");
  v.push_back("b");
  v.push_back("a");
  v.push_back("c");
  maclisp.push_back(v);
  v.clear();
  v.push_back("a");
  v.push_back("b");
  v.push_back("a");
  v.push_back("d");
  v.push_back("d");
  maclisp.push_back(v);
  v.clear();
  v.push_back("a");
  v.push_back("b");
  v.push_back("b");
  v.push_back("c");
  v.push_back("c");
  interlisp.push_back(v);
  v.clear();
  v.push_back("c");
  v.push_back("e");
  v.push_back("c");
  v.push_back("c");
  v.push_back("e");
  interlisp.push_back(v);
  v.clear();
  cout << compareshuffle(maclisp, interlisp) << endl;*/
  pair<string,dialect > scotlandpath = readfile("Scotland-path.dat");
  pair<string,dialect > scotlandtrigram = readfile("Scotland-trigram.dat");
  pair<string,dialect > stolcnadpath = readfile("Stolcnad-path.dat");
  pair<string,dialect > stolcnadtrigram = readfile("Stolcnad-trigram.dat");
  pair<string,dialect > londonpath = readfile("London-path.dat");
  pair<string,dialect > londontrigram = readfile("London-trigram.dat");
  pair<string,dialect > ldononpath = readfile("Ldonon-path.dat");
  pair<string,dialect > ldonontrigram = readfile("Ldonon-trigram.dat");
  cout << "London vs Scotland: ";
  cout << average_r(londonpath.second, scotlandpath.second) << endl;
  /*cout << "compare = {";
  cout << " 'permutation-trigrams-original': [";
  cout << comparepermutation(londontrigram.second, scotlandtrigram.second) << endl;
  cout << "]," << endl << " 'permutation-trigrams-mixed': [";
  cout << comparepermutation(ldonontrigram.second, stolcnadtrigram.second) << endl;
  cout << "]," << endl << " 'permutation-paths-original': [";
  cout << comparepermutation(londonpath.second, scotlandpath.second) << endl;
  cout << "]," << endl << " 'permutation-paths-mixed': [";
  cout << comparepermutation(ldononpath.second, stolcnadpath.second) << endl;
  cout << "]," << endl << " 'shuffle-trigrams-original': [";
  cout << compareshuffle(londontrigram.second, scotlandtrigram.second) << endl;
  cout << "]," << endl << " 'shuffle-trigrams-mixed': [";
  cout << compareshuffle(ldonontrigram.second, stolcnadtrigram.second) << endl;
  cout << "]," << endl << " 'shuffle-paths-original': [";
  cout << compareshuffle(londonpath.second, scotlandpath.second) << endl;
  cout << "]," << endl << " 'shuffle-paths-mixed': [";
  cout << compareshuffle(ldononpath.second, stolcnadpath.second) << endl;
  cout << "]," << endl << " 'original-trigrams-original': [";
  cout << compare(londontrigram.second, scotlandtrigram.second) << endl;
  cout << "]," << endl << " 'original-trigrams-mixed': [";
  cout << compare(ldonontrigram.second, stolcnadtrigram.second) << endl;
  cout << "]," << endl << " 'original-paths-original': [";
  cout << compare(londonpath.second, scotlandpath.second) << endl;
  cout << "]," << endl << " 'original-paths-mixed': [";
  cout << compare(ldononpath.second, stolcnadpath.second) << endl;
  cout << "]}"; */
  
  /* d2 = {'a': 0.33333333333333331, 'c': 0.14814814814814814, 'b': 0.44444444444444442, 'e': 0.07407407407407407}
   * h2 = {'a': 0.45454545454545453, 'c': 0.22727272727272727, 'b': 0.27272727272727271, 'd': 0.045454545454545456}
   * hd = dct.zip(d,h, default=0)
   * hd2 = dct.zip(d2,h2, default=0)
   * add = lambda (x,y): x+y
   * hdsum = dct.map(add, hd)
   * hd2sum = dct.map(add, hd2)
   * sentence = dct.map(lambda ((fi,fj), t, tf):(fi*t/tf, fj*t/tf), dct.zip(hd2,hdsum, hd2sum))
   * sentence = {'a': (8.0384615384615383, 10.961538461538462), 'c': (3.551569506726457, 5.4484304932735421), 'b': (11.15492957746479, 6.8450704225352101), 'e': (2.0, 0.0), 'd': (0.0, 1.0)}
   * variety = 2 * len(hd) / (sum(h.values()) + sum(d.values()))
   * variety = 0.32653061224489793
   * normed = dct.map(lambda (ci,cj): (ci*variety,cj*variety), sentence)
   * normed = {'a': (2.6248037676609104, 3.5792778649921506), 'c': (1.1596961654617002, 1.7790793447423809), 'b': (3.6424259844782982, 2.2351250359298644), 'e': (0.65306122448979587, 0.0), 'd': (0.0, 0.32653061224489793)}
   * def r(mns): return sum(abs(m-n) for m,n in mns)
   * r(normed.values()) = 3.96075
   */
}
