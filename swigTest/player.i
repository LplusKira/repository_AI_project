%module player
%include "std_vector.i"
namespace std {
  %template(Intvector) vector<int>;
 }

%{
  #include <vector>
  using namespace std;
  void fifo_test(vector<int> a);  
%}

void fifo_test(std::vector<int> a);

/*
%{
   void fifo_test(Intvector);
   %}*/



