CFLAGS += -Wall -Wextra

# Add ZeroMQ library
LDFLAGS += -lzmq

.PHONY: build run-daemon run-demo clean

build: daemon/daemon demo/simple

run-daemon: daemon/daemon
	./$<

run-demo: demo/simple
	./$<

clean:
	-rm */*.o
	-rm */*.a
	-rm daemon/daemon
	-rm demo/simple

ipc/libipc.a: ipc/ipc.o
	$(AR) crs $@ $^

daemon/%.o: daemon/%.cpp
	$(CXX) $< $(CFLAGS) -I ipc -c -o $@

daemon/daemon: daemon/main.o ipc/libipc.a
	$(CXX) $^ $(CFLAGS) $(LDFLAGS) -o $@

lib/%.o: lib/%.c
	$(CXX) $< $(CFLAGS) -I ipc -c -o $@

lib/libmpolicy.a: lib/mpolicy.o ipc/libipc.a
	$(AR) crs $@ $^

demo/simple: demo/simple.cpp lib/libmpolicy.a
	$(CXX) $< $(CXXFLAGS) $(LDFLAGS) -I lib -o $@ -L lib -l mpolicy
