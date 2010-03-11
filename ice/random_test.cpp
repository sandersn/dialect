#include "icecore.h"
#include <iostream>
using namespace std;
#define N 5
#define TRIALS 300000
void random_test() {
  static Urand uni((unsigned)time(0));
  int is[N];
  for(int i = 0; i < N; i++) {
    is[i] = 0;
  }
  for(int _ = 0; _ < N * TRIALS; _++) {
    is[uni.next(N)]++;
  }
  for(int i = 0; i < N; i++) {
    cout << is[i] << ' ';
  }
  cout << endl;
}
void shuffle_test() {
  vector<int> l(N);
  int rs[N][N];
  for(int i = 0; i < N; i++) {
    l[i] = i;
    for(int j = 0; j < N; j++) {
      rs[i][j] = 0;
    }
  }
  for(int _ = 0; _ < N * TRIALS; _++) {
    shuffle(l);
    for(int i = 0; i < N; i++) {
      rs[i][l[i]]++;
    }
  }
  for(int i = 0; i < N; i++) {
    for(int j = 0; j < N; j++) {
      cout << rs[i][j] << ' ';
    }
    cout << endl;
  }
}
void choice_test() {
  vector<int> l(N);
  int is[N];
  for(int i = 0; i < N; i++) {
    is[i] = 0;
    l[i] = i;
  }
  for(int _ = 0; _ < N * TRIALS; _++) {
    is[choice(l)]++;
  }
  for(int i = 0; i < N; i++) {
    cout << is[i] << ' ';
  }
  cout << endl;
}
int main() {
  cout << "-------- random test ---------\n";
  random_test();
  cout << "-------- shuffle test ---------\n";
  shuffle_test();
  cout << "-------- choice test ---------\n";
  choice_test();
  return 0;
}
