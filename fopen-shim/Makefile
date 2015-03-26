fopen_shim.so: fopen_shim.c
	gcc -shared -fPIC fopen_shim.c -o fopen_shim.so -ldl

all: fopen_shim.so

clean:
	rm *.so