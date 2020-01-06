# Add ZeroMQ library
LDFLAGS += -lzmq

# Do not echo the commands before running them
.SILENT:

.PHONY: run clean

run-daemon: daemon/daemon
	./$<

run-demo: demo/simple
	./$<

clean:
	-rm */*.o
	-rm */*.a
	-rm daemon/daemon
	-rm simple/simple

ipc/libipc.a: ipc/ipc.o
	$(CC) $^ $(CFLAGS) $(LDFLAGS) -r -o $@

daemon/%.o: daemon/%.c
	$(CC) $< $(CFLAGS) -I ipc -c -o $@

daemon/daemon: daemon/main.o ipc/libipc.a
	$(CC) $^ $(CFLAGS) $(LDFLAGS) -o $@

lib/%.o: lib/%.c
	$(CC) $< $(CFLAGS) -I ipc -c -o $@

lib/libmpolicy.a: lib/mpolicy.o ipc/libipc.a
	$(CC) $^ $(CFLAGS) $(LDFLAGS) -r -o $@

demo/simple: demo/simple.cpp lib/libmpolicy.a
	$(CXX) $< $(CXXFLAGS) $(LDFLAGS) -I lib -o $@ -L lib -l mpolicy
