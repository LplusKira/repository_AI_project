%module structtest
%include "std_vector.i"
namespace std {
  %template(Intvector) vector<int>;
 }

%{
  #include <vector>
  using namespace std;
  struct s{
    int i;
    vector<int> v;
  };
  struct s make_struct();  
%}

struct s{
  int i;
  std::vector<int> v;
};
struct s make_struct();
