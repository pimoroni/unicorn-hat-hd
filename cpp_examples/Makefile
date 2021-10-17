forest: forest.cpp mtwrap.o
	g++ -o $@ -Og $+ -Wall -fwrapv

forest-opt: forest.cpp mtwrap.o
	g++ -o $@ -O2 $+ -Wall -fwrapv

mtwrap.o: mtwrap.cpp
	g++ -c mtwrap.cpp -O2 -fwrapv

clean:
	rm -f forest forest-opt mtwrap.o
.PHONY: clean
