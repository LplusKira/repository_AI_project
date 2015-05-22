swig -python -c++ $1.i
g++ -c -fpic $1.cpp $1_wrap.cxx -I/usr/include/python2.7 &&  g++ -shared $1.o $1_wrap.o -o _$1.so && python $1_test.py
