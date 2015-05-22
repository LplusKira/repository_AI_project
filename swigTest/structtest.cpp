#include <vector>
using namespace std;

struct s{
  int i;
  vector<int> v;
} st;

struct s make_struct(){
  struct s ss;
  ss.i = 111;
  ss.v.push_back(11);
  return ss;
}
