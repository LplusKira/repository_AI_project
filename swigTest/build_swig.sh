
swig -python $1.i
gcc -c -fpic $1.c $1_wrap.c -I/usr/include/python2.7
gcc -shared $1.o $1_wrap.o -o _$1.so

python
